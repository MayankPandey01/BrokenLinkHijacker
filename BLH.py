import requests
from urllib.parse import urlparse, urljoin
import urllib3
from bs4 import BeautifulSoup
import colorama
import sys
import argparse
import random

colorama.init()

headers = { 'user-agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
 }

to_verify_ssl_cert=True
urllib3.disable_warnings()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
RED = colorama.Fore.RED
BLUE = colorama.Fore.BLUE
CYAN = colorama.Fore.CYAN


social_list=["twitter.com","facebook.com","instagram.com","linkedin.com","youtube.com","twitch.com","twitch.tv","discord.com","slack.com","soundcloud.com","medium.com",
"vimeo.com","skype.com","pinterest.com","ct.pinterest.com","snapchat.com","telegram","t.me","telegram.com","clickcease.com","wistia.com","adjust.com","github.com"

]

inbound_urls = set()
outbound_urls = set()
current_inbound_urls =set()
broken_urls  = set()
social_urls = []
number_of_broken_link=0


total_urls_visited = 0



def banner():
    version="1.0"
    ascii_banner="""
     ____            _                _     _       _
    | __ ) _ __ ___ | | _____ _ __   | |   (_)_ __ | | __
    |  _ \| '__/ _ \| |/ / _ \ '_ \  | |   | | '_ \| |/ /
    | |_) | | | (_) |   <  __/ | | | | |___| | | | |   <
    |____/|_|  \___/|_|\_\___|_| |_| |_____|_|_| |_|_|\_\\

     _   _ _  _            _               _   _   _
    | | | (_)(_) __ _  ___| | _____ _ __  | | | | | |
    | |_| | || |/ _` |/ __| |/ / _ \ '__| | | | | | |
    |  _  | || | (_| | (__|   <  __/ |    |_| |_| |_|
    |_| |_|_|/ |\__,_|\___|_|\_\___|_|    (_) (_) (_)
           |__/
    """
    print(ascii_banner)
    print(f"{RED}                        Version-",version)
def random_ua():
    UAS=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
     "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36",
     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36",
     "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1",
     "Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36"
     )

    ua = UAS[random.randrange(len(UAS))] # to generate random User-Agent for deep crawling
    ua=str(ua)
    headers['user-agent']=ua

def is_valid(url): #Checking For Valid URL's
    try:
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)
        valid_request=requests.get(url,headers=headers,verify=to_verify_ssl_cert)
        if valid_request!=200:
            print(f"{RED} Enter Valid Url {RESET} ")
            sys.exit()
            
    except:
        print(f"{RED} ERROR {RESET} ")
        sys.exit()




def main_webpage_links(url):   #Returns all URLs from the given Main Website
    try:
        urls = set()
        random_ua()
        domain_name = urlparse(url).netloc
        soup = BeautifulSoup(requests.get(url,headers=headers,verify=to_verify_ssl_cert).content, "html.parser")
        for a_tag in soup.findAll("a"):              #CHECK FOR LINKS IN HERF TAG
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                continue
            href = urljoin(url, href)
            parsed_href = urlparse(href)
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
            if not is_valid(href):
                continue
            if href in inbound_urls:
                continue
            if domain_name not in href:
                if href not in outbound_urls:
                    if verbosity:
                        print(f"{BLUE}[!] Outbound link: {href}{RESET}")
                    outbound_urls.add(href)
                    social_domain=str(urlparse(href).netloc)
                    if social_domain and social_domain.strip('www.') in social_list:
                        social_urls.append(href)
                continue
            if verbosity:
                print(f"{GREEN}[*] Inbound link: {href}{RESET}")
            urls.add(href)
            inbound_urls.add(href)
            
        for img_tag in soup.findAll('img'):  #check for link inside images
            href = img_tag.attrs.get('src')
            if href == "" or href is None:
                continue
            href = urljoin(url, href)
            parsed_href = urlparse(href)
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
            if not is_valid(href):
                continue
            if href in inbound_urls:
                continue
            if domain_name not in href:
                if href not in outbound_urls:
                    if verbosity:
                        print(f"{GRAY}[!] Outbound Image link: {href}{RESET}")
                    outbound_urls.add(href)
                    social_domain=str(urlparse(href).netloc)
                    if social_domain and social_domain.strip('www.') in social_list:
                        social_urls.append(href)
                continue
            if verbosity:
                print(f"{GRAY}[!] Inbound Image link: {href}{RESET}")
            inbound_urls.add(href)

        return urls
    except KeyboardInterrupt:
        print(f"{RED} Keyboard Interrupt detected{RESET} ")
        sys.exit()


def crawl(url):
    try:
        global total_urls_visited
        total_urls_visited += 1
        links = main_webpage_links(url)
        for link in links:
            random_ua()
            crawl(link)
    except KeyboardInterrupt:
        print(f"{RED} Keyboard Interrupt detected{RESET} ")
        sys.exit()
    except:
        print(f"{RED} ERROR {RESET} ")
        sys.exit()

