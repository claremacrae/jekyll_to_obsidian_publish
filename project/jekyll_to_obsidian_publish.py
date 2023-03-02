import os.path
import re
from os import walk
from os.path import join


def convert_file(source_path: str, destination_path: str) -> None:
    if source_path == './migration.md':
        print(f'    Skipping {source_path}')
        return

    with open(source_path) as f:
        content = f.read()

    # Hide the README.md from Publish, with frontmatter
    if source_path == './README.md':
        content = """---
publish: false
---

""" + content

    content = convert_content(content)

    from pathlib import Path
    Path(os.path.dirname(destination_path)).mkdir(parents=True, exist_ok=True)
    with open(destination_path, 'w') as f:
        f.write(content)


def convert_content(content: str) -> str:

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


class SiteConverter:
    def __init__(self, source: str, destination: str) -> None:
        self.source = source
        self.destination = destination

    def convert(self) -> None:
        """
        Walks through the filetree rooted at `root`.
        For each markdown file that it finds, it replaces a particular comment line with the corresponding template.
        Parameters:
            top_directory: path from which this method should run. Generally: root of the hub.
            :param source: path from which this method should run. Generally the project's documentation folder.
            :param destination: output path, where the converted files are saved to. 
        """

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
                    convert_file(source_path, destination_path)

def convert_markdown() -> None:
    site_converter = SiteConverter('.', '../docsv2')
    site_converter.convert()


if __name__ == '__main__':
    convert_markdown()
