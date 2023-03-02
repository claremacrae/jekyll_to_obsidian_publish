import unittest
# import pytest

from approvaltests.approvals import verify, verify_all

# from approvaltests.reporters.python_native_reporter import PythonNativeReporter
from approvaltests import Options, verify_as_json
# from approvaltests.reporters.generic_diff_reporter_factory import GenericDiffReporterFactory
# from approvaltests import set_default_reporter


class ConversionTests(unittest.TestCase):
    def setUp(self) -> None:
        pass
        # set_default_reporter(None)  # Use the first difftool found on your system
        # self.reporter = GenericDiffReporterFactory().get("DiffMerge")
        # Download DiffMerge at https://sourcegear.com/diffmerge/

    def test_(self) -> None:
        self.assertEqual(5, 5)

    def test_info_conversion(self) -> None:
        from project.jekyll_to_obsidian_publish import convert_content
        input = f'''{{: .info }}
> This is the information
'''
        options = Options().for_file.with_extension(".md")
        verify(convert_content(input), options = options)


# def test_pytest() -> None:
#     assert True
