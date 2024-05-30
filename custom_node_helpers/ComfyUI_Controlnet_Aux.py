from custom_node_helper import CustomNodeHelper
from config import config

MODELS = {
    "UNet.pth": "bdsqlsz/qinglong_controlnet-lllite/Annotators",
    "mobile_sam.pt": "dhkim2810/MobileSAM",
    "hrnetv2_w64_imagenet_pretrained.pth": "hr16/ControlNet-HandRefiner-pruned",
    "graphormer_hand_state_dict.bin": "hr16/ControlNet-HandRefiner-pruned",
    "rtmpose-m_ap10k_256_bs5.torchscript.pt": "hr16/DWPose-TorchScript-BatchSize5",
    "dw-ll_ucoco_384_bs5.torchscript.pt": "hr16/DWPose-TorchScript-BatchSize5",
    "rtmpose-m_ap10k_256.onnx": "hr16/UnJIT-DWPose",
    "yolo_nas_s_fp16.onnx": "hr16/yolo-nas-fp16",
    "yolo_nas_m_fp16.onnx": "hr16/yolo-nas-fp16",
    "yolox_l.torchscript.pt": "hr16/yolox-onnx",
    "densepose_r101_fpn_dl.torchscript": "LayerNorm/DensePose-TorchScript-with-hint-image",
    "densepose_r50_fpn_dl.torchscript": "LayerNorm/DensePose-TorchScript-with-hint-image",
    "mlsd_large_512_fp32.pth": "lllyasviel/Annotators",
    "150_16_swin_l_oneformer_coco_100ep.pth": "lllyasviel/Annotators",
    "ControlNetHED.pth": "lllyasviel/Annotators",
    "ZoeD_M12_N.pt": "lllyasviel/Annotators",
    "scannet.pt": "lllyasviel/Annotators",
    "hand_pose_model.pth": "lllyasviel/Annotators",
    "upernet_global_small.pth": "lllyasviel/Annotators",
    "latest_net_G.pth": "lllyasviel/Annotators",
    "netG.pth": "lllyasviel/Annotators",
    "sk_model2.pth": "lllyasviel/Annotators",
    "dpt_hybrid-midas-501f0c75.pt": "lllyasviel/Annotators",
    "table5_pidinet.pth": "lllyasviel/Annotators",
    "erika.pth": "lllyasviel/Annotators",
    "250_16_swin_l_oneformer_ade20k_160k.pth": "lllyasviel/Annotators",
    "sk_model.pth": "lllyasviel/Annotators",
    "body_pose_model.pth": "lllyasviel/Annotators",
    "res101.pth": "lllyasviel/Annotators",
    "facenet.pth": "lllyasviel/Annotators",
    "isnetis.ckpt": "skytnt/anime-seg",
    "yolox_l.onnx": "yzd-v/DWPose",
    "dw-ll_ucoco_384.onnx": "yzd-v/DWPose",
    "7_model.pth": "bdsqlsz/qinglong_controlnet-lllite/Annotators",
    "gmflow-scale1-mixdata.pth": "hr16/Unimatch",
    "gmflow-scale2-mixdata.pth": "hr16/Unimatch",
    "gmflow-scale2-regrefine6-mixdata.pth": "hr16/Unimatch",
    "depth_anything_vitl14.pth": "LiheYoung/Depth-Anything/checkpoints",
    "depth_anything_vitb14.pth": "LiheYoung/Depth-Anything/checkpoints",
    "depth_anything_vits14.pth": "LiheYoung/Depth-Anything/checkpoints",
    "diffusion_edge_indoor.pt": "hr16/Diffusion-Edge",
    "diffusion_edge_natrual.pt": "hr16/Diffusion-Edge",  # (model has a typo)
    "diffusion_edge_urban.pt": "hr16/Diffusion-Edge",
    "dsine.pt": "hr16/Diffusion-Edge",
    "swin_b-68c6b09e.pth": "torch",
    "vgg16-397923af.pth": "torch",
    "depth_anything_metric_depth_indoor.pt": "LiheYoung/Depth-Anything/checkpoints_metric_depth",
    "depth_anything_metric_depth_outdoor.pt": "LiheYoung/Depth-Anything/checkpoints_metric_depth",
    "MTEED.pth": "TheMistoAI/MistoLine/Anyline",
    "metric_depth_vit_small_800k.pth": "JUGGHM/Metric3D",
    "metric_depth_vit_large_800k.pth": "JUGGHM/Metric3D",
    "metric_depth_vit_giant2_800k.pth": "JUGGHM/Metric3D",
}


