"""Require the release snapshot to match the workspace rc.1 manifest."""
import argparse
from pathlib import Path

from build_pinned_release import load_manifest


def check_sync(release_path, workspace_path):
    release = load_manifest(release_path)
    workspace = load_manifest(workspace_path)
    # Only this release-specific checkout is exempt, on either side.
    release.pop('governance/.github', None)
    workspace.pop('governance/.github', None)
    differences = []
    for name in sorted(release.keys() | workspace.keys()):
        if name not in release:
            differences.append(f'{name}: missing from release manifest')
        elif name not in workspace:
            differences.append(f'{name}: missing from workspace manifest')
        elif release[name] != workspace[name]:
            differences.append(f'{name}: type, URL or SHA differs')
    if differences:
        raise ValueError('manifest drift:\n' + '\n'.join(differences))
    return len(release)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('release', type=Path)
    parser.add_argument('workspace', type=Path)
    args = parser.parse_args()
    try:
        count = check_sync(args.release, args.workspace)
    except (ValueError, OSError) as error:
        parser.exit(1, f'{error}\n')
    print(f'Matched {count} repositories (governance/.github excepted)')


if __name__ == '__main__':
    main()
