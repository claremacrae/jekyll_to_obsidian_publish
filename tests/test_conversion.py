import unittest
from pathlib import Path

from approvaltests import Options
from approvaltests.approvals import verify

from project.jekyll_to_obsidian_publish import PageConverter


class ConversionTests(unittest.TestCase):
    def setUp(self) -> None:
        pass
        # set_default_reporter(None)  # Use the first difftool found on your system
        # self.reporter = GenericDiffReporterFactory().get("DiffMerge")
        # Download DiffMerge at https://sourcegear.com/diffmerge/

    def test_info_conversion(self) -> None:
        converter = PageConverter()

        input = f'''{{: .info }}
> This is the information
'''
        options = Options().for_file.with_extension(".md")
        verify(converter.convert_content('./README.md', input), options=options)

    def test_full_conversion(self) -> None:
        filename = 'sample_jekyll_document.md'
        self.verify_conversion_of_test_file_content(filename)

    # ------------------------------------------------------------------------------------------------
    # Helper functions
    # ------------------------------------------------------------------------------------------------

    def verify_conversion_of_content(self, content: str, filename: str) -> None:
        converter = PageConverter()
        options = Options().for_file.with_extension(".md")
        verify(converter.convert_content(filename, content), options=options)

    def verify_conversion_of_test_file_content(self, filename: str) -> None:
        input_file = Path(__file__).with_name(filename)
        with open(input_file) as f:
            content = f.read()
        self.verify_conversion_of_content(content, filename)
