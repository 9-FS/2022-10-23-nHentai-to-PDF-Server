#import "@preview/wrap-it:0.1.0": wrap-content  // https://github.com/ntjess/wrap-it/blob/main/docs/manual.pdf
#import "./doc_templates/src/note.typ": *
#import "./doc_templates/src/style.typ": set_style


#show: doc => set_style(
    topic: "nhentai_to_pdf_server",
    author: "구FS",
    language: "EN",
    doc
)
#set text(size: 3.5mm)


#align(center, text(size: 2em, weight: "bold")[nhentai_to_pdf_server])
#line(length: 100%, stroke: 0.3mm)
\
\
= Introduction

This is the nHentai downloader I wrote to archive as much of the #link("https://nhentai.net/language/english/popular")[english nHentai library] as I can. This server version builds upon the original #link("https://github.com/9-FS/2021-11-15-nHentai-to-PDF")[nhentai to PDF downloader] and automates searching by `NHENTAI_TAG`, creating a `downloadme.txt` from that, downloading the hentai, and finally repeating the process all over again. It basically syncs part of the nhentai library to the local directory at `LIBRARY_PATH`.

Big thanks go out to #link("https://github.com/sam-k0")[h3nTa1m4st3r_xx69], who helped me using nhentai's completely undocumented API. Without him this project could not have been reactivated.
I'm happy about anyone who finds my software useful and feedback is also always welcome. Happy downloading~

= Table of Contents

#outline()

#pagebreak(weak: true)

= Installation
== Firefox

+ Execute the program once. This will create a default `./config/config.json`.
    + Set `LIBRARY_PATH` to the directory you want to download to. By default, it will download to `./hentai/`.
    + Set `LIBRARY_SPLIT` if you want to split your library into sub-directories. The number specifies the maximum number of hentai to allow per sub-directory. Set "0" if you want to disable splitting your library into sub-directories. It is disabled by default and only recommended if the number of hentai in 1 directory starts to affect file explorer performance. This _should_ not affect you if you have 10.000 files or less in 1 directory. By default, it will split into sub-directories of maximum 10.000 hentai each.
    + Set `NHENTAI_TAG` to the tag you want to download. By default, it will download "language:english"; all english hentai. You can set it to any tag you want with "tag:{tag}". You can find a list of all tags #link("https://nhentai.net/tags/")[here].
+ Execute the program again. This will create a default `./.env`.
    + Go to https://nhentai.net/. Clear the cloudflare prompt.
    + Open the developer console with F12.
    + Go to the tab "Storage". On the left side expand "Cookies". Click on "https://nhentai.net".
    + Copy the cookie values into the `./.env`.
    + Go to https://www.whatismybrowser.com/detect/what-is-my-user-agent/ and copy your user agent into `./.env`.

== Google Chrome

+ Execute the program once. This will create a default `./config/config.json`.
    + Set `LIBRARY_PATH` to the directory you want to download to. By default, it will download to `./hentai/`.
    + Set `LIBRARY_SPLIT` if you want to split your library into sub-directories. The number specifies the maximum number of hentai to allow per sub-directory. Set "0" if you want to disable splitting your library into sub-directories. It is disabled by default and only recommended if the number of hentai in 1 directory starts to affect file explorer performance. This _should_ not affect you if you have 10.000 files or less in 1 directory. By default, it will split into sub-directories of maximum 10.000 hentai each.
    + Set `NHENTAI_TAG` to the tag you want to download. By default, it will download "language:english"; all english hentai. You can set it to any tag you want with "tag:{tag}". You can find a list of all tags #link("https://nhentai.net/tags/")[here].
+ Execute the program again. This will create a default `./.env`.
    + Go to https://nhentai.net/. Clear the cloudflare prompt.
    + Open the developer console with F12.
    + Go to the tab "Application". On the left side under "Storage", expand "Cookies". Click on "https://nhentai.net".
    + Copy the cookie values into the `./.env`.
    + Go to https://www.whatismybrowser.com/detect/what-is-my-user-agent/ and copy your user agent into `./.env`.

#info()[Setting cookies seems to be required daily nowadays.]

#pagebreak(weak: true)

= Usage

Choose hentai by nHentai ID to download and convert to PDF. You can either load ID from a `./config/downloadme.txt` seperated by linebreaks or directly enter ID into the console separated by spaces.