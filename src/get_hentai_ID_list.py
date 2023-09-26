# Copyright (c) 2023 구FS, all rights reserved. Subject to the MIT licence in `licence.md`.
import concurrent.futures
import dropbox
import inspect
import json
from KFSdropbox import KFSdropbox
from KFSfstr    import KFSfstr
import requests
import time
import logging
import os


def get_hentai_ID_list(cookies: dict[str, str], headers: dict[str, str], dbx: dropbox.Dropbox, dropbox_config: dict[str, str]) -> list[int]:
    """
    Tries to return hentai ID list to download by trying to load "./downloadme.txt" or by searching on nhentai.net for all hentai ID with tag dropbox_config["tag"].

    Arguments:
    - cookies: cookies to send with the request to bypass bot protection
    - headers: user agent to send with the request to bypass bot protection
    - dbx: dropbox instance
    - dropbox_config: dropbox configuration

    Returns:
    - hentai_ID_list: list of hentai ID to download
    """

    file_tried: bool=False                  # tried to load from file?
    hentai_ID_in_dropbox_list: list[str]    # list of hentai ID already downloaded and in dropbox, don't redownload these
    hentai_ID_list: list[int]=[]            # hentai ID list
    hentai_ID_list_str: list[str]


    while True:
        if os.path.isfile("./downloadme.txt")==True and file_tried==False:                                  # if ID list in file and not tried to load from file yet: load from file, only try once
            file_tried=True
            with open("downloadme.txt", "rt") as downloadme_file:
                hentai_ID_list_str=downloadme_file.readlines()                                              # read all lines from file
        else:                                                                                               # if ID list file not available: ask user for input
            hentai_ID_list_str=_get_hentai_ID_list_from_tag_search(cookies, headers, dbx, dropbox_config)   # get hentai ID list by searching by tag
        
        hentai_ID_list_str=[hentai_ID for hentai_ID in hentai_ID_list_str if len(hentai_ID)!=0] # remove empty inputs
        if len(hentai_ID_list_str)==0:                                                          # if file or user input empty: retry
            continue

        logging.info("Removing already downloaded ID...")
        hentai_ID_in_dropbox_list=[os.path.splitext(hentai_filename)[0].split(" ")[0] for hentai_filename in KFSdropbox.list_files(dbx, dropbox_config["dropbox_dest_path"])]   # download list of already downloaded hentai, convert filename to ID only
        hentai_ID_list_str=[hentai_ID for hentai_ID in hentai_ID_list_str if hentai_ID not in hentai_ID_in_dropbox_list]                                                        # filter out already downloaded ID, do this in any case also if list loaded from downloadme.txt
        logging.info("Removed already downloaded ID.")

        for hentai_ID in hentai_ID_list_str:    # convert all hentai ID to int
            try:
                hentai_ID_list.append(int(hentai_ID))
            except ValueError:                  # if input invalid: discard whole input, ask user (again)
                logging.error(f"Converting input \"{hentai_ID}\" to int failed.")
                break
        else:                                   # if all ID converted without failure: break out of while, return desired ID
            break
    
    return hentai_ID_list


def _get_hentai_ID_list_from_tag_search(cookies: dict[str, str], headers: dict[str, str], dbx: dropbox.Dropbox, dropbox_config: dict[str, str]) -> list[str]:
    """
    Tries to return hentai ID list to download by searching on nhentai.net for all hentai ID with tag dropbox_config["tag"].

    Arguments:
    - cookies: cookies to send with the request to bypass bot protection
    - headers: user agent to send with the request to bypass bot protection
    - dbx: dropbox instance
    - dropbox_config: dropbox configuration

    Returns:
    - hentai_ID_list_str: list of hentai ID to download
    """

    hentai_ID_list_str: list[str]=[]        # list of hentai ID to download
    hentai_ID_new: list[str]
    NHENTAI_SEARCH_API_URL: str="https://nhentai.net/api/galleries/search"
    page_no_current: int=1
    page_no_max: int                        # number of pages a nhentai search by tag would return


    search_request=requests.Request("GET", NHENTAI_SEARCH_API_URL, cookies=cookies, headers=headers, params={"query": dropbox_config["tag"], "sort": "popular", "page": 1}).prepare()   # prepare beforehand to generate full URL from params
    page_no_max=_get_page_no_max_by_tag(search_request)    
    logging.debug(f"Searching by tag\"{dropbox_config['tag']}\" results in {KFSfstr.notation_abs(page_no_max, 0, round_static=True)} number of pages.")                                 # get page_no_max by searching by tag
    

    logging.info("")
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as thread_manager:
        search_requests=[requests.Request("GET", NHENTAI_SEARCH_API_URL, cookies=cookies, headers=headers, params={"query": dropbox_config["tag"], "sort": "popular", "page": page_no}).prepare() for page_no in range(1, page_no_max+1)]   # prepare beforehand to generate full URL from params
        for hentai_ID_new in thread_manager.map(_search_hentai_ID_by_tag, search_requests):                                                                                                                                                 # search by tag on all pages
            hentai_ID_list_str+=hentai_ID_new
            logging.info(f"\rDownloaded hentai ID from \"{search_requests[page_no_current-1].url}\", page {KFSfstr.notation_abs(page_no_current, 0, round_static=True)}/{KFSfstr.notation_abs(page_no_max, 0, round_static=True)}.") 
            logging.debug(hentai_ID_new)
            logging.debug("")
            page_no_current+=1


    hentai_ID_list_str=list(dict.fromkeys(hentai_ID_list_str))  # remove duplicates
    hentai_ID_list_str.sort()                                   # sort

    logging.info("Saving hentai ID list in \"downloadme.txt\"...")  # save as backup in case something crashes, normal nHentai to PDF downloader could pick up if needed
    with open("downloadme.txt", "wt") as h_ID_list_file:
        h_ID_list_file.write("\n".join([str(hentai_ID) for hentai_ID in hentai_ID_list_str]))
    logging.info("\rSaved hentai ID list in \"downloadme.txt\".")

    return hentai_ID_list_str


