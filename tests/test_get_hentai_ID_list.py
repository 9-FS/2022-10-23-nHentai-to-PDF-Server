# Copyright (c) 2023 구FS, all rights reserved. Subject to the MIT licence in `licence.md`.
import datetime as dt
import dropbox
import hypothesis, hypothesis.strategies
import json
from KFSdropbox import KFSdropbox
import os
import sys

sys.path.append("./")   # enables importing via parent directory
from src.get_hentai_ID_list import get_hentai_ID_list


@hypothesis.settings(deadline=dt.timedelta(seconds=500), max_examples=10)
@hypothesis.given(hypothesis.strategies.lists(hypothesis.strategies.integers()).filter(lambda downloadme_content: 0<len(downloadme_content)))   #generate random downloadme.txt containing numbers, do not trigger downloads from nhentai.net, can't independently verify that anyways and takes too long
def test_get_hentai_ID_list(downloadme_content: list[int]) -> None:
    cookies: dict[str, str]                 # for requests.get to bypass bot protection
    dbx: dropbox.Dropbox                    # dropbox instance
    dropbox_config: dict[str, str]          # dropbox_dest_path
    hentai_ID_list: list[int]               # hentai ID list to download
    hentai_ID_in_dropbox_list: list[int]    # hentai ID list of already downloaded hentai
    headers: dict[str, str]                 # for requests.get to bypass bot protection


    with open("./cookies.json", "rt") as cookies_file:                      # load cookies to bypass bot protection
        cookies=json.loads(cookies_file.read())
    with open("./dropbox_API_cred.json", "rt") as dropbox_API_cred_file:    # load cookies to bypass bot protection
        dropbox_API_cred=json.loads(dropbox_API_cred_file.read())
    with open("./dropbox_config.json", "rt") as dropbox_config_file:        # load cookies to bypass bot protection
        dropbox_config=json.loads(dropbox_config_file.read())
    with open("./headers.json", "rt") as headers_file:                      # load headers to bypass bot protection
        headers=json.loads(headers_file.read())
    dbx=dropbox.Dropbox(oauth2_refresh_token=dropbox_API_cred["refresh_token"], app_key=dropbox_API_cred["app_key"], app_secret=dropbox_API_cred["app_secret"]) # create Dropbox instance
    
    with open("./downloadme.txt", "wt", errors="ignore") as downloadme_file:            # save random downloadme.txt containing numbers (valid) and strings (invalid)
        downloadme_file.write("\n".join([str(line) for line in downloadme_content]))    # list[int|str] -> list[str] -> std, write to file

    hentai_ID_list=get_hentai_ID_list(cookies, headers, dbx, dropbox_config)    # get hentai ID list from random downloadme.txt, load from downloadme.txt first, then if that is completely invalid and discarded correctly, use correct user input
    

    assert 0<len(hentai_ID_list)                    # check that hentai ID list is not empty

    for hentai_ID in hentai_ID_list:                # check that hentai ID list does not contain duplicates
        assert hentai_ID_list.count(hentai_ID)==1

    assert sorted(hentai_ID_list)==hentai_ID_list   # check that hentai ID list is sorted

    for hentai_ID in hentai_ID_list:                # check that hentai ID list only contains integers
        assert isinstance(hentai_ID, int)

    hentai_ID_in_dropbox_list=[int(os.path.splitext(hentai_filename)[0].split(" ")[0]) for hentai_filename in KFSdropbox.list_files(dbx, dropbox_config["dropbox_dest_path"])]  # download list of already downloaded hentai, convert filename to ID only
    for hentai_ID_in_dropbox in hentai_ID_in_dropbox_list:
        assert hentai_ID_in_dropbox not in hentai_ID_list                                                                                                                       # check that hentai ID list does not contain already downloaded hentai
    
    for line in downloadme_content: # check that hentai ID list contains all valid integers from random downloadme.txt that are not already downloaded
        try:
            int(line)
        except ValueError:
            continue
        
        if int(line) not in hentai_ID_in_dropbox_list:
            assert int(line) in hentai_ID_list

    return