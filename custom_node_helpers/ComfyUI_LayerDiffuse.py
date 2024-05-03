from custom_node_helper import CustomNodeHelper


class ComfyUI_LayerDiffuse(CustomNodeHelper):
    @staticmethod
    def get_config_weights(config):
        config_weights_map = {
            "SDXL, Attention Injection": ["layer_xl_transparent_attn.safetensors"],
            "SDXL, Conv Injection": ["layer_xl_transparent_conv.safetensors"],
            "SD15, Attention Injection, attn_sharing": [
                "layer_sd15_transparent_attn.safetensors"
            ],
            "SDXL, Foreground": ["layer_xl_fg2ble.safetensors"],
            "SDXL, Background": ["layer_xl_bg2ble.safetensors"],
            "Diff, SDXL, Foreground": ["layer_xl_fgble2bg.safetensors"],
            "Diff, SDXL, Background": ["layer_xl_bgble2fg.safetensors"],
            "SD15, attn_sharing, Batch size (3N)": ["layer_sd15_joint.safetensors"],
            "SD15, Foreground, attn_sharing, Batch size (2N)": [
                "layer_sd15_fg2bg.safetensors"
            ],
            "SD15, Background, attn_sharing, Batch size (2N)": [
                "layer_sd15_bg2fg.safetensors"
            ],
        }
        return config_weights_map.get(config, [])

    @staticmethod
    def get_vae_weights(config):
        vae_weights_map = {
            "SD15": ["layer_sd15_vae_transparent_decoder.safetensors"],
            "SDXL": ["vae_transparent_decoder.safetensors"],
        }

        return vae_weights_map.get(config, [])

    @staticmethod
    def add_weights(weights_to_download, node):
        if node.is_type_in(
            [
                "LayeredDiffusionApply",
                "LayeredDiffusionJointApply",
                "LayeredDiffusionCondApply",
                "LayeredDiffusionCondJointApply",
            ]
        ):
            config = node.input("config")
            weights_to_download.extend(ComfyUI_LayerDiffuse.get_config_weights(config))
        elif node.is_type(
            "LayeredDiffusionDiffApply",
        ):
            config = f"Diff, {node.input('config')}"
            weights_to_download.extend(ComfyUI_LayerDiffuse.get_config_weights(config))
        elif node.is_type_in(
            [
                "LayeredDiffusionDecode",
                "LayeredDiffusionDecodeRGBA",
                "LayeredDiffusionDecodeSplit",
            ]
        ):
            sd_version = node.input("sd_version")
            weights_to_download.extend(ComfyUI_LayerDiffuse.get_vae_weights(sd_version))
