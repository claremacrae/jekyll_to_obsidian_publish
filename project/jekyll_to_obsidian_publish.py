import re
from os import walk
from os.path import join


def convert_file(file: str, absolute_path: str) -> None:
    if absolute_path == './migration.md':
        print(f'    Skipping {absolute_path}')
        return

    with open(absolute_path) as f:
        content = f.read()

    content = convert_content(content)

    with open(absolute_path, 'w') as f:
        f.write(content)


def convert_content(content: str) -> str:
    replacements = [
        ['{: .info }', '> [!info]'],
        ['{: .released }', '> [!success] Released'],
        ['{: .warning }', '> [!warning]'],
        ['{: .no_toc }\n', ''],
    ]
    for replacement in replacements:
        content = content.replace(replacement[0], replacement[1])

    p = re.compile(r'\[(.*)]\({{ site.baseurl }}{% link ([^ ]+)\.md %}(#[a-z-]+)?\)')
    content = p.sub(r'[[\2\3|\1]]', content)

    return content


def walk_tree(top_directory: str) -> None:
    """
    Walks through the filetree rooted at `root`.
    For each markdown file that it finds, it replaces a particular comment line with the corresponding template.
    Parameters:
        top_directory: path from which this method should run. Generally: root of the hub.
        :param top_directory: ath from which this method should run. Generally the project's documentation folder.
    """

    # Loop through the files
    for root, dirs, files in walk(top_directory, topdown=True):
        # Exclude directories and files
        # dirs[:] = [d for d in dirs if d not in DIRECTORIES_TO_EXCLUDE]
        dirs.sort()
        # files[:] = [f for f in files if f not in FILES_TO_EXCLUDE]
        files.sort()

        # Loop through the files
        for file in files:
            # We only care about markdown files
            # Note: Alternative implementation is to use os.splitext;
            # both work for this usecase
            if file.endswith(".md"):
                absolute_path = join(root, file)
                print(file, absolute_path)
                convert_file(file, absolute_path)


def convert_markdown() -> None:
    walk_tree('.')


if __name__ == '__main__':
    convert_markdown()
