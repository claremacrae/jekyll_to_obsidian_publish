import os.path
import re
from os import walk
from os.path import join
from typing import List, Tuple, Any, Dict

import frontmatter

StringReplacements = List[List[str]]
MetaData = Dict[str, Any]


class PageConverter:
    def convert_file(self, source_path: str, destination_path: str) -> None:
        if self.should_skip_file(source_path):
            print(f'    Skipping {source_path}')
            return

        content = self.read_file(source_path)
        content = self.convert_content(source_path, content)
        self.write_file(destination_path, content)

    def convert_content(self, source_path: str, content: str) -> str:
        original_metadata = self.extract_front_matter(content)
        content = self.update_front_matter(content, source_path)
        content = self.convert_tables_of_contents(content)
        content = self.convert_callouts(content)
        content = self.convert_internal_links(content)

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
        replacements: StringReplacements = [
            ['{: .info }', '> [!info]'],
            ['{: .released }', '> [!success] Released'],
            ['{: .warning }', '> [!warning]'],
            ['<div class="code-example" markdown="1">\n', ''],
            ['</div>\n', ''],
        ]
        return self.apply_replacements(content, replacements)

    def convert_internal_links(self, content: str) -> str:
        # TODO Convert hyphens in #.... (heading names) to spaces
        p = re.compile(r'\[([^{}]+)]\({{ site\.baseurl }}{% link ([a-z0-9-/]+)\.md %}(#[a-z-]+)?\)')

        lines = content.split('\n')
        for i, line in enumerate(lines):
            lines[i] = p.sub(r'[[\2\3|\1]]', line)

        return '\n'.join(lines)

    def apply_replacements(self, content: str, replacements: StringReplacements) -> str:
        for replacement in replacements:
            content = content.replace(replacement[0], replacement[1])
        return content

    def should_skip_file(self, source_path: str) -> bool:
        return source_path == './migration.md'

    def read_file(self, source_path: str) -> str:
        with open(source_path) as f:
            content = f.read()
        return content

    def write_file(self, destination_path: str, content: str) -> None:
        from pathlib import Path
        Path(os.path.dirname(destination_path)).mkdir(parents=True, exist_ok=True)
        with open(destination_path, 'w') as f:
            f.write(content)


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

    def convert(self) -> None:
        """
        Walks through the filetree rooted at `root`.
        For each markdown file that it finds, it replaces a particular comment line with the corresponding template.
        """

        page_converter = PageConverter()

        for root, dirs, files in walk(self.source, topdown=True):
            # Exclude directories and files
            dirs[:] = [d for d in dirs if d not in ['_site']]
            dirs.sort()
            # files[:] = [f for f in files if f not in FILES_TO_EXCLUDE]
            files.sort()

            for file in files:
                if file.endswith(".md"):
                    source_path = join(root, file)
                    destination_path = join(self.destination, source_path)
                    destination_path = os.path.normpath(destination_path)
                    print(destination_path)
                    page_converter.convert_file(source_path, destination_path)


def convert_markdown() -> None:
    site_converter = SiteConverter('.', '../docsv2')
    site_converter.convert()


if __name__ == '__main__':
    convert_markdown()
