class Node:
    def __init__(self, node):
        self.node = node

    def type(self):
        return self.node["class_type"]

    def is_type(self, type):
        return "class_type" in self.node and self.node["class_type"] == type

    def is_type_in(self, types):
        return "class_type" in self.node and self.node["class_type"] in types

    def has_input(self, key):
        return key in self.node["inputs"]

    def input(self, key, default_value=None):
        return self.node["inputs"][key] if key in self.node["inputs"] else default_value

    def set_input(self, key, value):
        self.node["inputs"][key] = value

    def raise_if_unsupported(self, unsupported_nodes={}):
        if self.is_type_in(unsupported_nodes):
            raise ValueError(f"{self.type()} node is not supported: {unsupported_nodes[self.type()]}")
