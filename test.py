import os
from path_utils import module_name_from_file_path, file_path, top_level_package

CODE_ROOT_FOLDER = os.path.join(os.path.dirname(__file__), "source/zeeguu-web/")
_test_path = "src/landingPage/LandingPage.js"
test_path = file_path(CODE_ROOT_FOLDER, _test_path)

def test_file_path():
    assert test_path == os.path.join(os.path.dirname(__file__), "source/zeeguu-web/src/landingPage/LandingPage.js")

def test_module_name_from_file_path():
    assert module_name_from_file_path(CODE_ROOT_FOLDER, test_path) == "src.landingPage.LandingPage"

def test_top_level_package():
    assert (top_level_package("src.landingPage.LandingPage") == "src")
    assert (top_level_package("src.landingPage.LandingPage", 2) == "src.landingPage")

test_file_path()
test_module_name_from_file_path()
test_top_level_package()