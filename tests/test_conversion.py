import unittest
from pathlib import Path

from approvaltests import Options
from approvaltests.approvals import verify

from project.jekyll_to_obsidian_publish import convert_content


class ConversionTests(unittest.TestCase):
    def setUp(self) -> None:
        pass
        # set_default_reporter(None)  # Use the first difftool found on your system
        # self.reporter = GenericDiffReporterFactory().get("DiffMerge")
        # Download DiffMerge at https://sourcegear.com/diffmerge/

    def test_info_conversion(self) -> None:
        input = f'''{{: .info }}
> This is the information
'''
        options = Options().for_file.with_extension(".md")
        verify(convert_content(input), options=options)

    def test_full_conversion(self) -> None:
        input_file = Path(__file__).with_name('sample_jekyll_document.md')
        with open(input_file) as f:
            content = f.read()
        options = Options().for_file.with_extension(".md")
        verify(convert_content(content), options=options)
