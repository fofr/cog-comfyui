MODELS = {
    "150_16_swin_l_oneformer_coco_100ep.pth": "lllyasviel/Annotators",
    "250_16_swin_l_oneformer_ade20k_160k.pth": "lllyasviel/Annotators",
    "ControlNetHED.pth": "lllyasviel/Annotators",
    "ControlNetLama.pth": "lllyasviel/Annotators",
    "RealESRGAN_x4plus.pth": "lllyasviel/Annotators",
    "ZoeD_M12_N.pt": "lllyasviel/Annotators",
    "body_pose_model.pth": "lllyasviel/Annotators",
    "clip_g.pth": "lllyasviel/Annotators",
    "dpt_hybrid-midas-501f0c75.pt": "lllyasviel/Annotators",
    "erika.pth": "lllyasviel/Annotators",
    "facenet.pth": "lllyasviel/Annotators",
    "hand_pose_model.pth": "lllyasviel/Annotators",
    "lama.ckpt": "lllyasviel/Annotators",
    "latest_net_G.pth": "lllyasviel/Annotators",
    "mlsd_large_512_fp32.pth": "lllyasviel/Annotators",
    "netG.pth": "lllyasviel/Annotators",
    "network-bsds500.pth": "lllyasviel/Annotators",
    "res101.pth": "lllyasviel/Annotators",
    "scannet.pt": "lllyasviel/Annotators",
    "sk_model.pth": "lllyasviel/Annotators",
    "sk_model2.pth": "lllyasviel/Annotators",
    "table5_pidinet.pth": "lllyasviel/Annotators",
    "upernet_global_small.pth": "lllyasviel/Annotators",
    "dw-ll_ucoco_384.onnx": "yzd-v/DWPose",
    "yolox_l.onnx": "yzd-v/DWPose",
    "dw-ll_ucoco_384_bs5.torchscript.pt": "hr16/DWPose-TorchScript-BatchSize5",
    "rtmpose-m_ap10k_256_bs5.torchscript.pt": "hr16/DWPose-TorchScript-BatchSize5",
    "yolo_nas_l_fp16.onnx": "hr16/yolo-nas-fp16",
    "yolo_nas_m_fp16.onnx": "hr16/yolo-nas-fp16",
    "yolo_nas_s_fp16.onnx": "hr16/yolo-nas-fp16",
    "yolox_l.torchscript.pt": "hr16/yolox-onnx",
    "densepose_r50_fpn_dl.torchscript": "LayerNorm/DensePose-TorchScript-with-hint-image",
    "mobile_sam.pt": "dhkim2810/MobileSAM",
    "control_sd15_inpaint_depth_hand_fp16.safetensors": "hr16/ControlNet-HandRefiner-pruned",
    "graphormer_hand_state_dict.bin": "hr16/ControlNet-HandRefiner-pruned",
    "hrnetv2_w64_imagenet_pretrained.pth": "hr16/ControlNet-HandRefiner-pruned",
    "isnetis.ckpt": "skytnt/anime-seg",
}


class ComfyUI_Controlnet_Aux:
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
    def weights_mapping():
        return {"Zoe-DepthMapPreprocessor": "ZoeD_M12_N.pt"}

    @staticmethod
    def add_controlnet_preprocessor_weight(weights_to_download, node):
        if (
            "class_type" in node
            and node["class_type"] in ComfyUI_Controlnet_Aux.weights_mapping()
        ):
            weights_to_download.append(
                ComfyUI_Controlnet_Aux.weights_mapping()[node["class_type"]]
            )
