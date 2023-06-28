
def from_path():
    print("import cv2 from path")
    import imp
    import sys,os
    cv2_package_path = '/home/dipak/opencv_inst/lib/python3.8/site-packages/cv2'
    cv2_package_name = "cv2"
    sys.path.append(cv2_package_path)
    cv2 = imp.load_source(cv2_package_name, cv2_package_path + '/__init__.py')
    return cv2