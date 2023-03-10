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
        content = self.convert_tables_with_blank_lines(content)
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
        p = re.compile(r'\[([^{}]+)]\({{ site\.baseurl }}{% link ([a-z0-9-/]+)\.md %}(#[a-z-]+)?\)')

        lines = content.split('\n')
        for i, line in enumerate(lines):
            lines[i] = p.sub(r'[[\2\3|\1]]', line)

        return '\n'.join(lines)

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
        danger =  '''
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
