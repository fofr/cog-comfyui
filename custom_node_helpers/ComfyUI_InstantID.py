from custom_node_helper import CustomNodeHelper


class ComfyUI_InstantID(CustomNodeHelper):
    @staticmethod
    def add_weights(weights_to_download, node):
        if node.is_type("InstantIDFaceAnalysis"):
            weights_to_download.append("models/antelopev2")
        elif (
            node.is_type("InstantIDModelLoader")
            and node.input("instantid_file") == "ipadapter.bin"
        ):
            node.set_input("instantid_file", "instantid-ip-adapter.bin")
            weights_to_download.append("instantid-ip-adapter.bin")
        elif node.is_type("ControlNetLoader"):
            if (
                node.input("control_net_name")
                == "instantid/diffusion_pytorch_model.safetensors"
            ):
                node.set_input("control_net_name", "instantid-controlnet.safetensors")
                weights_to_download.append("instantid-controlnet.safetensors")
