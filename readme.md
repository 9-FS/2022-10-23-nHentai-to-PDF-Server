---
Topic: "nHentai to PDF Server"
Author: "구FS"
---
<link href="./doc_templates/md_style.css" rel="stylesheet"></link>
<body>

# <p style="text-align: center">nHentai to PDF Server</p>
<br>
<br>

- [1. General](#1-general)
- [2. How to Set Up](#2-how-to-set-up)
  - [2.1. Firefox](#21-firefox)
  - [2.2. Google Chrome](#22-google-chrome)

## 1. General

This is the nHentai downloader I wrote to archive as much of the [english nHentai library](https://nhentai.net/language/english/popular) as I can. This server version builds upon the original [nhentai to PDF downloader](https://github.com/9-FS/2021-11-15-nHentai-to-PDF) and automates searching by `nhentai_tag`, creating a `downloadme.txt` from that, downloading the hentai, and finally repeating the process all over again. It basically syncs part of the nhentai library to the local directory at `library_path`.  
Big thanks go out to [h3nTa1m4st3r_xx69](https://github.com/sam-k0), who helped me using nhentai's completely undocumented API. Without him this project could not have been reactivated.  
I'm happy about anyone who finds my software useful and feedback is also always welcome. Happy downloading~

<div style="page-break-after: always;"></div>

## 2. How to Set Up
### 2.1. Firefox

1. Execute the program once. This will create a default `./config/cookies.json`.
1. Go to https://nhentai.net/. Clear the cloudflare prompt.
1. Open the developer console with F12.
1. Go to the tab "Storage". On the left side expand "Cookies". Click on "https://nhentai.net".
1. Copy the cookie values into the `cookies.json`.
1. Execute the program again. This will create a default `./config/headers.json`.
1. Go to https://www.whatismybrowser.com/detect/what-is-my-user-agent/ and copy your user agent into `headers.json`.
1. In `./config/settings.json` set `library_path` to the directory you want to download to. By default, it will download to `./hentai/`.
1. In `./config/settings.json` set `library_split` if you want to split your library into sub-directories. The number specifies the maximum number of hentai to allow per sub-directory. Set "0" if you want to disable splitting your library into sub-directories. By default, it will split into sub-directories of maximum 10.000 hentai each.
1. In `./config/settings.json` set `nhentai_tag` to the tag you want to download. By default, it will download "language:english"; all english hentai. You can set it to any tag you want with "tag:{tag}". You can find a list of all tags [here](https://nhentai.net/tags/).

### 2.2. Google Chrome

1. Execute the program once. This will create a default `./config/cookies.json`.
1. Go to https://nhentai.net/. Clear the cloudflare prompt.
1. Open the developer console with F12.
1. Go to the tab "Application". On the left side under "Storage", expand "Cookies". Click on "https://nhentai.net".
1. Copy the cookie values into the `cookies.json`.
1. Execute the program again. This will create a default `./config/headers.json`.
1. Go to https://www.whatismybrowser.com/detect/what-is-my-user-agent/ and copy your user agent into `headers.json`.
1. In `./config/settings.json` set `library_path` to the directory you want to download to. By default, it will download to `./hentai/`.
1. In `./config/settings.json` set `library_split` to the maximum number of hentai per sub-directory in your `library_path`. Set "0" if you want to disable splitting your library into sub-directories.
1. In `./config/settings.json` set `library_split` if you want to split your library into sub-directories. The number specifies the maximum number of hentai to allow per sub-directory. Set "0" if you want to disable splitting your library into sub-directories. By default, it will split into sub-directories of maximum 10.000 hentai each.
1. In `./config/settings.json` set `nhentai_tag` to the tag you want to download. By default, it will download "language:english"; all english hentai. You can set it to any tag you want with "tag:{tag}". You can find a list of all tags [here](https://nhentai.net/tags/).

> :information_source:  
> Setting cookies seems to be required daily nowadays.

</body>