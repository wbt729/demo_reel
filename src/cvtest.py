# import sys
# import imp

# cv2_package_path = '/home/georg/gles/projekte/eigene/jetson/work/opencv_install/lib/python3.11/site-packages/cv2/'
# cv2_package_name = "cv2"
# sys.path.append(cv2_package_path)
# cv2 = imp.load_source(cv2_package_name, cv2_package_path, '/__init__.py')

# print(cv2.getBuildInformation())

# import types
# import importlib.machinery

# from importlib import import_module

fn = '/home/georg/gles/projekte/eigene/jetson/work/opencv_install/lib/python3-11/site-packages/cv2/__init__.py' # without .py

import importlib
import sys

# spec = importlib.util.spec_from_file_location(module_name, file_path)
module_name = "cv2"
spec = importlib.util.spec_from_file_location(module_name, fn)
cv2 = importlib.util.module_from_spec(spec)
sys.modules[module_name] = cv2
spec.loader.exec_module(cv2)

print(cv2.getBuildInformation())