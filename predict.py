import os
import shutil
import tarfile
import zipfile
from typing import List
from cog import BasePredictor, Input, Path
from helpers.comfyui import ComfyUI

OUTPUT_DIR = "/tmp/outputs"
INPUT_DIR = "/tmp/inputs"
COMFYUI_TEMP_OUTPUT_DIR = "ComfyUI/temp"

with open("examples/photomaker.json", "r") as file:
    EXAMPLE_WORKFLOW_JSON = file.read()


class Predictor(BasePredictor):
    def setup(self):
        self.comfyUI = ComfyUI("127.0.0.1:8188")
        self.comfyUI.start_server(OUTPUT_DIR, INPUT_DIR)

    def cleanup(self):
        for directory in [OUTPUT_DIR, INPUT_DIR, COMFYUI_TEMP_OUTPUT_DIR]:
            if os.path.exists(directory):
                shutil.rmtree(directory)
            os.makedirs(directory)

    def handle_input_file(self, input_file: Path):
        file_extension = os.path.splitext(input_file)[1]
        if file_extension == ".tar":
            with tarfile.open(input_file, "r") as tar:
                tar.extractall(INPUT_DIR)
        elif file_extension == ".zip":
            with zipfile.ZipFile(input_file, "r") as zip_ref:
                zip_ref.extractall(INPUT_DIR)
        elif file_extension in [".jpg", ".jpeg", ".png", ".webp"]:
            shutil.copy(input_file, os.path.join(INPUT_DIR, f"input{file_extension}"))
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

        print("====================================")
        print(f"Inputs uploaded to {INPUT_DIR}:")
        self.log_and_collect_files(INPUT_DIR)
        print("====================================")

    def log_and_collect_files(self, directory, prefix=""):
        files = []
        for f in os.listdir(directory):
            if f == "__MACOSX":
                continue
            path = os.path.join(directory, f)
            if os.path.isfile(path):
                print(f"{prefix}{f}")
                files.append(Path(path))
            elif os.path.isdir(path):
                print(f"{prefix}{f}/")
                files.extend(self.log_and_collect_files(path, prefix=f"{prefix}{f}/"))
        return files

    def transform_prompt_map(self, prompt_map_string: str):
        """
        Transform the given prompt_map string into a formatted string suitable for JSON injection.

        Parameters
        ----------
        prompt_map_string : str
            A string containing animation prompts in the format 'frame number : prompt at this frame',
            separated by '|'. Colons inside the prompt description are allowed.

        Returns
        -------
        str
            A formatted string where each prompt is represented as '"frame": "description"'.
        """

        segments = prompt_map_string.split("|")

        formatted_segments = []
        for segment in segments:
            frame, prompt = segment.split(":", 1)
            frame = frame.strip()
            prompt = prompt.strip()

            formatted_segment = f'"{frame}": "{prompt}"'
            formatted_segments.append(formatted_segment)

        return ", ".join(formatted_segments)

    def predict(
        self,
        prompt: str = Input(
            description="Prompt for changes in animation. Provide 'frame number : prompt at this frame', separate different prompts with '|'. Make sure the frame number does not exceed the length of video (frames)",
            default="0: a big (chrome:1.1) cyborg robot dance, (white science lab:1.1) | 100 :a (chrome:1.1) cyborg robot dance, (red led blinksp:1.1), (white science lab:1.1)",
        ),
        negative_prompt: str = Input(
            description="Input Negative Prompt (constant)",
            default="embedding:easynegative, (worst quality, low quality: 1.3), zombie, horror, distorted, photo, nfsw",
        ),
        first_num_inference_steps: int = Input(
            description="Number of denoising steps", ge=1, le=50, default=15
        ),
        first_guidance_scale: float = Input(
            description="Scale for classifier-free guidance", ge=1, le=50, default=7.5
        ),
        second_num_inference_steps: int = Input(
            description="Second pass, for video interoplation. Number of denoising steps",
            ge=1,
            le=50,
            default=15,
        ),
        second_guidance_scale: float = Input(
            description="Second pass, for video interoplation. Scale for classifier-free guidance",
            ge=1,
            le=50,
            default=8.5,
        ),
        pose_video: Path = Input(
            description="Video of a subject doing something fun or interesting, this video will be used to track any people and their pose estimations for the final video",
            default=None,
        ),
        subject_image: Path = Input(
            description="An image of what the subject should look like in the final video",
            default=None,
        ),
        subject_controlnet_strength: float = Input(
            description="Strength of the controlnet for the subject/character image",
            ge=0.0,
            le=1.0,
            default=0.2,
        ),
        background_image: Path = Input(
            description="An image of what the background should look like in the final video",
            default=None,
        ),
        background_controlnet_strength: float = Input(
            description="Strength of the controlnet for the background image",
            ge=0.0,
            le=1.0,
            default=0.4,
        ),
        return_temp_files: bool = Input(
            description="Return any temporary files, such as preprocessed controlnet images. Useful for debugging.",
            default=False,
        ),
        randomise_seeds: bool = Input(
            description="Automatically randomise seeds (seed, noise_seed, rand_seed)",
            default=True,
        ),
    ) -> List[Path]:
        """Run a single prediction on the model"""
        self.cleanup()

        # Read the workflow JSON from 'workflow_api.json'
        workflow_json_path = "workflow_api.json"
        with open(workflow_json_path, "r") as file:
            workflow_json_content = file.read()

        input_files = {
            "pose_video": pose_video,
            "subject_image": subject_image,
            "background_image": background_image,
        }
        for name, file_path in input_files.items():
            if file_path is not None:
                file_extension = os.path.splitext(file_path)[1]
                new_file_name = f"{name}{file_extension}"  # Correct filename format
                shutil.copy(file_path, os.path.join(INPUT_DIR, new_file_name))
                # Hard code the replacement for each specific case
                if name == "pose_video":
                    print(f"Replacing POSE_VIDEO.mp4 with {new_file_name}")
                    workflow_json_content = workflow_json_content.replace(
                        "POSE_VIDEO.mp4", new_file_name
                    )
                elif name == "subject_image":
                    print(f"Replacing SUBJECT_IMAGE.jpg with {new_file_name}")
                    workflow_json_content = workflow_json_content.replace(
                        "SUBJECT_IMAGE.jpg", new_file_name
                    )
                elif name == "background_image":
                    print(f"Replacing BACKGROUND_IMAGE.jpg with {new_file_name}")
                    workflow_json_content = workflow_json_content.replace(
                        "BACKGROUND_IMAGE.jpg", new_file_name
                    )

        prompt = self.transform_prompt_map(prompt)
        prompt = prompt.replace('"', '\\"')
        print(f"Replacing $PROMPT with {prompt}")
        workflow_json_content = workflow_json_content.replace(
            '"$PROMPT"',
            f'"{prompt}"',
        )
        # negative_prompt = self.transform_prompt_map(negative_prompt)
        # negative_prompt = negative_prompt.replace('"', '\\"')
        print(f"Replacing $NEGATIVE_PROMPT with {negative_prompt}")
        workflow_json_content = workflow_json_content.replace(
            '"$NEGATIVE_PROMPT"',
            f'"{negative_prompt}"',
        )

        print(f"Replacing $FIRST_NUM_INFERENCE_STEPS with {first_num_inference_steps}")
        workflow_json_content = workflow_json_content.replace(
            '"$FIRST_NUM_INFERENCE_STEPS"',
            str(first_num_inference_steps),
        )

        print(f"Replacing $FIRST_GUIDANCE_SCALE with {first_guidance_scale}")
        workflow_json_content = workflow_json_content.replace(
            '"$FIRST_GUIDANCE_SCALE"',
            str(first_guidance_scale),
        )

        print(
            f"Replacing $SECOND_NUM_INFERENCE_STEPS with {second_num_inference_steps}"
        )
        workflow_json_content = workflow_json_content.replace(
            '"$SECOND_NUM_INFERENCE_STEPS"',
            str(second_num_inference_steps),
        )

        print(f"Replacing $SECOND_GUIDANCE_SCALE with {second_guidance_scale}")
        workflow_json_content = workflow_json_content.replace(
            '"$SECOND_GUIDANCE_SCALE"',
            str(second_guidance_scale),
        )

        print(
            f"Replacing $SUBJECT_CONTROLNET_STRENGTH with {subject_controlnet_strength}"
        )
        workflow_json_content = workflow_json_content.replace(
            '"$SUBJECT_CONTROLNET_STRENGTH"',
            str(subject_controlnet_strength),
        )

        print(
            f"Replacing $BACKGROUND_CONTROLNET_STRENGTH with {background_controlnet_strength}"
        )
        workflow_json_content = workflow_json_content.replace(
            '"$BACKGROUND_CONTROLNET_STRENGTH"',
            str(background_controlnet_strength),
        )

        # NOTE: Sanity check
        with open("replaced_workflow_api.json", "w") as file:
            file.write(workflow_json_content)

        # Now, workflow_json_content contains the actual JSON content as a string
        wf = self.comfyUI.load_workflow(workflow_json_content)

        if randomise_seeds:
            self.comfyUI.randomise_seeds(wf)

        self.comfyUI.connect()
        self.comfyUI.run_workflow(wf)

        files = []
        output_directories = [OUTPUT_DIR]
        if return_temp_files:
            output_directories.append(COMFYUI_TEMP_OUTPUT_DIR)

        for directory in output_directories:
            print(f"Contents of {directory}:")
            files.extend(self.log_and_collect_files(directory))
        print(files)

        mp4_files = [file for file in files if file.suffix == ".mp4"]
        hr_mp4_files = [file for file in mp4_files if "HR" in file.name]
        if len(mp4_files) > 1 and hr_mp4_files:
            return hr_mp4_files
        return mp4_files
