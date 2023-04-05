import unittest
from pathlib import Path

from approvaltests import Options
from approvaltests.approvals import verify

from project.jekyll_to_obsidian_publish import PageConverter, PageRenamer


class ConversionTests(unittest.TestCase):
    def setUp(self) -> None:
        pass
        # set_default_reporter(None)  # Use the first difftool found on your system
        # self.reporter = GenericDiffReporterFactory().get("DiffMerge")
        # Download DiffMerge at https://sourcegear.com/diffmerge/

    def test_page_renamer(self) -> None:
        renamer = PageRenamer()
        assert renamer.get_new_link_file_name('index') == 'Introduction'
        assert renamer.get_new_link_file_name('reference/index') == 'Reference'
        assert renamer.get_new_link_file_name('getting-started/statuses/status-types') == 'Status Types'

    def test_info_conversion(self) -> None:
        content = f'''{{: .info }}
> This is the information
'''
        self.verify_conversion_of_content(content, './README.md')

    def test_full_conversion(self) -> None:
        self.verify_conversion_of_test_file_content('sample_jekyll_document.md', './getting-started/statuses.md')

    def test_sample_front_page(self) -> None:
        self.verify_conversion_of_test_file_content('./sample_front_page.md', './index.md')

    # ------------------------------------------------------------------------------------------------
    # Helper functions
    # ------------------------------------------------------------------------------------------------

    def verify_conversion_of_content(self, content: str, published_filename: str) -> None:
        converter = PageConverter()
        options = Options().for_file.with_extension(".md")
        verify(converter.convert_content(published_filename, content, True), options=options)

    def verify_conversion_of_test_file_content(self, markdown_file_to_read: str, published_filename) -> None:
        input_file = Path(__file__).with_name(markdown_file_to_read)
        with open(input_file) as f:
            content = f.read()
        self.verify_conversion_of_content(content, published_filename)
