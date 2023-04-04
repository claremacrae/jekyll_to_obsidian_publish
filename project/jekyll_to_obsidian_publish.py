import os.path
import re
import subprocess
from os import walk
from os.path import join
from typing import List, Tuple, Any, Dict

import frontmatter

EXTRACT_JEKYLL_INTERNAL_LINK_REGEXP = re.compile(r'\[([^{}]+)]\({{ site\.baseurl }}{% link ([a-z0-9-/]+)\.md %}(#[a-z-0-9]+)?\)')

StringReplacements = List[List[str]]
MetaData = Dict[str, Any]


class PageRenamer:
    renames = {
        '../docsv2/index.md': '../docsv2/Introduction.md',
        '../docsv2/advanced/api.md': '../docsv2/advanced/Tasks Api.md',
        '../docsv2/advanced/daily-agenda.md': '../docsv2/advanced/Daily Agenda.md',
        '../docsv2/advanced/index.md': '../docsv2/advanced/Advanced.md',
        '../docsv2/advanced/notifications.md': '../docsv2/advanced/Notifications.md',
        '../docsv2/advanced/quickadd.md': '../docsv2/advanced/Quickadd.md',
        '../docsv2/advanced/styling.md': '../docsv2/advanced/Styling.md',
        '../docsv2/advanced/urgency.md': '../docsv2/advanced/Urgency.md',
        '../docsv2/getting-started/auto-suggest.md': '../docsv2/getting-started/Auto-Suggest.md',
        '../docsv2/getting-started/create-or-edit-task.md': '../docsv2/getting-started/Create or edit Task.md',
        '../docsv2/getting-started/dates.md': '../docsv2/getting-started/Dates.md',
        '../docsv2/getting-started/global-filter.md': '../docsv2/getting-started/Global Filter.md',
        '../docsv2/getting-started/index.md': '../docsv2/getting-started/Getting Started.md',
        '../docsv2/getting-started/priority.md': '../docsv2/getting-started/Priority.md',
        '../docsv2/getting-started/recurring-tasks.md': '../docsv2/getting-started/Recurring Tasks.md',
        '../docsv2/getting-started/statuses.md': '../docsv2/getting-started/Statuses.md',
        '../docsv2/getting-started/use-filename-as-default-date.md': '../docsv2/getting-started/Use Filename as Default Date.md',
        '../docsv2/getting-started/statuses/core-statuses.md': '../docsv2/getting-started/statuses/Core Statuses.md',
        '../docsv2/getting-started/statuses/custom-statuses.md': '../docsv2/getting-started/statuses/Custom Statuses.md',
        '../docsv2/getting-started/statuses/editing-a-status.md': '../docsv2/getting-started/statuses/Editing a Status.md',
        '../docsv2/getting-started/statuses/example-statuses.md': '../docsv2/getting-started/statuses/Example Statuses.md',
        '../docsv2/getting-started/statuses/status-settings.md': '../docsv2/getting-started/statuses/Status Settings.md',
        '../docsv2/getting-started/statuses/status-types.md': '../docsv2/getting-started/statuses/Status Types.md',
        '../docsv2/how-to/find-tasks-for-coming-7-days.md': '../docsv2/how-to/Find tasks for coming 7 days.md',
        '../docsv2/how-to/find-tasks-with-invalid-data.md': '../docsv2/how-to/Find tasks with invalid data.md',
        '../docsv2/how-to/get-tasks-in-current-file.md': '../docsv2/how-to/How to get tasks in current file.md',
        '../docsv2/how-to/index.md': '../docsv2/how-to/How Tos.md',
        '../docsv2/how-to/set-up-custom-statuses.md': '../docsv2/how-to/Set up custom statuses.md',
        '../docsv2/how-to/show-tasks-in-calendar.md': '../docsv2/how-to/Show tasks in a calendar.md',
        '../docsv2/how-to/style-backlinks.md': '../docsv2/how-to/How to style backlinks.md',
        '../docsv2/how-to/style-custom-statuses.md': '../docsv2/how-to/Style custom statuses.md',
        '../docsv2/installation/index.md': '../docsv2/installation/Installation.md',
        '../docsv2/other-plugins/dataview.md': '../docsv2/other-plugins/Dataview.md',
        '../docsv2/other-plugins/index.md': '../docsv2/other-plugins/Other Plugins.md',
        '../docsv2/queries/combining-filters.md': '../docsv2/queries/Combining Filters.md',
        '../docsv2/queries/comments.md': '../docsv2/queries/Comments.md',
        '../docsv2/queries/examples.md': '../docsv2/queries/Examples.md',
        '../docsv2/queries/explaining-queries.md': '../docsv2/queries/Explaining Queries.md',
        '../docsv2/queries/filters.md': '../docsv2/queries/Filters.md',
        '../docsv2/queries/grouping.md': '../docsv2/queries/Grouping.md',
        '../docsv2/queries/index.md': '../docsv2/queries/Queries.md',
        '../docsv2/queries/layout.md': '../docsv2/queries/Layout.md',
        '../docsv2/queries/limit.md': '../docsv2/queries/Limiting.md',
        '../docsv2/queries/regular-expressions.md': '../docsv2/queries/Regular Expressions.md',
        '../docsv2/queries/sorting.md': '../docsv2/queries/Sorting.md',
        '../docsv2/quick-reference/index.md': '../docsv2/quick-reference/Quick Reference.md',
        '../docsv2/reference/index.md': '../docsv2/reference/Reference.md',
        '../docsv2/reference/status-collections/anuppuccin-theme.md': '../docsv2/reference/status-collections/AnuPpuccin Theme.md',
        '../docsv2/reference/status-collections/aura-theme.md': '../docsv2/reference/status-collections/Aura Theme (Dark mode only).md',
        '../docsv2/reference/status-collections/ebullientworks-theme.md': '../docsv2/reference/status-collections/Ebullientworks Theme.md',
        '../docsv2/reference/status-collections/index.md': '../docsv2/reference/status-collections/Status Collections.md',
        '../docsv2/reference/status-collections/its-theme.md': '../docsv2/reference/status-collections/ITS Theme.md',
        '../docsv2/reference/status-collections/minimal-theme.md': '../docsv2/reference/status-collections/Minimal Theme.md',
        '../docsv2/reference/status-collections/slrvb-alternate-checkboxes-snippet.md': "../docsv2/reference/status-collections/SlRvb's Alternate Checkboxes.md",
        '../docsv2/reference/status-collections/things-theme.md': '../docsv2/reference/status-collections/Things Theme.md'
    }


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
        updated_line = EXTRACT_JEKYLL_INTERNAL_LINK_REGEXP.sub(r'[[\2\3|\1]]', line)
        return updated_line

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

    def convert(self, decorate: bool = True) -> None:
        """
        Walks through the filetree rooted at `root`.
        For each markdown file that it finds, it replaces a particular comment line with the corresponding template.
        """

        page_converter = PageConverter()
        file_renames: Dict[str, str] = dict()

        for root, dirs, files in walk(self.source, topdown=True):
            # Exclude directories and files
            dirs[:] = [d for d in dirs if d not in ['_site']]
            dirs.sort()
            # files[:] = [f for f in files if f not in FILES_TO_EXCLUDE]
            files.sort()

            for file in files:
                print(file)
                if file.endswith(".md"):
                    source_path = join(root, file)
                    destination_path = join(self.destination, source_path)
                    destination_path = os.path.normpath(destination_path)
                    print(destination_path)

                    # Experiment with renaming file to match title in metadata
                    content = page_converter.read_file(source_path)
                    original_metadata = page_converter.extract_front_matter(content)
                    if 'title' in original_metadata.keys():
                        new_file_name = original_metadata['title'] + '.md'
                        new_path = os.path.join(os.path.split(destination_path)[0], new_file_name)

                        print(new_path)
                        if new_path != destination_path:
                            git_command = f'git mv "{destination_path}" "{new_path}"'
                            file_renames[destination_path] = new_path
                            print(git_command)
                            subprocess.run(git_command, shell=True)
                            print()
                            destination_path = new_path

                    page_converter.convert_file(source_path, destination_path, decorate)
        # The printout of file_renames gets pasted in to PageRenamer
        if file_renames != PageRenamer.renames:
            print(file_renames)
            raise RuntimeError('ERROR - list of filenames in PageRenamer is out of date')

def convert_markdown() -> None:
    site_converter = SiteConverter('.', '../docsv2')
    site_converter.convert()

    # Activate this to update the snippet file(s):
    # site_converter = SiteConverter('../docs-snippets', '../docs-snippets2')
    # site_converter.convert(False)


if __name__ == '__main__':
    convert_markdown()
