# Copyright (c) 2023 구FS, all rights reserved. Subject to the MIT licence in `licence.md`.
import datetime as dt
import hypothesis, hypothesis.strategies
import json
import os
import sys

sys.path.append("./")   # enables importing via parent directory
from src.get_hentai_ID_list import get_hentai_ID_list


@hypothesis.given(hypothesis.strategies.lists(hypothesis.strategies.integers()).filter(lambda downloadme_content: 0<len(downloadme_content)))   #generate random downloadme.txt containing numbers, do not trigger downloads from nhentai.net, can't independently verify that anyways and takes too long
def test_get_hentai_ID_list(downloadme_content: list[int]) -> None:
    cookies: dict[str, str]                 # for requests.get to bypass bot protection
    headers: dict[str, str]                 # for requests.get to bypass bot protection
    hentai_ID_list: list[int]               # hentai ID list to download


    with open("./cookies.json", "rt") as cookies_file:      # load cookies to bypass bot protection
        cookies=json.loads(cookies_file.read())
    with open("./headers.json", "rt") as headers_file:      # load headers to bypass bot protection
        headers=json.loads(headers_file.read())
    with open("./settings.json", "rt") as settings_file:    # load settings
        settings=json.loads(settings_file.read())
    
    with open("./downloadme.txt", "wt", errors="ignore") as downloadme_file:            # save random downloadme.txt containing numbers (valid) and strings (invalid)
        downloadme_file.write("\n".join([str(line) for line in downloadme_content]))    # list[int|str] -> list[str] -> str, write to file

    hentai_ID_list=get_hentai_ID_list(cookies, headers, settings["nhentai_tag"])    # get hentai ID list from random downloadme.txt, load from downloadme.txt first, then if that is completely invalid and discarded correctly, use correct user input
    

    assert 0<len(hentai_ID_list)                    # check that hentai ID list is not empty

    for hentai_ID in hentai_ID_list:                # check that hentai ID list does not contain duplicates
        assert hentai_ID_list.count(hentai_ID)==1

    assert sorted(hentai_ID_list)==hentai_ID_list   # check that hentai ID list is sorted

    for hentai_ID in hentai_ID_list:                # check that hentai ID list only contains integers
        assert isinstance(hentai_ID, int)

    for line in downloadme_content: # check that hentai ID list contains all valid integers from random downloadme.txt that are not already downloaded
        try:
            int(line)
        except ValueError:
            continue
        else:
            assert int(line) in hentai_ID_list

    return