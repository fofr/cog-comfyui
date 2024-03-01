MODELS = [
    "bdsqlsz_controlllite_xl_canny.safetensors",
    "bdsqlsz_controlllite_xl_depth.safetensors",
    "bdsqlsz_controlllite_xl_dw_openpose.safetensors",
    "bdsqlsz_controlllite_xl_lineart_anime_denoise.safetensors",
    "bdsqlsz_controlllite_xl_mlsd_V2.safetensors",
    "bdsqlsz_controlllite_xl_normal.safetensors",
    "bdsqlsz_controlllite_xl_recolor_luminance.safetensors",
    "bdsqlsz_controlllite_xl_segment_animeface.safetensors",
    "bdsqlsz_controlllite_xl_segment_animeface_V2.safetensors",
    "bdsqlsz_controlllite_xl_sketch.safetensors",
    "bdsqlsz_controlllite_xl_softedge.safetensors",
    "bdsqlsz_controlllite_xl_t2i-adapter_color_shuffle.safetensors",
    "bdsqlsz_controlllite_xl_tile_anime_α.safetensors",
    "bdsqlsz_controlllite_xl_tile_anime_β.safetensors",
    "bdsqlsz_controlllite_xl_tile_realistic.safetensors",
]

class ComfyUI_Controlnet_Lllite:
    @staticmethod
    def models():
        return MODELS

    @staticmethod
    def weights_map(base_url):
        return {
            model: {
                "url": f"{base_url}/custom_nodes/ControlNet-LLLite-ComfyUI/{model}.tar",
                "dest": "ComfyUI/custom_nodes/ControlNet-LLLite-ComfyUI/models",
            }
            for model in MODELS
        }
