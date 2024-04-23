## 2024-04-23

- Add [ComfyUI-Frame-Interpolation](https://github.com/Fannovel16/ComfyUI-Frame-Interpolation)
- Add [ComfyUI-KJNodes](https://github.com/kijai/ComfyUI-KJNodes)

New AnimateDiff weights for [AnimateLCM](https://huggingface.co/wangfuyun/AnimateLCM):

- AnimateLCM_sd15_t2v.ckpt
- AnimateLCM_sd15_t2v_lora.safetensors

New checkpoint:

- [juggernaut_reborn.safetensors](https://civitai.com/models/46422/juggernaut) (SD15)

## 2024-04-22

- Add [ComfyUI-layerdiffuse](https://github.com/huchenlei/ComfyUI-layerdiffuse) custom node

Add [weights for layerdiffuse](https://huggingface.co/LayerDiffusion/layerdiffusion-v1):

- layer_sd15_bg2fg.safetensors
- layer_sd15_fg2bg.safetensors
- layer_sd15_joint.safetensors
- layer_sd15_transparent_attn.safetensors
- layer_sd15_vae_transparent_decoder.safetensors
- layer_xl_bg2ble.safetensors
- layer_xl_bgble2fg.safetensors
- layer_xl_fg2ble.safetensors
- layer_xl_fgble2bg.safetensors
- layer_xl_transparent_attn.safetensors
- layer_xl_transparent_conv.safetensors
- vae_transparent_decoder.safetensors

## 2024-04-18

Update dependencies:

- IPAdapter plus to support new adapter `ip-adapter-faceid-portrait_sdxl_unnorm.bin` for "extreme profile styles"
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI/compare/6c6a39251fe313c56a88c90d820009073b623dfe...a88b0ebc2d2f933c94e42aa689c42e836eedaf3c)
- AnimateDiff-Evolved
- VideoHelperSuite
- Advanced-ControlNet

## 2024-04-17

- [Update the Impact-Pack custom node](https://github.com/fofr/ComfyUI-Impact-Pack/commit/07a18e7c31ff7489fe7169370b3475a8af41ed4a) to support latest IPAdapter-Plus nodes.
- Add support for [comfyui-tooling-nodes](https://github.com/Acly/comfyui-tooling-nodes) to [add base64 image handling](https://github.com/fofr/cog-comfyui/pull/50)
- Add option to return WebP optimised images from model
- Fix PhotoMaker by using official implementation and updating custom node

AnimateDiff LCM Motion module:

- [animatediffLCMMotion_v10.ckpt](https://civitai.com/models/326698/animatediff-lcm-motion-model)

New models added:

- [rundiffusionXL_beta.safetensors](https://civitai.com/models/120964/rundiffusion-xl)
- [pixlAnimeCartoonComic_v10.safetensors](https://civitai.com/models/260599/pixl-animecartooncomic-style)
- [realisticLCMBYStable_v10.safetensors](https://civitai.com/models/232228?modelVersionId=262126)
- [photonLCM_v10.safetensors](https://civitai.com/models/306814/photon-lcm)

New loras:

- [pk_trainer_xl_v1.safetensors](https://huggingface.co/sWizad/pokemon-trainer-sprite-pixelart)
- [glowneon_xl_v1.safetensors](https://civitai.com/models/310235/glowneon-xl-lora)
- [add-detail-xl.safetensors](https://civitai.com/models/122359/detail-tweaker-xl)
- [aesthetic_anime_v1s.safetensors](https://civitai.com/models/295100/aesthetic-anime-lora)

New embeddings:

- [verybadimagenegative_v1.3.pt](https://civitai.com/models/11772/verybadimagenegative)
- [epiCNegative.pt](https://civitai.com/models/89484?modelVersionId=95256)
- [epiCRealism.pt](https://civitai.com/models/89484?modelVersionId=95263)

## 2024-04-05

- Update ComfyUI [to latest (6c6a392)](https://github.com/comfyanonymous/ComfyUI/commit/6c6a39251fe313c56a88c90d820009073b623dfe)
- Update to latest [IPAdapter Plus (
1ac1cae)](https://github.com/cubiq/ComfyUI_IPAdapter_plus) (breaking changes, custom nodes re-written)

## 2024-03-20

- [CinematicRedmond.safetensors](https://huggingface.co/artificialguybr/CinematicRedmond-SDXL)

New SD1.5 checkpoints for AnimateDiff:

- dynavision_v20Bakedvae.safetensors
- imp_v10.safetensors
- magicmixReverie_v10.safetensors
- majicmixRealistic_v7.safetensors
- rcnzCartoon3d_v20.safetensors
- toonyou_beta6.safetensors

## 2024-03-19

Add [ip_plus_composition_sdxl.safetensors](https://huggingface.co/ostris/ip-composition-adapter) IPAdapter

Add [AnimateDiff lightning weights](https://huggingface.co/ByteDance/AnimateDiff-Lightning):

- animatediff_lightning_1step_comfyui.safetensors
- animatediff_lightning_1step_diffusers.safetensors
- animatediff_lightning_2step_comfyui.safetensors
- animatediff_lightning_2step_diffusers.safetensors
- animatediff_lightning_4step_comfyui.safetensors
- animatediff_lightning_4step_diffusers.safetensors
- animatediff_lightning_8step_comfyui.safetensors
- animatediff_lightning_8step_diffusers.safetensors

## 2024-03-17

Add [ip_plus_composition_sd15.safetensors](https://huggingface.co/ostris/ip-composition-adapter) IPAdapter

## 2024-03-05

Add Juggernaut v9 and lightning:

- Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors
- Juggernaut_RunDiffusionPhoto2_Lightning_4Steps.safetensors

Add Albedobase XL v2.1:

- albedobaseXL_v21.safetensors

## 2024-03-04

Add QR Monster control nets for illusions:

- control_v1p_sd15_qrcode_monster.safetensors
- control_v1p_sdxl_qrcode_monster.safetensors

Add RealVis XL V4 Lightning:

- RealVisXL_V4.0_Lightning.safetensors

## 2024-02-26

- Fix: Always cancel and clear the ComfyUI server queue after a prediction
- Add support for ComfyUI_Comfyroll_CustomNodes
- Correctly download embeddings nested within prompt strings

## 2024-02-22

- Add safetensor SDXL lightning checkpoints, UNETs and Loras

## 2024-02-21

- Add SDXL lightning UNETs and Lora weights

Models added:

- sdxl_lightning_2step_lora.pth
- sdxl_lightning_4step_lora.pth
- sdxl_lightning_8step_lora.pth
- sdxl_lightning_1step_unet_x0.pth
- sdxl_lightning_2step_unet.pth
- sdxl_lightning_4step_unet.pth
- sdxl_lightning_8step_unet.pth
- epicrealismXL_v10.safetensors
- RealVisXL_V4.0.safetensors

## 2024-02-20

- Add support for [WAS nodes](https://github.com/fofr/cog-comfyui/pull/25)
- Add support for [comfyui-segment-anything](https://github.com/storyicon/comfyui_segment_anything)

Models added:

- mobile_sam.pt
- sam_hq_vit_b.pth
- sam_hq_vit_h.pth
- sam_hq_vit_l.pth
- groundingdino_swinb_cogcoor.pth
- groundingdino_swint_ogc.pth
- absolutereality_v181.safetensors
- [PerfectEyesXL Lora](https://civitai.com/models/118427/perfect-eyes-xl)
- [More details Lora](https://civitai.com/models/82098/add-more-details-detail-enhancer-tweaker-lora)
- [FastNegative embedding](https://civitai.com/models/71961/fast-negative-embedding-fastnegativev2)

## 2024-02-17

- Add support for [ComfyUI-Impact-Pack](https://github.com/fofr/cog-comfyui/pull/22)
- Add ViT-H, ViT-L and ViT-B [segment anything models](https://github.com/facebookresearch/segment-anything)
- Update [ComfyUI-AnimateDiff-Evolved](https://github.com/kosinkadink/ComfyUI-AnimateDiff-Evolved) to support Gen2 nodes (Fixes #19)

## 2024-02-14

- Add support for [InstantID](https://github.com/cubiq/ComfyUI_InstantID)
- Add support for [comfyui-reactor-nodes](https://github.com/Gourieff/comfyui-reactor-node)
- Improve support for Insightface in ComfyUI_IPAdapter_plus
- [Fix FaceID lora location](https://github.com/fofr/cog-comfyui/issues/15)

Models added:

- instantid-ipadapter.bin
- instantid-controlnet.safetensors
- antelopev2

## 2024-02-13

- Disable metadata on saved outputs (#14 by @digitaljohn)
- Add support for AIO_Preprocessor on ComfyUI_Controlnet_Aux
- Allow passing of an already parsed JSON workflow (helpful when forking the repo to push new Replicate models)

Models added:

- [copaxTimelessxlSDXL1_v8.safetensors](https://civitai.com/models/118111?modelVersionId=198246)

Loras added:

- [MODILL_XL_0.27_RC.safetensors](https://civitai.com/models/192139/modillxl-modern-colorful-illustration-style-lora)

## 2024-02-09

Models added:

- [artificialguybr](https://huggingface.co/artificialguybr) LoRAs
- [epicrealism_naturalSinRC1VAE.safetensors](https://civitai.com/models/25694/epicrealism)
- [motionctrl_svd.ckpt](https://huggingface.co/TencentARC/MotionCtrl)
- [sdxl_vae.safetensors](https://huggingface.co/stabilityai/sdxl-vae)

Face restoration and detection models:

- codeformer.pth
- GFPGANv1.3.pth
- GFPGANv1.4.pth
- RestoreFormer.pth
- detection_mobilenet0.25_Final.pth
- detection_Resnet50_Final.pth
- parsing_parsenet.pth
- yolov5l-face.pth
- yolov5n-face.pth

## 2024-01-23

Models added:

- [COOLKIDS_MERGE_V2.5.safetensors](https://civitai.com/models/60724/kids-illustration)
- [dreamlabsoil_V2_v2.safetensors](https://civitai.com/models/50718/dreamlabsoilv2)

Custom nodes added:

- https://github.com/BadCafeCode/masquerade-nodes-comfyui 240209b

## 2024-01-22

Models added:

- photomaker-v1.bin
- albedobaseXL_v13.safetensors
- RealESRGAN_x4plus_anime_6B.pth
- 4x_NMKD-Siax_200k.pth
- 4x-UltraSharp.pth
- [Harrlogos_v2.0.safetensors](https://civitai.com/models/176555/harrlogos-xl-finally-custom-text-generation-in-sd)
- starlightXLAnimated_v3.safetensors

Custom nodes added:

- https://github.com/TinyTerra/ComfyUI_tinyterraNodes eda8a09
- https://github.com/ssitu/ComfyUI_UltimateSDUpscale bcefc5b
- https://github.com/cubiq/ComfyUI_essentials c9236fe
- https://github.com/shiimizu/ComfyUI-PhotoMaker 75542a4
- https://github.com/pythongosssss/ComfyUI-Custom-Scripts 9916c13
