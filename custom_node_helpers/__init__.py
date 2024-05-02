import os
import sys
import importlib

current_dir = os.path.dirname(os.path.abspath(__file__))
for file in os.listdir(current_dir):
    if file.endswith(".py") and not file.startswith("__"):
        module_name = file[:-3]
        module = importlib.import_module(f".{module_name}", package=__name__)
        class_name = module_name
        setattr(sys.modules[__name__], class_name, getattr(module, class_name))
