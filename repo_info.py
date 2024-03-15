from argparse import ArgumentParser
from pathlib import Path
from typing import cast

from pygit2 import discover_repository, Repository, Commit, GIT_SORT_REVERSE, Index, IndexEntry


def main():
    args = _parse_arg()
    _show_content(args.path)


def _parse_arg():
    parser = ArgumentParser()
    parser.add_argument('path', type=Path)

    return parser.parse_args()


def _show_content(repository_path: Path):
    if not repository_path.is_dir():
        raise RuntimeError(f"Directory {repository_path} doesn't exist")

    rep = Repository(discover_repository(str(repository_path)))
    print('Head', rep.head.name)

    print('Commits:')
    for num, git_obj in enumerate(rep.walk(rep.head.target, GIT_SORT_REVERSE)):
        git_commit = cast(Commit, git_obj)
        print(f'\tCommit №{num}:', git_commit.message.strip())

    last_commit = cast(Commit, rep[rep.head.target])

    index = Index()
    index.read_tree(last_commit.tree)

    print('Files:')
    for git_obj in index:
        entry = cast(IndexEntry, git_obj)
        print('\t', entry.id.hex, entry.path)
        print('\t\tContent:', rep[entry.id].data)


if __name__ == "__main__":
    main()
