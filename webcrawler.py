#code referenced from : https://xtrp.io/blog/2019/11/09/a-quick-python-script-to-find-broken-links/
#trying to simplify it and getting it to work

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin
import argparse
import csv
import multiprocessing
from joblib import Parallel, delayed
import threading

mutex = threading.Lock()
def recursive_checker(url,link):
    link=link.strip()
    upd_url = urljoin(url, link)
    if (link.startswith("https") or link.startswith("http") or link.startswith("www")):
        upd_url=link
    if(upd_url in broken):
        results.append([link,upd_url,url])
        # mutex.acquire()
        # with open(name, 'a', newline='') as file:
        #     writer = csv.writer(file)
        #     writer.writerow([link, upd_url, url])
        print("Broken Link:", upd_url, "in", url)
        # mutex.release()
    elif(not upd_url in searched):
        # print(len(searched))
        if not("javascript" in upd_url or upd_url.startswith("mailto") or upd_url.endswith(".png") or upd_url.endswith(".jpg") or upd_url.endswith(".jpeg") or upd_url.endswith(".7z") or upd_url.endswith(".csv") or upd_url.endswith("=data")):
            try:
                req=requests.get(upd_url)
                if (req.status_code != 200):
                    broken.append(upd_url)
                    results.append([link, upd_url, url])
                    # mutex.acquire()
                    # with open(name, 'a', newline='') as file:
                    #     writer = csv.writer(file)
                    #     writer.writerow([link,upd_url, url])
                    print("Broken Link:", upd_url, "in", url)
                    # mutex.release()
                else:
                    print("Not Broken Link:", upd_url, "in", url)
                    if urlparse(upd_url).netloc == urlparse(url).netloc:
                        links=getlinks(upd_url)
                        Parallel(n_jobs=num_cores,backend="threading")(delayed(recursive_checker)(upd_url,link) for link in links)
            except Exception as e:
                print("Error:",str(e),upd_url)
                results.append([link, upd_url, url,"Error: "+str(e)])
                # mutex.acquire()
                # with open(name, 'a', newline='') as file:
                #     writer = csv.writer(file)
                #     writer.writerow([link,upd_url, url,"Error: "+str(e)])
                # mutex.release()
def getlinks(url):
    searched.append(url)
    req=requests.get(url)
    html_website=req.text
    soup=BeautifulSoup(html_website,'html.parser')
    a_tags=soup.select("a[href]")
    links=[]
    for a_tag in a_tags:
        links.append(a_tag["href"])
    return links

def main():
    global num_cores,name,searched,manager,broken,results
    manager = multiprocessing.Manager()
    searched=manager.list()
    broken=manager.list()
    results=manager.list()
    # global searched,broken
    num_cores = multiprocessing.cpu_count()
    name = ""
    # searched = broken = []
    parser = argparse.ArgumentParser(description='Link Checker!')
    parser.add_argument('--url', required=True,
                        help='Give a Url')
    parser.add_argument('--name', required=True,
                        help='Give a output name')
    args, unknown = parser.parse_known_args()
    url = args.url
    name = args.name
    print("URL:",url)
    recursive_checker(url,"")
    with open(name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Broken Link", "Broken URL", "URL Containing Broken Link", "Errors"])
        writer.writerows(results)
    print("WE ARE DONE")
    return "END OF LINK CHECKER, CHECK FILE: "+name


if __name__ == '__main__':
    main()