def _get_page_no_max_by_tag(search_request: requests.PreparedRequest) -> int:
    """
    Gets the number of pages a nhentai search by tag would return.

    Arguments:
    - search_request: prepared request to nhentai search API

    Returns:
    - page_no_max: number of pages a nhentai search by tag would return

    Raises:
    - requests.HTTPError: Downloading tag search from \"{search_request.url}\" failed multiple times.
    """

    page_no_max: int
    search: dict
    search_page: requests.Response


    attempt_no: int=1
    while True:
        try:
            search_page=requests.Session().send(search_request, timeout=10)
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):  # if connection error: try again
            time.sleep(1)
            if attempt_no<3:                                                            # try 3 times
                continue
            else:                                                                       # if failed 3 times: give up
                raise
        if search_page.status_code==403:                                                # if status code 403 (forbidden): probably cookies and headers not set correctly
            logging.error(f"Downloading tag search from \"{search_request.url}\" resulted in status code {search_page.status_code}. Have you set \"cookies.json\" and \"headers.json\" correctly?")
            raise requests.HTTPError(f"Error in {_search_hentai_ID_by_tag.__name__}{inspect.signature(_search_hentai_ID_by_tag)}: Downloading tag search from \"{search_request.url}\" resulted in status code {search_page.status_code}. Have you set \"cookies.json\" and \"headers.json\" correctly?")
        if search_page.ok==False:
            time.sleep(1)
            if attempt_no<3:                                                            # try 3 times
                continue
            else:                                                                       # if failed 3 times: give up
                raise

        search=json.loads(search_page.text)
        break

    page_no_max=int(search["num_pages"])

    return page_no_max


def _search_hentai_ID_by_tag(search_request: requests.PreparedRequest) -> list[str]:
    """
    Searches for nhentai ID by tag on page page_no.

    Arguments:
    - search_request: prepared request to nhentai search API

    Returns:
    - hentai_ID_list: hentai ID found by searching by tag on page page_no

    Raises:
    - requests.HTTPError: Downloading tag search from \"{NHENTAI_SEARCH_API_URL}\" with params={"query": tag, "sort": "popular", "page": PAGE_NO,} failed multiple times.
    """

    hentai_ID_list_str: list[str]
    search: dict
    search_page: requests.Response


    attempt_no: int=1
    while True:
        try:
            search_page=requests.Session().send(search_request, timeout=10)
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):  # if connection error: try again
            time.sleep(1)
            if attempt_no<3:                                                            # try 3 times
                continue
            else:                                                                       # if failed 3 times: give up
                raise
        if search_page.status_code==403:                                                # if status code 403 (forbidden): probably cookies and headers not set correctly
            logging.error(f"Downloading tag search from \"{search_request.url}\" resulted in status code {search_page.status_code}. Have you set \"cookies.json\" and \"headers.json\" correctly?")
            raise requests.HTTPError(f"Error in {_search_hentai_ID_by_tag.__name__}{inspect.signature(_search_hentai_ID_by_tag)}: Downloading tag search from \"{search_request.url}\" resulted in status code {search_page.status_code}. Have you set \"cookies.json\" and \"headers.json\" correctly?")
        if search_page.status_code==404:                                                # if status code 404 (not found): nhenati API is sus and randomly does not have some search result pages
            hentai_ID_list_str=[]                                                           # just return empty list
            return hentai_ID_list_str
        if search_page.ok==False:
            time.sleep(1)
            if attempt_no<3:                                                            # try 3 times
                continue
            else:                                                                       # if failed 3 times: give up
                raise

        search=json.loads(search_page.text)
        break


    hentai_ID_list_str=[str(hentai["id"]) for hentai in search["result"]]   # parse all hentai ID, ensure really string

    return hentai_ID_list_str