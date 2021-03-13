
# Broken Link Hijacker

BrokenLinkHijacker(BLH) is a Fast Broken Link Hijacker Tool written in Python. It crawls the website and searches for all the Broken Links.This tool is mainly designed for Bug Bounty Hunters.It helps bug hunters collect all the Broken Links from the domain they are targeting. It crawls the website on 3 different deepness to get all the links from it. It also helps to find all the Social Media or Social Engagement platforms links mentioned on the website.  It Searches for links in 
- `<a href>` tag
- `<img src>` tag

![BLH-3](https://user-images.githubusercontent.com/29165227/109423919-70c12d00-7a07-11eb-9598-2dd26d6a5b10.PNG)




## Installation
`https://github.com/MayankPandey01/BrokenLinkHijacker.git`

## Recommended Python Version:
This Tool Only Supports Python 3.
The recommended version for Python 3 is 3.8.x.

## Dependencies:

The dependencies can be installed using the requirements file:.

Installation on Windows:.
- python.exe -m pip install -r requirements.txt.

Installation on Linux.
- sudo pip install -r requirements.txt.


## How it Works

This tool searches for all the INBOUND and OUTBOUND links from HTML tags and then crawls it Further based on the Depness set by the user

Deepness Decide how the Search takes Place on the Webpage
- Deepness = 1
It means that only the given Url will be Crawled
- Deepness=2
In this search, the Crawler goes on Step Further and goes one more level deep to search
- Deepness=3
Here all the INBOUND links from the website are crawled until there is no link left to crawl.
This can take a significant amount of time to complete.


## Usage

Short Form    | Long Form     | Description
------------- | ------------- |-------------
url           | url           | A URL to scan 
-d            | Deepness      | Level of deepness to search.(Default=1)[Varies from 1-3]
-v            | --verbosity   | Set the Verbosity for Program
-o            | --output      | Weather to save the output in a file or not.(Default=False)
-h            | --help        | Displays help 


## Examples

- To Use the Tool in the default setting.\
`BLH.py https://google.com` will give result.

![BLH-4](https://user-images.githubusercontent.com/29165227/109423934-820a3980-7a07-11eb-9348-c25692ce16aa.PNG)


- To Increase Deepness Use :

`BLH.py https://google.com -d 2  ` This will set Deepness to 2.\
`BLH.py https://google.com -d 3  ` This will set Deepness to 3 .

- To turn Verbosity Mode On or OFF :
 
  *By default Verbosity Mode is Set to True*.\
  `BLH.py https://google.com -v False` . \
  `-v F or -v Flase ` |  `-v T or -v True`.

- To Save output To a file : 

  *By default Output is Set to False. The output filename is set to `domain_links.txt` by default*.\
  `BLH.py https://google.com -o True` . \
  `-o F or -o False ` | `-o T or -o True`.

   
### Note
- More details here https://edoverflow.com/2017/broken-link-hijacking/

Use This Tool Wisely.\
Happy Hacking :sparkles: :sparkles:
