import json
import os.path
import re
import subprocess
import sys
from os import walk
from os.path import join
from typing import List, Any, Dict, Sequence
import argparse

import frontmatter

FILE_NAMES_MARKDOWN_FILE = os.path.join(os.path.dirname(__file__), 'markdown_files.json')

EXTRACT_JEKYLL_INTERNAL_LINK_REGEXP = re.compile(
    r'\[([^{}]+)]\({{ site\.baseurl }}{% link ([a-z0-9-/]+)\.md %}(#[a-z-0-9]+)?\)')

StringReplacements = List[List[str]]
MetaData = Dict[str, Any]


class PageRenamer:
    with open(FILE_NAMES_MARKDOWN_FILE) as f:
        renames = json.load(f)

    def get_new_link_file_name(self, path_without_file_extension: str) -> str:
        """
        This converts a filename in a link
        :param path_without_file_extension: 
        :return: 
        """
        old_path = f'../docsv2/{path_without_file_extension}.md'
        new_path = PageRenamer.renames[old_path]
        return os.path.basename(new_path).replace('.md', '')

    @classmethod
    def get_new_disk_file_name(cls, destination_path: str) -> str:
        """
        This converts a filename on disk
        :param destination_path: 
        :return: 
        """
        if destination_path in PageRenamer.renames:
            return PageRenamer.renames[destination_path]
        else:
            # For cases like README.md with no TITLE in the file, so not saved in PageRenamer
            return destination_path


