import os
import sys
import json
import time
import socket
import urllib3
import requests
import threading


def worker(term, site, url, headers):
    global file_complete
    global urls_list
    global exec_list

    payload = json.dumps({
        "term": term,
        "site": site,
        "step_skip_b1": True
    })

    requests_kwargs = {
        "url": url,
        "timeout": 600,
        "data": payload,
        "headers": headers
    }
    try:
        start = time.time()
        session = requests.Session()
        response = session.post(**requests_kwargs)
        print(f'response : {response}')
        end = time.time()
        exec_list.append(end - start)
        with open(file_complete, 'a') as f:
            sys.stdout = f
            print(f"{site} : {term} : {json.loads(response.text)}")
            if 'urls' in json.loads(response.text):
                urls_list.extend(json.loads(response.text)['urls'])

    except (socket.timeout, urllib3.exceptions.ReadTimeoutError, requests.exceptions.ReadTimeout):
        with open(file_complete, 'a') as f:
            sys.stdout = f
            print(f"socket timeout for {site} : {term}")


def main():
    global original_stdout
    global file_simple
    global file_complete
    global urls_list
    global exec_list

    sites = ['http://m4ufree.tv/',
             'http://www.movie4k.ml',
             'https://1234movies.club',
             'https://123moviefree.sc',
             'https://123movie-gdn.dev',
             'https://1-23movies.cc',
             'https://123movies4u.vip',
             'https://123moviesd.com',
             'https://123moviesfree.love',
             'https://123moviesfun.is',
             'https://123moviesgo.club',
             'https://123moviesgo.wf',
             'https://1movies.life',
             'https://altadefinizione.name',
             'https://bflix.watch/',
             'https://cuevana.blog',
             'https://cuevana3.so',
             'https://dmphim.net',
             'https://filminvazio.hu',
             'https://filmstoon.in',
             'https://film-streaming1.club',
             'https://fmovies.pink',
             'https://fmovies.top',
             'https://fmoviesto.cc',
             'https://gomovies.agency',
             'https://gomovies.design',
             'https://gomovies.guru',
             'https://m4ufree.tv',
             'https://m4uhd.net',
             'https://movgotv.com',
             'https://moviesjoy.to',
             'https://pelisplushd.net',
             'https://projectfreetv.watch',
             'https://tinyzonetv.to',
             'https://vumoo.life',
             'https://vw1.ffmovies.sc',
             'https://w.putlockers.co',
             'https://w2.putlockers.co',
             'https://w5.putlocker.to',
             'https://watch0123movies.org',
             'https://ww5.fmovie.cc',
             'https://www.dpstream.best',
             'https://www.illimitestreaming.co',
             'https://www.movie4k.ml',
             'https://www.pelisplus.org',
             'https://www.thetamilyogi.co',
             'https://www1.1movies.live',
             'https://www1.cmovies.ac',
             'https://www1.solarmovies.movie',
             'https://www4.fusionmovies.to',
             'https://xmovies8.10s.live',
             'https://yesmovies.sx',
             'https://ymovies.vip',
             'https://yomovies.is',
             "https://123-movies-free.com",
             "https://www1.123moviesto.to/",
             "https://123moviesfree.net",
             "https://123moviesgot.com",
             "https://4movie.me/",
             "https://altadefinizione.sale/",
             "https://ww.123movieshub.one",
             "https://ww1.123movieshub.one",
             "https://123movies.gdn",
             "https://123putlocker.info",
             "https://www3.0gomovies.com",
             "https://new123movies.la/",
             "https://la123movies.com/",
             "https://movies123.show",
             "https://123moviess.cc",
             "https://123movies.domains",
             "https://www4.123movies.link",
             "https://movies123.pro",
             "https://altadefinizione.network/",
             "https://altadefinizione.la",
             "https://bmovies.co/",
             "https://ffmovies.to/",
             "https://fmovies.to/movies",
             "https://nyafilmer.vip/",
             "https://w2.putlockers.co/",
             "https://putlockernew.site/",
             "https://ww2.1movies.is",
             "https://ww3.1todaypk.live/",
             "https://www9.0123movies.com/",
             "https://xmovies.is/",
             "https://zona-leros.net",
             "https://europixhd.biz/",
             "https://hd-streams.org/",
             "https://kinos.to/",
             "https://lookmovie.io/",
             "https://losmovies.live",
             "https://m4ufree.fun/",
             "https://moviestars.to/",
             "https://voirfilms.stream",
             "https://wvw.ocine.cc",
             "https://www.dpstream.biz/",
             "https://www.putlockers.cr/",
             "https://5movies.run",
             "https://wmoviesfree.com/",
             "https://free-putlockers.com",
             "https://couchtuner.name",
             "https://projectfreetv.fun",
             "https://spacemov.top",
             "https://xmovies08.org",
             "https://watch32hd.org",
             "http://ww1.m4ufree.com",
             "https://gostream.cool",
             "https://w1.putlocker.to",
             "https://movies7.to",
             "https://putlocker.vip",
             "https://himovies.to",
             "https://ww1.solarmovie.cr",
             "https://fsharetv.co",
             "https://onionplay.co",
             "https://9movies.yt",
             "https://mkvking.com",
             "https://bmovies.vip",
             "https://fmovies.top",
             "https://hdbest.net",
             "https://esubmovie.com",
             "https://fmovieshd.vip/",
             "https://www1.ev01.net"
             ]
    terms = ['No time to die 2021', 'Nobody 2021', 'Grimm', 'Game of Thrones']

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {api_token}"
    }

    for site in sites:
        for term in terms:
            while not threading.active_count() < concurrent_threads:
                continue
            sys.stdout = original_stdout
            print(f"Launching : {site} : {term}")
            time.sleep(1)
            p = threading.Thread(target=worker, args=[term, site, url, headers])
            p.start()

    while threading.active_count() != 1:
        continue

    with open(file_simple, 'a') as f:
        sys.stdout = f
        print(f'Final urls_list : {urls_list}')
        print(f'exec list : {exec_list}')
        print(f'length of exec list : {len(exec_list)}')
        print(f'average exec time : {sum(exec_list) / len(exec_list)}')


if __name__ == '__main__':
    url = os.getenv("URL")
    original_stdout = sys.stdout
    file_simple = 'simpleLogs.txt'
    file_complete = 'completeLogs.txt'
    api_token = os.getenv("API_TOKEN")
    concurrent_threads = int(os.getenv("CONCURRENT_THREADS"))
    urls_list = []
    exec_list = []
    main()
