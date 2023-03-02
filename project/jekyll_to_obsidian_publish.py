import os.path
import re
from os import walk
from os.path import join


class PageConverter:
    def convert_file(self, source_path: str, destination_path: str) -> None:
        if self.should_skip_file(source_path):
            print(f'    Skipping {source_path}')
            return

        content = self.read_file(source_path)

        # Hide the README.md from Publish, with frontmatter
        if source_path == './README.md':
            content = """---
publish: false
---

""" + content

        content = self.convert_content(content)

        self.write_file(destination_path, content)

    def convert_content(self, content: str) -> str:

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

        replacements = [
            ['{: .info }', '> [!info]'],
            ['{: .released }', '> [!success] Released'],
            ['{: .warning }', '> [!warning]'],
            ['{: .no_toc }\n', ''],
            [table_of_contents_plus_rule, ''],
            [table_of_contents, ''],
        ]
        for replacement in replacements:
            content = content.replace(replacement[0], replacement[1])

        # TODO Convert hyphens in #.... (heading names) to spaces
        p = re.compile(r'\[([^{}]+)]\({{ site\.baseurl }}{% link ([a-z0-9-/]+)\.md %}(#[a-z-]+)?\)')

        lines = content.split('\n')
        for i, line in enumerate(lines):
            lines[i] = p.sub(r'[[\2\3|\1]]', line)

        return '\n'.join(lines)

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
