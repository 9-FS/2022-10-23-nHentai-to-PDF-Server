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
  - [2.1. Connection to nhentai.net (with Google Chrome)](#21-connection-to-nhentainet-with-google-chrome)
  - [2.2. Connection to dropbox.com](#22-connection-to-dropboxcom)

## 1. General

This is the nHentai downloader I wrote to archive as much of the [english nHentai library](https://nhentai.net/language/english/popular) as I can. This server version builds upon the original [nhentai to PDF downloader](https://github.com/9-FS/2021-11-15-nHentai-to-PDF) and automates the creation of a `downloadme.txt`, downloading the hentai, and finally uploading it to a dropbox folder of your choosing. It basically syncs part of the nhentai library (a tag of your choice) to your dropbox.  
Big thanks go out to [h3nTa1m4st3r_xx69](https://github.com/sam-k0), who helped me using nhentai's completely undocumented API. Without him this project could not have been reactivated.  
I'm happy about anyone who finds my software useful and feedback is also always welcome. Happy downloading~

## 2. How to Set Up
### 2.1. Connection to nhentai.net (with Google Chrome)

1. Execute the program once. This will create a default `cookies.json`.
1. Go to https://nhentai.net/. Clear the cloudflare prompt.
1. Open the developer console with F12.
1. Go to the tab "Application". On the left side under "Storage", expand "Cookies". Click on "https://nhentai.net".
1. Copy the cookie values into the `cookies.json`.
1. Execute the program again. This will create a default `headers.json`.
1. Go to https://www.whatismybrowser.com/detect/what-is-my-user-agent/ and copy your user agent into `headers.json`.

> :information_source:  
> This seems to be required daily nowadays.

### 2.2. Connection to dropbox.com
1. Execute the program again. This will create a default `dropbox_API_cred.json`.
1. Go to https://stackoverflow.com/questions/70641660/how-do-you-get-and-use-a-refresh-token-for-the-dropbox-api-python-3-x and follow the accepted answer's steps to get your dropbox API credentials. Copy your credentials into `dropbox_API_cred.json`.
1. Execute the program again. This will create a default `dropbox_config.json`.
1. Optionally set a custom destination folder in your dropbox and change the tag to the hentai you're interested in. It is set to `language:english` by default, but accepts other tags in format `tag:{tag_name}` (Obviously leave out the curly brackets.).

</body>