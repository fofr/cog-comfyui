## 2024-07-18

- [Update ComfyUI](https://github.com/comfyanonymous/ComfyUI/compare/29c2e26724d4982a3e33114eb9064f1a11f4f4ed..374e093e09c94b528d7c9dfc337c65cc5c433ee3)
- Add Kolors native support
- Add Kolors IPAdapter support

Weights:

- [kolors.fp16.safetensors](https://huggingface.co/Kwai-Kolors/Kolors/blob/main/unet/diffusion_pytorch_model.fp16.safetensors)
- [Kolors-IP-Adapter-Plus.bin](https://huggingface.co/Kwai-Kolors/Kolors-IP-Adapter-Plus)
- [clip-vit-large-patch14-336.bin](https://huggingface.co/Kwai-Kolors/Kolors-IP-Adapter-Plus/blob/main/image_encoder/pytorch_model.bin)

## 2024-07-17

- Update [ComfyUI-Impact-Pack](https://github.com/fofr/ComfyUI-Impact-Pack/compare/07a18e7..9ad8f85)

New controlnets:

- [controlnet-depth-sdxl-1.0.safetensors](https://huggingface.co/xinsir/controlnet-depth-sdxl-1.0)
- [controlnet-union-sdxl-1.0.safetensors](https://huggingface.co/xinsir/controlnet-union-sdxl-1.0)
- [TTPLANET_Controlnet_Tile_realistic_v2_rank256.safetensors](https://huggingface.co/TTPlanet/TTPLanet_SDXL_Controlnet_Tile_Realistic)

New checkpoints:

- Stable Cascade (checkpoint, unet and vae)
- [PixArt-Sigma-XL-2-1024-MS.pth](https://huggingface.co/PixArt-alpha/PixArt-Sigma/tree/main)

Add more ultralytics detectors:

- bbox/face_yolov8n.pt
- bbox/face_yolov8n.pt
- bbox/face_yolov8n_v2.pt
- bbox/face_yolov8s.pt
- bbox/hand_yolov8n.pt
- segm/deepfashion2_yolov8s-seg.pt
- segm/face_yolov8m-seg_60.pt
- segm/face_yolov8n-seg2_60.pt
- segm/hair_yolov8n-seg_60.pt
- segm/hair_yolov8n-seg_60.pt
- segm/person_yolov8n-seg.pt
- segm/person_yolov8s-seg.pt
- segm/skin_yolov8m-seg_400.pt
- segm/skin_yolov8n-seg_400.pt
- segm/skin_yolov8n-seg_800.pt

## 2024-07-16

Fixes:

- Allow duplicate URLs within workflow ([fixes #120](https://github.com/fofr/cog-comfyui/issues/120))

New checkpoints:

- [Realistic_Vision_V4.0.safetensors](https://huggingface.co/SG161222/Realistic_Vision_V4.0_noVAE)
- [Realistic_Vision_V4.0-inpainting.safetensors](https://huggingface.co/SG161222/Realistic_Vision_V4.0_noVAE)

New loras:

- [hd_helper_v1.safetensors](https://civitai.com/models/110071/hd-helper) an SD15 helper for larger images
- [Polaroidv2.safetensors](https://civitai.com/models/243554?modelVersionId=356493) (SDXL)

## 2024-07-15

- [Update ComfyUI](https://github.com/comfyanonymous/ComfyUI/compare/2f03201690e0fb8a3ec551a125b20d89c9019a02...29c2e26724d4982a3e33114eb9064f1a11f4f4ed)
- Add [ComfyMath](https://github.com/evanspearman/ComfyMath) custom nodes
- Add [SUPIR](https://github.com/kijai/ComfyUI-SUPIR) custom nodes
- Add KJ's [IC Light](https://github.com/kijai/ComfyUI-IC-Light) custom nodes
- Add [StyleAligned](https://github.com/brianfitzgerald/style_aligned_comfy) custom nodes
- Add [AttentionCouple](https://github.com/laksjdjf/attention-couple-ComfyUI) custom nodes
- TensorRT engines added for SD3 on A40, A100 and H100
- ComfyUI enums helper added for easy access to schedulers and samplers
- Update [ReActor](https://github.com/Gourieff/comfyui-reactor-node/compare/51ae8f6...bcfd45c) to latest

New weights:

- [aura_flow_0.1.safetensors](https://huggingface.co/fal/AuraFlow)
- [Kolors diffusers model](https://huggingface.co/Kwai-Kolors/Kolors) and LLMs:
  - chatglm3-4bit.safetensors
  - chatglm3-8bit.safetensors
  - chatglm3-fp16.safetensors

SUPIR weights:

- SUPIR-v0F.ckpt
- SUPIR-v0F_fp16.safetensors
- SUPIR-v0Q.ckpt
- SUPIR-v0Q_fp16.safetensors

LivePortrait weights:

- appearance_feature_extractor.safetensors
- landmark.onnx
- motion_extractor.safetensors
- spade_generator.safetensors
- stitching_retargeting_module.safetensors
- warping_module.safetensors

FaceRestore weights:

- GPEN-BFR-1024.onnx
- GPEN-BFR-2048.onnx
- GPEN-BFR-512.onnx

Lora:

- [charTurnBetaLora.safetensors](https://civitai.com/models/7252/charturnerbeta-lora-experimental)

## 2024-07-02

- Update ComfyUI
- Update [ComfyUI_IPAdapter_plus](https://github.com/cubiq/ComfyUI_IPAdapter_plus/compare/2ff4fc4...8208e27)
- Update [ComfyUI-AnimateDiff-Evolved](https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved/compare/e2313c4...832e832)
- Update [ComfyUI-Advanced-ControlNet](https://github.com/Kosinkadink/ComfyUI-Advanced-ControlNet/compare/f6adc32...7a456aa) (not backwards compatible)
- Update [ComfyUI-VideoHelperSuite](https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite/compare/08dc3d6...0037f49)
- Update [comfyui-prompter-fofrai](https://github.com/fofr/comfyui-prompter-fofrai/compare/26c4a21...3243a26)

New weights:

- [ponyDiffusionV6XL_v6StartWithThisOne.safetensors](https://huggingface.co/LyliaEngine/Pony_Diffusion_V6_XL)
- [SD3-Controlnet-Canny.safetensors](https://huggingface.co/InstantX/SD3-Controlnet-Canny)
- [SD3-Controlnet-Pose.safetensors](https://huggingface.co/InstantX/SD3-Controlnet-Pose)
- [SD3-Controlnet-Tile.safetensors](https://huggingface.co/InstantX/SD3-Controlnet-Tile)
- [controlnet-tile-sdxl-1.0.safetensors](https://huggingface.co/xinsir/controlnet-tile-sdxl-1.0/tree/main)

## 2024-06-24

- Add [comfyui-prompter-fofrai](https://github.com/fofr/comfyui-prompter-fofrai) custom node

### Add your own weights

Visit the `train` tab on Replicate to create a new version of this model with your own weights:

https://replicate.com/fofr/any-comfyui-workflow/train

Here you can give public or private URLs to weights on HuggingFace and CivitAI. If URLs are private or need authentication, make sure to include an API key or access token.

Check the training logs to see what filenames to use in your workflow JSON. For example:

```
Downloading from HuggingFace:
...
Size of the tar file: 217.88 MB
====================================
When using your new model, use these filenames in your JSON workflow:
araminta_k_midsommar_cartoon.safetensors
```

## 2024-06-15

Add SD3 weights and CLIP weights:

- sd3_medium.safetensors
- sd3_medium_incl_clips.safetensors
- sd3_medium_incl_clips_t5xxlfp16.safetensors
- sd3_medium_incl_clips_t5xxlfp8.safetensors
- clip_g.safetensors
- clip_l.safetensors
- t5xxl_fp16.safetensors

## 2024-06-11

[Updated ComfyUI](https://github.com/comfyanonymous/ComfyUI/compare/eecd69b53a896343775bcb02a4f8349e7442ffd1...a82fae2) to latest. Includes SD3 nodes.

Updated ComfyUI custom nodes:

- [ComfyUI_IPAdapter_plus](https://github.com/cubiq/ComfyUI_IPAdapter_plus/compare/d33265a...7d8adae)
- [ComfyUI-Inspire-Pack](https://github.com/ltdrdata/ComfyUI-Inspire-Pack/compare/0916454...9b2d22a)
- [comfyui-tooling-nodes](https://github.com/Acly/comfyui-tooling-nodes/compare/294d366...2f39365)
- [ComfyUI-AnimateDiff-Evolved](https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved/compare/eba6a50...e2313c4)
- [ComfyUI-VideoHelperSuite](https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite/compare/acbf789...08dc3d6)
- [ComfyUI-Advanced-ControlNet](https://github.com/Kosinkadink/ComfyUI-Advanced-ControlNet/compare/6788448...f6adc32)
- [efficiency-nodes-comfyui](https://github.com/jags111/efficiency-nodes-comfyui/compare/97f284b...a5422d6)
- [Derfuu_ComfyUI_ModdedNodes](https://github.com/Derfuu/Derfuu_ComfyUI_ModdedNodes/compare/2ace4c4...5c93bd1)
- [ComfyUI_FizzNodes](https://github.com/FizzleDorf/ComfyUI_FizzNodes/compare/ebf7fbf...3db5b71)
- [ComfyUI_tinyterraNodes](https://github.com/TinyTerra/ComfyUI_tinyterraNodes/compare/8d8bb56...732d417)
- [ComfyUI-Custom-Scripts](https://github.com/pythongosssss/ComfyUI-Custom-Scripts/compare/9916c13...edc5321)
- [masquerade-nodes-comfyui](https://github.com/BadCafeCode/masquerade-nodes-comfyui/compare/240209b...69a9449)
- [comfyui-reactor-node](https://github.com/Gourieff/comfyui-reactor-node/compare/ae81f62...51ae8f6)
- [was-node-suite-comfyui](https://github.com/WASasquatch/was-node-suite-comfyui/compare/33534f2...72290fc)
- [comfyui_segment_anything](https://github.com/fofr/comfyui_segment_anything/compare/8bc6178...2916eb3)
- [ComfyUI-BRIA_AI-RMBG](https://github.com/ZHO-ZHO-ZHO/ComfyUI-BRIA_AI-RMBG/compare/44a3f8f...827fcd6)
- [ComfyUI-layerdiffuse](https://github.com/huchenlei/ComfyUI-layerdiffuse/compare/151f746...4b421cf)
- [ComfyUI-KJNodes](https://github.com/kijai/ComfyUI-KJNodes/compare/5430564...cdd507d)
- [PuLID_ComfyUI](https://github.com/cubiq/PuLID_ComfyUI/compare/45f7709...145a5ef)
- [comfyui_jankhidiffusion](https://github.com/blepping/comfyui_jankhidiffusion/compare/e54ff4d...6111b81)
- [ComfyUI-Anyline](https://github.com/TheMistoAI/ComfyUI-Anyline/compare/d84ba37...2f35c98)
- [rgthree-comfy](https://github.com/rgthree/rgthree-comfy/compare/23fddb8...ab0a59a)

New checkpoints:

- [animagine-xl-3.0.safetensors](https://civitai.com/models/260267?modelVersionId=293564)

[Add araminta_k’s new loras](https://huggingface.co/alvdansen), most use "daiton style" as keyword:

- araminta_k/abstract-anime-painting.safetensors,
- araminta_k/araminta-k-illustration.safetensors,
- araminta_k/BandW-Manga.safetensors,
- araminta_k/gemini-anime.safetensors,
- araminta_k/haute-couture-illustration.safetensors,
- araminta_k/japanese-poster-prints.safetensors,
- araminta_k/lost-and-lonely-manga.safetensors,
- araminta_k/painting-light.safetensors,
- araminta_k/pop-art-anime.safetensors,
- araminta_k/sketched-out-manga.safetensors,
- araminta_k/soft-ones.safetensors,
- araminta_k/soft-pastel-anime.safetensors,
- araminta_k/vincent-sketch-manga.safetensors

Other new loras:

- [RW_PS1v1.safetensors](https://civitai.com/models/55613/ps1-graphics-rw) (PS1 SD15 lora, "ps1 style")
- [artificialguybr/3DRedmond15V-LiberteRedmond-3DRenderStyle-3DRenderAF.safetensors](https://huggingface.co/artificialguybr/3d-redmond-1-5v-3d-render-style-for-liberte-redmond-sd-1-5) ("3D Render Style, 3DRenderAF")

## 2024-06-03

New checkpoints:

- [EpicrealismXL_Hades.safetensors](https://civitai.com/models/354130?modelVersionId=534487)
- [epicrealismXL_v7FinalDestination.safetensors](https://civitai.com/models/277058/epicrealism-xl)

New embedding:

- [realisticvision-negative-embedding.pt](https://civitai.com/models/36070/negative-embedding-for-realistic-vision-v20)

Models for ToonCrafter:

- CLIP-ViT-H-fp16.safetensors
- stable-diffusion-2-1-clip-fp16.safetensors
- stable-diffusion-2-1-clip.safetensors
- [tooncrafter_512_interp-fp16.safetensors](https://huggingface.co/Kijai/DynamiCrafter_pruned/tree/main)

New detailer:

- [bbox/Eyes.pt](https://civitai.com/models/150925/eyes-detection-adetailer)

Update KJNodes to latest:

- [KJNodes](https://github.com/kijai/ComfyUI-KJNodes/compare/48d5a18...5430564)

## 2024-05-30

- Refactor repo to make it easier to use as a template
- Added guide in `MAKING_A_MODEL_GUIDE.md`

New SDXL control nets:

- [controlnet-openpose-sdxl-1.0.safetensors](https://huggingface.co/xinsir/controlnet-openpose-sdxl-1.0)
- [controlnet-openpose-sdxl-1.0_twins.safetensors](https://huggingface.co/xinsir/controlnet-openpose-sdxl-1.0)
- [controlnet-scribble-sdxl-1.0.safetensors](https://huggingface.co/xinsir/controlnet-scribble-sdxl-1.0)
- [controlnet-canny-sdxl-1.0.safetensors](https://huggingface.co/xinsir/controlnet-canny-sdxl-1.0)
- [controlnet-canny-sdxl-1.0_V2.safetensors](https://huggingface.co/xinsir/controlnet-canny-sdxl-1.0)

## 2024-05-24

[Update comfyui_controlnet_aux](https://github.com/Fannovel16/comfyui_controlnet_aux/compare/692a3d0...8e51eb3) to include support for:

- Anyline
- Metric3D
- TTPlanet Tile

[Update ComfyUI-AnimateDiff-Evolved to latest](https://github.com/kosinkadink/ComfyUI-AnimateDiff-Evolved/commit/f9e0343...eba6a50) and add support for:

- CameraCtrl ([CameraCtrl_pruned.safetensors](https://huggingface.co/Kosinkadink/CameraCtrl/tree/main))

Update custom nodes:

- [ComfyUI_InstantID to fix PuLID compatibility](https://github.com/cubiq/ComfyUI_InstantID/commit/d8c70a0cd8ce0d4d62e78653674320c9c3084ec1)
- [ComfyUI-Frame-Interpolation](https://github.com/Fannovel16/ComfyUI-Frame-Interpolation/compare/5e11679...1c4c4b4)
- [PuLID_ComfyUI](https://github.com/cubiq/PuLID_ComfyUI/compare/b88e5aa...45f7709)
- [ComfyUI-VideoHelperSuite](https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite/compare/5b5026c...acbf789)
- [ComfyUI-Advanced-ControlNet](https://github.com/Kosinkadink/ComfyUI-Advanced-ControlNet/compare/fbf005f...6788448)
- [efficiency-nodes-comfyui](https://github.com/jags111/efficiency-nodes-comfyui/compare/3b7e89d...97f284b)
- [ComfyUI_FizzNodes](https://github.com/FizzleDorf/ComfyUI_FizzNodes/compare/cd6cadd...ebf7fbf)
- [ComfyUI_UltimateSDUpscale](https://github.com/ssitu/ComfyUI_UltimateSDUpscale/compare/bcefc5b...233f8b8)
- [ComfyUI_essentials](https://github.com/cubiq/ComfyUI_essentials/compare/101ebae...94b7450)
- [ComfyUI-Inspire-Pack](https://github.com/cubiq/ComfyUI_Inspire_Pack/compare/c8231dd...0916454)

Add support for [GLIGEN weights](https://huggingface.co/comfyanonymous/GLIGEN_pruned_safetensors/tree/main):

- gligen_sd14_textbox_pruned.safetensors
- gligen_sd14_textbox_pruned_fp16.safetensors

## 2024-05-21

Add support for custom nodes:

- [rgthree-comfy](https://github.com/rgthree/rgthree-comfy)
- [ComfyUI-Anyline](https://github.com/TheMistoAI/ComfyUI-Anyline)

New models:

- [crystalClearXL_ccxl.safetensors](https://civitai.com/models/122822/crystal-clear-xl)
- Anyline preprocessor [MTEED.pth](https://huggingface.co/TheMistoAI/MistoLine/tree/main/Anyline)

## 2024-05-15

Add support for HiDiffusion via [comfyui_jankhidiffusion](https://github.com/blepping/comfyui_jankhidiffusion)

## 2024-05-13

Add support for [ComfyUI-IC-Light-Native](https://github.com/huchenlei/ComfyUI-IC-Light-Native)

New [UNets for IC Light](https://huggingface.co/huchenlei/IC-Light-ldm/tree/main):

- iclight_sd15_fbc_unet_ldm.safetensors
- iclight_sd15_fc_unet_ldm.safetensors

## 2024-05-10

New checkpoints:

- [leosamsHelloworldXL_helloworldXL60.safetensors](https://civitai.com/models/43977/leosams-helloworld-xl)
- [copaxCuteXLSDXL10_v4.safetensors](https://civitai.com/models/119226)

Added [MistoLine lineart controlnets](https://huggingface.co/TheMistoAI/MistoLine/tree/main):

- mistoLine_fp16.safetensors
- mistoLine_rank256.safetensors

## 2024-05-08

Add [PuLID-ComfyUI](https://github.com/cubiq/PuLID_ComfyUI) custom node support

New checkpoints:

- [jibMixRealisticXL_v10Lightning46Step.safetensors](https://civitai.com/models/194768?modelVersionId=395827)

## 2024-05-07

New checkpoints:

- [sdxlUnstableDiffusers_nihilmania.safetensors](https://civitai.com/models/84040?modelVersionId=395107)
- [sdxlUnstableDiffusers_v11Rundiffusion.safetensors](https://civitai.com/models/84040?modelVersionId=309729)

## 2024-05-03

- Adding support for [rembg](https://github.com/danielgatis/rembg), used in a variety of custom nodes
- Update ComfyUI_tinyterraNodes to latest to fix rembg issue

## 2024-05-01

Update [ComfyUI Controlnet Aux](https://github.com/Fannovel16/comfyui_controlnet_aux/tree/692a3d0)

New controlnets:

- [depth-anything.safetensors](https://huggingface.co/spaces/LiheYoung/Depth-Anything/blob/main/checkpoints_controlnet/diffusion_pytorch_model.safetensors)

New controlnet preprocessors:

- [Diffusion-Edge](https://huggingface.co/hr16/Diffusion-Edge) ([Paper](https://github.com/GuHuangAI/DiffusionEdge))
- [Depth-Anything](https://huggingface.co/spaces/LiheYoung/Depth-Anything/tree/main/checkpoints) and [Zoe Depth-Anything](https://huggingface.co/spaces/LiheYoung/Depth-Anything/tree/main/checkpoints_metric_depth)
- [Unimatch](https://huggingface.co/hr16/Unimatch) optical flow estimation
- [TEED](https://huggingface.co/bdsqlsz/qinglong_controlnet-lllite/blob/main/Annotators/7_model.pth)

## 2024-04-30

- Update ComfyUI to latest ([eecd69b](https://github.com/comfyanonymous/ComfyUI/commit/eecd69b53a896343775bcb02a4f8349e7442ffd1))

New checkpoint:

- [juggernautXL_juggernautX.safetensors](https://civitai.com/models/133005?modelVersionId=456194)

## 2024-04-26

Add [Hyper-SD Lora and UNet weights](https://huggingface.co/ByteDance/Hyper-SD):

- Hyper-SD15-1step-lora.safetensors
- Hyper-SD15-2steps-lora.safetensors
- Hyper-SD15-4steps-lora.safetensors
- Hyper-SD15-8steps-lora.safetensors
- Hyper-SDXL-1step-lora.safetensors
- Hyper-SDXL-2steps-lora.safetensors
- Hyper-SDXL-4steps-lora.safetensors
- Hyper-SDXL-8steps-lora.safetensors
- Hyper-SDXL-1step-Unet-Comfyui.fp16.safetensors
- Hyper-SDXL-1step-Unet.safetensors

## 2024-04-25

Update [ComfyUI_Essentials to latest](https://github.com/cubiq/ComfyUI_essentials/commit/101ebaef8df8b0c7f55a810c8394e3276b0487e1) as requested in [#71](https://github.com/fofr/cog-comfyui/issues/71)

New SD15 loras and embeddings as requested in [#72](https://github.com/fofr/cog-comfyui/issues/72):

- [age_slider-LECO-v1.safetensors](https://civitai.com/models/179792/age-slider)
- [weight_slider-LECO-v1.safetensors](https://civitai.com/models/180008?modelVersionId=202032)
- [SDXLrender_v2.0.safetensors](https://civitai.com/models/171159?modelVersionId=236130)
- [JuggernautNegative-neg.pt](https://civitai.com/models/81563/juggernaut-negative-embedding)

Also added ultralytics model [hair_yolov8n-seg_60.pt](https://github.com/hben35096/assets/releases/tag/yolo8)

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