class ComfyUI_Controlnet_Aux(CustomNodeHelper):
    @staticmethod
    def prepare(**kwargs):
        kwargs["weights_downloader"].download_if_not_exists(
            "mobilenet_v2-b0353104.pth",
            f"{config['WEIGHTS_BASE_URL']}/custom_nodes/comfyui_controlnet_aux/mobilenet_v2-b0353104.pth.tar",
            "/root/.cache/torch/hub/checkpoints/",
        )

    @staticmethod
    def models():
        return MODELS

    @staticmethod
    def weights_map(base_url):
        return {
            key: {
                "url": f"{base_url}/custom_nodes/comfyui_controlnet_aux/{key}.tar",
                "dest": f"ComfyUI/custom_nodes/comfyui_controlnet_aux/ckpts/{MODELS[key]}",
            }
            for key in MODELS
        }

    # Controlnet preprocessor models are not included in the API JSON
    # We need to add them manually based on the nodes being used to
    # avoid them being downloaded automatically from elsewhere
    @staticmethod
    def node_class_mapping():
        return {
            # Depth
            "MiDaS-NormalMapPreprocessor": "dpt_hybrid-midas-501f0c75.pt",
            "MiDaS-DepthMapPreprocessor": "dpt_hybrid-midas-501f0c75.pt",
            "Zoe-DepthMapPreprocessor": "ZoeD_M12_N.pt",
            "LeReS-DepthMapPreprocessor": ["res101.pth", "latest_net_G.pth"],
            "MeshGraphormer-DepthMapPreprocessor": [
                "hrnetv2_w64_imagenet_pretrained.pth",
                "graphormer_hand_state_dict.bin",
            ],
            "DepthAnythingPreprocessor": [
                "depth_anything_vitl14.pth",
                "depth_anything_vitb14.pth",
                "depth_anything_vits14.pth",
            ],
            "Zoe_DepthAnythingPreprocessor": [
                "depth_anything_metric_depth_indoor.pt",
                "depth_anything_metric_depth_outdoor.pt",
            ],
            "Metric3DPreprocessor": [
                "metric_depth_vit_small_800k.pth",
                "metric_depth_vit_large_800k.pth",
                "metric_depth_vit_giant2_800k.pth",
            ],
            "Metric3D-NormalMapPreprocessor": [
                "metric_depth_vit_small_800k.pth",
                "metric_depth_vit_large_800k.pth",
                "metric_depth_vit_giant2_800k.pth",
            ],
            # Segmentation
            "BAE-NormalMapPreprocessor": "scannet.pt",
            "OneFormer-COCO-SemSegPreprocessor": "150_16_swin_l_oneformer_coco_100ep.pth",
            "OneFormer-ADE20K-SemSegPreprocessor": "250_16_swin_l_oneformer_ade20k_160k.pth",
            "UniFormer-SemSegPreprocessor": "upernet_global_small.pth",
            "SemSegPreprocessor": "upernet_global_small.pth",
            "AnimeFace_SemSegPreprocessor": ["UNet.pth", "isnetis.ckpt"],
            "SAMPreprocessor": "mobile_sam.pt",
            "DSINE-NormalMapPreprocessor": "dsine.pt",
            # Line extractors
            "AnimeLineArtPreprocessor": "netG.pth",
            "HEDPreprocessor": "ControlNetHED.pth",
            "FakeScribblePreprocessor": "ControlNetHED.pth",
            "M-LSDPreprocessor": "mlsd_large_512_fp32.pth",
            "PiDiNetPreprocessor": "table5_pidinet.pth",
            "LineArtPreprocessor": ["sk_model.pth", "sk_model2.pth"],
            "Manga2Anime_LineArt_Preprocessor": "erika.pth",
            "TEEDPreprocessor": "7_model.pth",
            "DiffusionEdge_Preprocessor": [
                "diffusion_edge_indoor.pt",
                "diffusion_edge_natrual.pt",  # model has a typo
                "diffusion_edge_urban.pt",
                "vgg16-397923af.pth",
                "swin_b-68c6b09e.pth",
            ],
            "AnyLineArtPreprocessor_aux": [
                "MTEED.pth",
                "erika.pth",
                "netG.pth",
                "sk_model2.pth",
            ],
            # Pose
            "OpenposePreprocessor": [
                "body_pose_model.pth",
                "hand_pose_model.pth",
                "facenet.pth",
            ],
            # Optical flow
            "Unimatch_OptFlowPreprocessor": [
                "gmflow-scale1-mixdata.pth",
                "gmflow-scale2-mixdata.pth",
                "gmflow-scale2-regrefine6-mixdata.pth",
            ],
        }

    @staticmethod
    def add_weights(weights_to_download, node):
        node_mapping = ComfyUI_Controlnet_Aux.node_class_mapping()

        if node.is_type_in(node_mapping.keys()):
            class_weights = node_mapping[node.type()]
            weights_to_download.extend(
                class_weights if isinstance(class_weights, list) else [class_weights]
            )

        # Additional check for AIO_Preprocessor and its preprocessor input value
        if node.is_type("AIO_Preprocessor"):
            preprocessor = node.input("preprocessor")
            if preprocessor in node_mapping:
                preprocessor_weights = node_mapping[preprocessor]
                weights_to_download.extend(
                    preprocessor_weights
                    if isinstance(preprocessor_weights, list)
                    else [preprocessor_weights]
                )
