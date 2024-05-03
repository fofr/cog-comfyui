from custom_node_helper import CustomNodeHelper

RIFE_MODELS = [
    "rife40.pth",
    "rife41.pth",
    "rife42.pth",
    "rife43.pth",
    "rife44.pth",
    "rife45.pth",
    "rife46.pth",
    "rife47.pth",
    "rife48.pth",
    "rife49.pth",
    "sudo_rife4_269.662_testV1_scale1.pth",
]

FILM_MODELS = [
    "film_net_fp32.pt",
]

AMT_MODELS = [
    "amt-s.pth",
    "amt-g.pth",
    "amt-l.pth",
    "gopro_amt-s.pth",
]

CAIN_MODELS = [
    "pretrained_cain.pth",
]

FRAME_INTERPOLATION_MODELS_PATH = (
    "ComfyUI/custom_nodes/ComfyUI-Frame-Interpolation/ckpts"
)


class ComfyUI_Frame_Interpolation(CustomNodeHelper):
    @staticmethod
    def models():
        return RIFE_MODELS + FILM_MODELS + AMT_MODELS + CAIN_MODELS

    @staticmethod
    def weights_map(base_url):
        model_categories = {
            "rife": RIFE_MODELS,
            "film": FILM_MODELS,
            "amt": AMT_MODELS,
            "cain": CAIN_MODELS,
        }
        weights = {}
        for category, models in model_categories.items():
            for model in models:
                weights[model] = {
                    "url": f"{base_url}/custom_nodes/ComfyUI-Frame-Interpolation/{category}/{model}.tar",
                    "dest": f"{FRAME_INTERPOLATION_MODELS_PATH}/{category}",
                }
        return weights

    @staticmethod
    def check_for_unsupported_nodes(node):
        unsupported_nodes = {
            "IFRNet VFI": "Use RIFE or FILM - IFRNet weights are not available",
            "IFUnet VFI": "Use RIFE or FILM - IFUnet weights are not available",
            "MCM VFI": "Use RIFE or FILM - MCM is not available because cupy is not installed",
            "GMFSS Fortuna VFI": "Use RIFE or FILM - GMFSS Fortuna VFI is not available because cupy is not installed",
            "Sepconv VFI": "Use RIFE or FILM - Sepconv VFI is not available because cupy is not installed",
            "STMFNet VFI": "Use RIFE or FILM - STMFNet VFI is not available because cupy is not installed",
            "FLAVR VFI": "Use RIFE or FILM - FLAVR VFI weights are not available",
        }
        node.raise_if_unsupported(unsupported_nodes)