class PageConverter:
    def convert_file(self, source_path: str, destination_path: str, decorate: bool) -> None:
        if self.should_skip_file(source_path):
            print(f'    Skipping {source_path}')
            return

        content = self.read_file(source_path)
        content = self.convert_content(source_path, content, decorate)
        self.write_file(destination_path, content)

    def convert_content(self, source_path: str, content: str, decorate: bool) -> str:
        if decorate:
            content = self.update_front_matter(content, source_path)
        content = self.convert_tables_of_contents(content)
        content = self.convert_callouts(content)
        content = self.convert_internal_links(content)
        content = self.convert_tables_with_blank_lines(content)
        if decorate:
            content = self.add_danger_message_if_default_page(content, source_path)
            content = self.add_link_to_this_page_on_old_site(content, source_path)

        return content

    def extract_front_matter(self, content: str) -> MetaData:
        metadata = frontmatter.loads(content)
        return metadata.to_dict()

    def update_front_matter(self, content: str, source_path: str) -> str:
        metadata = frontmatter.loads(content)

        unwanted_keys = [
            'grand_parent',
            'has_children',
            'has_toc',
            'layout',
            'nav_order',
            'parent',
            'title',
        ]
        for key in unwanted_keys:
            if key in metadata:
                metadata.__delitem__(key)

        if source_path == './README.md':
            # Hide the README.md from Publish, with frontmatter.
            metadata['publish'] = False
        else:
            # Make sure Publish picks up all other files.
            metadata['publish'] = True

        # Reinstate original end-of-line that frontmatter removes
        return frontmatter.dumps(metadata) + '\n'

    def convert_tables_of_contents(self, content: str) -> str:
        table_of_contents = """
<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>
"""
        table_of_contents_plus_rule = f'''
{table_of_contents}
---'''
        replacements: StringReplacements = [
            ['{: .no_toc }\n', ''],
            [table_of_contents_plus_rule, ''],
            [table_of_contents, ''],
        ]
        content = self.apply_replacements(content, replacements)
        return content

    def convert_callouts(self, content: str) -> str:
        content = self.convert_one_old_callout(content, 'Warning', 'yellow', 'warning')
        content = self.convert_one_old_callout(content, 'Important', 'yellow', 'important')
        content = self.convert_one_old_callout(content, 'Info', 'blue', 'info')

        replacements: StringReplacements = [
            ['{: .info }', '> [!info]'],
            ['{: .released }', '> [!quote] Released'],
            ['{: .warning }', '> [!warning]'],
            ['<div class="code-example" markdown="1">\n', ''],
            ['</div>\n', ''],
            ['<hr />\n', ''],
        ]
        return self.apply_replacements(content, replacements)

    def convert_one_old_callout(self, content: str, old_title: str, old_color: str, new_callout_type: str) -> str:
        replacement = f'> [!{new_callout_type}]\n> '
        brace1 = '{'
        brace2 = '}'
        replacements: StringReplacements = [
            [f'{old_title}\n{brace1}: .label .label-{old_color}{brace2}\n\n', replacement],
            [f'{old_title}\n{brace1}: .label .label-{old_color} {brace2}\n\n', replacement],
            [f'{old_title}\n{brace1}: .label .label-{old_color}{brace2}\n', replacement],
            [f'{old_title}\n{brace1}: .label .label-{old_color} {brace2}\n', replacement],
        ]
        return self.apply_replacements(content, replacements)

    def convert_internal_links(self, content: str) -> str:
        # TODO Convert hyphens in #.... (heading names) to spaces
        lines = content.split('\n')
        for i, line in enumerate(lines):
            updated_line = self.convert_all_internal_links_in_line(line)
            lines[i] = updated_line

        return '\n'.join(lines)

    def convert_all_internal_links_in_line(self, line: str) -> str:
        matches = EXTRACT_JEKYLL_INTERNAL_LINK_REGEXP.findall(line)
        for link_text, path_without_file_extension, anchor_or_empty in matches:
            line = line.replace(self.old_link_line(anchor_or_empty, link_text, path_without_file_extension),
                                self.new_link_line(anchor_or_empty, link_text, path_without_file_extension))
        return line

    def old_link_line(self, anchor_or_empty: str, link_text: str, path_without_file_extension: str) -> str:
        whole_link_including_brackets = ''.join(
            [
                '[',
                link_text,
                ']({{ site.baseurl }}{% link ' + \
                path_without_file_extension,
                '.md %}',
                anchor_or_empty,
                ')',
            ]
        )
        return whole_link_including_brackets

    def new_link_line(self, anchor_or_empty: str, link_text: str, path_without_file_extension: str) -> str:
        renamer = PageRenamer()
        new_path_without_file_extension = renamer.get_new_link_file_name(path_without_file_extension)
        path_and_anchor = f'{new_path_without_file_extension}{anchor_or_empty}'
        if path_and_anchor == link_text:
            # No need to give custom display text, if it matches the file name, and we are not linking to a heading
            new_link_including_brackets = f'[[{link_text}]]'
        else:
            new_link_including_brackets = f'[[{path_and_anchor}|{link_text}]]'
        return new_link_including_brackets

    def convert_tables_with_blank_lines(self, content: str) -> str:
        # Fix the table in Urgency.md by removing blank lines:
        tr_afore = '''  </tr>\n\n  <tr>'''
        tr_after = '''  </tr>\n  <tr>'''
        replacements: StringReplacements = [
            [tr_afore, tr_after],
        ]
        return self.apply_replacements(content, replacements)

    def apply_replacements(self, content: str, replacements: StringReplacements) -> str:
        for replacement in replacements:
            content = content.replace(replacement[0], replacement[1])
        return content

    def should_skip_file(self, source_path: str) -> bool:
        return source_path == './migration.md'

    def add_danger_message_if_default_page(self, content: str, source_path: str) -> str:
        if source_path != './index.md':
            return content

        heading_to_modify = '# Introduction\n'
        danger = '''
> [!Danger] About this site
> This is an experimental conversion of the Tasks user docs to Obsidian Publish, tracked in [#1706](https://github.com/obsidian-tasks-group/obsidian-tasks/issues/1706).
>
> This site - [publish.obsidian.md/tasks](https://publish.obsidian.md/tasks/queries/sorting) - is now well-tested, and you are welcome to stay here and use the site. The content is the same as on the original site.
>
> Every page here has a 'View this page on the old documentation site' section at the bottom, making it easy to compare the old and new sites side-by-side, and to report any problems you find.
>
> You can read more about progress on this conversion, including known problems and remaining steps, at the [[migration|Migration to Publish]] page.
>
> Alternatively, you can visit the [original documentation site](https://obsidian-tasks-group.github.io/obsidian-tasks/) instead.
'''
        replacements: StringReplacements = [
            [heading_to_modify, heading_to_modify + danger]
        ]
        return self.apply_replacements(content, replacements)

    def read_file(self, source_path: str) -> str:
        with open(source_path) as f:
            content = f.read()
        return content

    def write_file(self, destination_path: str, content: str) -> None:
        from pathlib import Path
        Path(os.path.dirname(destination_path)).mkdir(parents=True, exist_ok=True)
        with open(destination_path, 'w') as f:
            f.write(content)

    def add_link_to_this_page_on_old_site(self, content: str, source_path: str) -> str:
        if source_path == './README.md':
            return content

        relative_path = source_path
        relative_path = relative_path.replace('./', '')
        relative_path = relative_path.replace('index.md', '')
        relative_path = relative_path.replace('.md', '/')
        old_url = f'https://obsidian-tasks-group.github.io/obsidian-tasks/{relative_path}'
        return content + f'''
---

## View this page on the old documentation site

> [!Info] Request for feedback
> This page is an experimental migration of the Tasks user docs to Obsidian Publish. When the conversion is good enough, this will become the live site.
>
> For comparison, you can view [this page on the old documentation site]({old_url}).

> [!Bug] Please report any problems
>
> We are keeping a list of [[migration#Current Status and Known Problems|Known Problems]] with the conversion.
>
> If you notice any other problems in this page, compared to [the old one]({old_url}), please let us know in [#1706](https://github.com/obsidian-tasks-group/obsidian-tasks/issues/1706#issuecomment-1454284835).
>
> Please include:
>
> - The URL of this problem page
> - A screenshot of the problem.
>
> Thank you!
'''