def status_check(url):
    try:
        r=requests.get(url,headers=headers,verify=to_verify_ssl_cert)
        if r.status_code==404:
            number_of_broken_link+=1
            print(f"{RED}[!] BROKEN LINK: {url}{RESET}")
        if r.status_code==301 or r.status_code==302 or r.status_code==401 or r.status_code==403 or r.status_code==429 or r.status_code==500 or r.status_code==503:
            print(f"{CYAN}[!] HTTP ERROR : {url}{r.status_code}{RESET}")
    except KeyboardInterrupt:
        print(f"{RED} Keyboard Interrupt detected{RESET} ")
        sys.exit()
    except:
         print(f"{CYAN}[!] UNABLE TO CONNECT : {url}{RESET}")

def main_proc(deep):
        if deep>3 or deep<=0:
                print(f"{RED}[*] Incorrect Value for Deepness :{RESET}",deep)
                print(f"{RED}[*] Deepness Level Varies from 1-3{RESET}")
                print("")
        
        if deep==1:
            links = main_webpage_links(url)
            print("")
            search_msg()
            for link in outbound_urls:
                link=str(link)
                status_check(link)
            status_check_msg()
        elif deep==2:
            links = main_webpage_links(url)
            for link in links:
                main_webpage_links(link)
            print("")
            search_msg()
            for link in outbound_urls:
                link=str(link)
                status_check(link)
            status_check_msg()
            
        elif deep==3:
            crawl(url)
            search_msg()
            for link in outbound_urls:
                link=str(link)
                status_check(link)
            status_check_msg()



def info():
        print("")
        print(f"{BLUE} Domain Name -->{RESET}",domain_name)
        print(f"{BLUE} Deepness --> {RESET}",deep)
        print(f"{BLUE} Output To a File --> {RESET}",output)
        print(f"{BLUE} Output File --> {RESET}",output_location,"(DEFAULT)")
        print(f"{BLUE} Verbosity --> {RESET}",verbosity)
        print(f"{BLUE} TO verify SSL Certificate --> {RESET}",to_verify_ssl_cert)
        print("")

def print_output():
    print(f"{BLUE} Printing Output To File --> ",output_location)
    with open(f"{domain_name}_links.txt", "a") as f:
                print(" Domain Name -->",domain_name, file=f)
                print( "Deepness -->",deep, file=f)
                print("Output File -->",output_location,"(DEFAULT)", file=f)
                print("Verbosity -->",verbosity, file=f)
                print("Output To a File -->",output, file=f)
                print("", file=f)
                print("---Inbound URL's---", file=f)
                print("", file=f)
                for internal_link in inbound_urls:
                    print(internal_link.strip(), file=f)
                print("", file=f)
                print("---Outbound URL's---", file=f)
                print("", file=f)
                for external_link in outbound_urls:
                    print(external_link.strip(), file=f)
                print("", file=f)
                print("---Social URL's---", file=f)
                print("", file=f)   
                for social_links in social_urls:
                    print(social_links.strip(), file=f)
                print("", file=f)
                print("[+] Total Inbound links:", len(inbound_urls), file=f)
                print("[+] Total Outbound links:", len(outbound_urls), file=f)
                print("[+] Total URLs:", len(outbound_urls) + len(inbound_urls), file=f)
                print("", file=f)
    f.close()


def stats():
        print("")
        print("[+] Total Inbound links:", len(inbound_urls))
        print("[+] Total Outbound links:", len(outbound_urls))
        print("[+] Total URLs:", len(outbound_urls) + len(inbound_urls))
        print("")


def status_check_msg():
    try:
        if number_of_broken_link==0:
                    print(f"{RED}[*] NO BROKEN LINKS FOUND{RESET}")
    except KeyboardInterrupt:
        print(f"{RED} Keyboard Interrupt detected{RESET} ")
        sys.exit()

def search_msg():
    print("-----------------------------------"f"{GREEN}Searching Broken Links{RESET}""-----------------------------------------")
    print("")

def show_social():
    for i in social_urls:
        print(f"{GREEN}[--] Social URL's: {i}{RESET}")




                                 #Main Section


if __name__ == "__main__":
    try:
        
        import argparse
        parser = argparse.ArgumentParser(description="Broken Link Finder Tool with Python")
        parser.add_argument("url", help="The URL to extract links from.")
        parser.add_argument("-d", "--deepness", help="Level of deepness to search.(Default=1)", default=1, type=int)
        parser.add_argument("-o", "--output", help="Weather to save the output in a file. Default is False(Filename=domain-name_links.txt)")
        parser.add_argument("-v", "--verbosity", help="Set the Verbosity of Program(Default=True)")
        args = parser.parse_args()
        url = args.url
        deep = args.deepness
        verbosity = args.verbosity
        domain_name = urlparse(url).netloc
        output_location=domain_name+"_links.txt"
        banner()
        if args.verbosity==False or args.verbosity=="F":
            verbosity=False
        else:
            verbosity=True
        if args.output==True or args.output=="T":
            output=True
        else:
            output=False
        is_valid(url)
        info()
        main_proc(deep)
        for i in social_urls:
            print(f"{GREEN}[--] Social URL's: {i}{RESET}")
        stats()
        if output:
            print_output()

    except KeyboardInterrupt:
        print(f"{RED} Keyboard Interrupt detected{RESET} ")
        sys.exit()