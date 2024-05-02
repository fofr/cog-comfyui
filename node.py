class Node:
    @staticmethod
    def is_type(title, node):
        return "class_type" in node and node["class_type"] == title

    @staticmethod
    def is_type_in(node, types):
        return "class_type" in node and node["class_type"] in types

    @staticmethod
    def has_key(node, key):
        return key in node["inputs"]

    @staticmethod
    def value(node, key, default_value=None):
        return node["inputs"][key] if key in node["inputs"] else default_value
