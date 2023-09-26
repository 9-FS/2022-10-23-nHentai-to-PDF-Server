# Copyright (c) 2023 구FS, all rights reserved. Subject to the MIT licence in `licence.md`.
import dropbox, dropbox.exceptions
import json
from KFSconfig  import KFSconfig
from KFSdropbox import KFSdropbox
from KFSfstr    import KFSfstr
from KFSlog     import KFSlog
from KFSmedia   import KFSmedia
from KFSsleep   import KFSsleep
import logging
import os
from get_hentai_ID_list import get_hentai_ID_list
from Hentai             import Hentai


@KFSlog.timeit
def main():
    cleanup_success: bool=True                  # cleanup successful
    cookies: dict[str, str]                     # for requests.get to bypass bot protection
    COOKIES_DEFAULT: str=json.dumps({           # cookies configuration default
        "cf_clearance": "",
        "csrftoken": "",
    }, indent=4)
    dbx: dropbox.Dropbox                        # dropbox instance
    dropbox_API_cred: dict[str, str]            # dropbox API credentials
    DROPBOX_API_CRED_DEFAULT: str=json.dumps({  # dropbox configuration default
        "app_key": "",
        "app_secret": "",
        "refresh_token": "",
    }, indent=4)
    dropbox_config: dict[str, str]              # dropbox_dest_path
    DROPBOX_CONFIG_DEFAULT: str=json.dumps({    # dropbox hentai destination path
        "dropbox_dest_path": "/hentai/",        # the path to the dropbox directory to sync to
        "tag": "language:english",              # the tag to download and sync to dropbox, usually all english hentai
    }, indent=4)
    headers: dict[str, str]                     # for requests.get to bypass bot protection
    HEADERS_DEFAULT: str=json.dumps({           # headers configuration default
        "User-Agent": "",
    }, indent=4)
    hentai: Hentai                              # individual hentai
    hentai_ID_list: list[int]                   # hentai ID to download


    try:
        cookies         =json.loads(KFSconfig.load_config("cookies.json",          COOKIES_DEFAULT))            # load cookies to bypass bot protection
        headers         =json.loads(KFSconfig.load_config("headers.json",          HEADERS_DEFAULT))            # load headers to bypass bot protection
        dropbox_API_cred=json.loads(KFSconfig.load_config("dropbox_API_cred.json", DROPBOX_API_CRED_DEFAULT))   # load API credentials
        dropbox_config  =json.loads(KFSconfig.load_config("dropbox_config.json",   DROPBOX_CONFIG_DEFAULT))     # load dropbox configuration
    except FileNotFoundError:
        return
    dbx=dropbox.Dropbox(oauth2_refresh_token=dropbox_API_cred["refresh_token"], app_key=dropbox_API_cred["app_key"], app_secret=dropbox_API_cred["app_secret"]) # create Dropbox instance
    
    
    while True:
        hentai_ID_list=get_hentai_ID_list(cookies, headers, dbx, dropbox_config)   # get desired hentai ID
        

        for i, hentai_ID in enumerate(hentai_ID_list):  # work through all desired hentai
            logging.info("--------------------------------------------------")
            logging.info(f"{KFSfstr.notation_abs(i+1, 0, round_static=True)}/{KFSfstr.notation_abs(len(hentai_ID_list), 0, round_static=True)} ({KFSfstr.notation_abs((i+1)/(len(hentai_ID_list)), 2, round_static=True)})")

            try:
                hentai=Hentai(hentai_ID, cookies, headers)  # create hentai object
            except ValueError:                              # if hentai does not exist:
                continue                                    # skip to next hentai
            else:
                logging.info(hentai)

            try:
                hentai.download()                               # download hentai
            except FileExistsError:                             # if hentai already exists:
                continue                                        # skip to next hentai
            except KFSmedia.DownloadError:
                with open("FAILURES.txt", "at") as fails_file:  # append in failure file
                    fails_file.write(f"{hentai.ID}\n")
                continue                                        # skip to next hentai

            logging.info(f"Uploading \"{hentai.PDF_filepath}\" to dropbox \"{dropbox_config['dropbox_dest_path']}{os.path.basename(hentai.PDF_filepath)}\"...")
            try:
                KFSdropbox.upload_file(dbx, hentai.PDF_filepath, f"{dropbox_config['dropbox_dest_path']}{os.path.basename(hentai.PDF_filepath)}")   # upload PDF to dropbox
            except dropbox.exceptions.ApiError as e:
                logging.error(f"Uploading \"{hentai.PDF_filepath}\" to dropbox \"{dropbox_config['dropbox_dest_path']}{os.path.basename(hentai.PDF_filepath)}\" failed with:\n{e}\nFile probably exists already.")
                with open("FAILURES.txt", "at") as fails_file:  # append in failure file just to be sure
                    fails_file.write(f"{hentai.ID}\n")
            else:
                logging.info(f"Uploaded \"{hentai.PDF_filepath}\" to dropbox \"{dropbox_config['dropbox_dest_path']}{os.path.basename(hentai.PDF_filepath)}\".")

            try:
                os.remove(hentai.PDF_filepath)  # try to clean up and remove uploaded PDF
            except PermissionError:
                logging.warning(f"Deleting \"{hentai.PDF_filepath}\" failed with PermissionError.")
        logging.info("--------------------------------------------------")


        logging.info("Deleting leftover image folders...")
        for hentai_ID in hentai_ID_list:                                                                # attempt final cleanup
            if os.path.isdir(f"./hentai/{hentai_ID}") and len(os.listdir(f"./hentai/{hentai_ID}"))==0:  # if cache folder still exists and is empty:
                try:
                    os.rmdir(f"./hentai/{hentai_ID}")                                                   # try to clean up
                except PermissionError:                                                                 # may fail if another process is still using directory like dropbox
                    logging.warning(f"Deleting \"./hentai/{hentai_ID}\" failed with PermissionError.")
                    cleanup_success=False                                                               # cleanup unsuccessful

        if cleanup_success==True:
            logging.info("\rDeleted leftover image folders.")

        KFSsleep.sleep_mod(100) # sleep until the next whole 100s