class SiteConverter:
    def __init__(self, source: str, destination: str) -> None:
        """
        Class to copy a directory of markdown Jekyll docs, and output a directory for use with Obsidian Publish.
        Parameters:
            top_directory: path from which this method should run. Generally: root of the hub.
            :param source: path from which this method should run. Generally the project's documentation folder.
            :param destination: output path, where the converted files are saved to.
        """
        self.source = source
        self.destination = destination

    def convert(self, decorate: bool = True) -> None:
        """
        Walks through the filetree rooted at `root`.
        For each markdown file that it finds, it replaces a particular comment line with the corresponding template.
        """

        page_converter = PageConverter()

        for root, dirs, files in walk(self.source, topdown=True):
            self.filter_tree_args(dirs, files)

            for file in files:
                print(file)
                if file.endswith(".md"):
                    source_path = self.get_source_path(root, file)
                    destination_path = self.get_destination_path(source_path)

                    destination_path = self.rename_file_based_on_saved_filenames(destination_path)

                    page_converter.convert_file(source_path, destination_path, decorate)

    def rename_file_based_on_saved_filenames(self, destination_path: str) -> str:
        new_path = PageRenamer.get_new_disk_file_name(destination_path)

        print(new_path)
        if new_path != destination_path:
            destination_path = self.git_rename_file(destination_path, new_path)
        return destination_path

    def git_rename_file(self, destination_path: str, new_path: str) -> str:
        git_command = f'git mv "{destination_path}" "{new_path}"'
        print(git_command)
        subprocess.run(git_command, shell=True)
        print()
        destination_path = new_path
        return destination_path

    def create_json_files_list(self) -> None:
        """
        Walks through the filetree rooted at `root`.
        Saves a JSON file of the old and new file names
        """

        page_converter = PageConverter()
        file_renames: Dict[str, str] = dict()

        for root, dirs, files in walk(self.source, topdown=True):
            self.filter_tree_args(dirs, files)

            for file in files:
                print(file)
                if file.endswith(".md"):
                    source_path = self.get_source_path(root, file)
                    destination_path = self.get_destination_path(source_path)

                    # Experiment with renaming file to match title in metadata
                    content = page_converter.read_file(source_path)
                    original_metadata = page_converter.extract_front_matter(content)
                    new_path = destination_path
                    if 'title' in original_metadata.keys():
                        new_file_name = original_metadata['title'] + '.md'
                        new_path = os.path.join(os.path.split(destination_path)[0], new_file_name)

                    print(new_path)
                    file_renames[destination_path] = new_path
        # Save file_renames
        with open(FILE_NAMES_MARKDOWN_FILE, 'w') as f:
            f.write(json.dumps(file_renames, indent=4))

    def get_source_path(self, root: str, file: str) -> str:
        source_path = join(root, file)
        return source_path

    def get_destination_path(self, source_path: str) -> str:
        destination_path = join(self.destination, source_path)
        destination_path = os.path.normpath(destination_path)
        print(destination_path)
        return destination_path

    def filter_tree_args(self, dirs: List[str], files: List[str]) -> None:
        # Exclude directories and files
        dirs[:] = [d for d in dirs if d not in ['_site']]
        dirs.sort()
        # files[:] = [f for f in files if f not in FILES_TO_EXCLUDE]
        files.sort()

    def rename_files(self) -> None:
        """
        Rename files from Jekyll convention to new one for Obsidian Public
        """

        for root, dirs, files in walk(self.source, topdown=True):
            self.filter_tree_args(dirs, files)

            for file in files:
                print(file)
                if file.endswith(".md"):
                    source_path = self.get_source_path(root, file)
                    destination_path = self.get_destination_path(source_path)
                    self.rename_file_based_on_saved_filenames(destination_path)



def convert_markdown() -> None:
    site_converter = SiteConverter('.', '../docsv2')
    site_converter.convert()

    # Activate this to update the snippet file(s):
    # site_converter = SiteConverter('../docs-snippets', '../docs-snippets2')
    # site_converter.convert(False)


def main(argv: Sequence[str]) -> None:
    parser = argparse.ArgumentParser(
        description="Convert Tasks plugin docs from Jekyll to Obsidian Publish"
    )
    parser.add_argument(
        "--save-files-list", action="store_true",
        help="Generate a JSON file containing all the original Markdown docs files."
    )
    parser.add_argument(
        "--rename-files", action="store_true",
        help="Rename markdown files from Jekyll file names to their titles"
    )
    args = parser.parse_args(argv)

    site_converter = SiteConverter('.', '../docsv2')
    if args.save_files_list:
        site_converter.create_json_files_list()
    elif args.rename_files:
        site_converter.rename_files()
    else:
        convert_markdown()


if __name__ == '__main__':
    main(sys.argv[1:])
