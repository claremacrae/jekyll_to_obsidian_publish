import os.path
import unittest
from pathlib import Path

from approvaltests import Options
from approvaltests.approvals import verify

from project.jekyll_to_obsidian_publish import PageConverter, PageRenamer


class PageRenamerTests(unittest.TestCase):
    def test_renames(self) -> None:
        renames = PageRenamer.renames
        print(type(renames))
        for key in renames.keys():
            print(type(key), key)

    def test_link_renamer(self) -> None:
        renamer = PageRenamer()
        assert renamer.get_new_link_file_name('index') == 'Introduction'
        assert renamer.get_new_link_file_name('reference/index') == 'Reference'
        assert renamer.get_new_link_file_name('getting-started/statuses/status-types') == 'Status Types'

    def test_page_renamer(self) -> None:
        def test_get_new_disk_file_name(destination: str, expected: str) -> None:
            assert (PageRenamer.get_new_disk_file_name(destination)) == expected

        test_get_new_disk_file_name('README.md', 'README.md')
        test_get_new_disk_file_name('other-plugins/dataview.md', 'other-plugins/Dataview.md')
        test_get_new_disk_file_name('reference/status-collections/aura-theme.md',
                                    'reference/status-collections/Aura Theme.md')

    def test_old_directory_listing(self) -> None:
        expected_directories = [
            '',
            'advanced',
            'getting-started',
            'getting-started/statuses',
            'how-to',
            'installation',
            'other-plugins',
            'queries',
            'quick-reference',
            'reference',
            'reference/status-collections']
        directories = PageRenamer().get_all_old_directory_names()
        assert directories == expected_directories

    def test_directory_new_name(self) -> None:
        assert PageRenamer.get_new_directory_name('') == ''
        assert PageRenamer.get_new_directory_name('advanced') == 'Advanced'
        assert PageRenamer.get_new_directory_name('getting-started') == 'Getting Started'
        assert PageRenamer.get_new_directory_name('getting-started/statuses') == 'Getting Started/Statuses'
        assert PageRenamer.get_new_directory_name('reference') == 'Reference'
        assert PageRenamer.get_new_directory_name('reference/status-collections') == 'Reference/Status Collections'

class PageConverterTests(unittest.TestCase):
    def setUp(self) -> None:
        pass
        # set_default_reporter(None)  # Use the first difftool found on your system
        # self.reporter = GenericDiffReporterFactory().get("DiffMerge")
        # Download DiffMerge at https://sourcegear.com/diffmerge/

    def test_info_conversion(self) -> None:
        content = f'''{{: .info }}
> This is the information
'''
        self.verify_conversion_of_content(content, './README.md')

    def test_full_conversion(self) -> None:
        self.verify_conversion_of_test_file_content('sample_jekyll_document.md', './getting-started/statuses.md')

    def test_sample_front_page(self) -> None:
        self.verify_conversion_of_test_file_content('./sample_front_page.md', './index.md')

    def test_adding_redirect(self) -> None:
        renamer = PageRenamer()
        assert renamer.get_new_url(
            'getting-started/recurring-tasks.md') == 'https://publish.obsidian.md/tasks/Getting+Started/Recurring+Tasks'

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


class SiteConverterTests(unittest.TestCase):
    pass
    # def test_add_links_to_new_site(self):
