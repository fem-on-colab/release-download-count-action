# Copyright (C) 2022-2023 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Script to fetch the download count of each release in a GitHub repository."""

import sys
import typing

import requests


def release_download_count(
    repository_name: str, token: str, per_page: int
) -> typing.Dict[typing.Tuple[str, str], int]:
    """Fetch the download count of each release in a GitHub repository."""
    if token != "":
        headers = {"Authorization": f"token {token}"}
    else:
        headers = None
    # Get all releases and corresponding download count
    page = 1
    count = dict()
    while True:
        response = requests.get(
            f"https://api.github.com/repos/{repository_name}/releases?page={page}&per_page={per_page}",
            headers=headers).json()
        assert isinstance(response, list)
        if len(response) > 0:
            for release in response:
                release_name = release["name"]
                for asset in release["assets"]:
                    asset_name = asset["name"]
                    asset_download_count = asset["download_count"]
                    assert (release_name, asset_name) not in count
                    count[(release_name, asset_name)] = asset_download_count
            page += 1
        else:
            break
    # Return a dictionary containing (release name, release asset): download count
    return count


if __name__ == "__main__":
    assert len(sys.argv) == 4
    release_download_count(sys.argv[1], sys.argv[2], int(sys.argv[3]))
