import os
import sys
import json
import time
import socket
import urllib3
import requests
import threading
from datetime import datetime


def worker_medialookup(site, url, headers):
    global file_complete
    global urls_list
    global positives_list

    payload = json.dumps({
        "url": site,
        "analytics_only": True,
        "include_length": True,
        "direct_url": True,
        "min_length_seconds": 300
    })

    post_kwargs = {
        "url": url,
        "timeout": 1200,
        "data": payload,
        "headers": headers
    }
    try:
        session = requests.Session()
        response = session.post(**post_kwargs)
        with open(file_complete, 'a') as f:
            sys.stdout = f
            for element in json.loads(response.text)['results']:
                if element['has_video']:
                    positives_list.append(element)
    except (socket.timeout, urllib3.exceptions.ReadTimeoutError, requests.exceptions.ReadTimeout):
        with open(file_complete, 'a') as f:
            sys.stdout = f
            print(f"socket timeout for {site}")
    except KeyError:
        sys.stdout = original_stdout
        print(f'Key error for url {site}')
        print(f'responses in key error : {response.text}')
    except Exception as e:
        sys.stdout = original_stdout
        print(f'error : {e}')


def main():
    global original_stdout
    global file_simple
    global file_complete
    global urls_list
    global exec_list

    headers_medialookup = {
        'Authorization': f"Bearer {api_token}",
        'Content-Type': 'application/json'
    }

    urls_list = [
        {'has_video': True,
         'url': 'https://ww0.0gomovies.so/tv/aavi1-game-of-thrones-season-1/',
         'reference_url': 'https://ww0.0gomovies.so/tv/aavi1-game-of-thrones-season-1/'},
        {'has_video': True,
         'url': 'https://ww3.watch0123movies.org/tvshows/watch-game-of-thrones-online-free/',
         'reference_url': 'https://ww3.watch0123movies.org/tvshows/watch-game-of-thrones-online-free/'},
        {'has_video': True,
         'url': 'https://ymovies.vip/film/game-of-thrones-season-8-30429/',
         'reference_url': 'https://ymovies.vip/film/game-of-thrones-season-8-30429/'},
        {'has_video': True,
         'url': 'https://ww1.123movies.link/movie/QBf2RQk9/IAYPz8BZ-nobody',
         'reference_url': 'https://ww1.123movies.link/movie/QBf2RQk9-nobody'},
        {'has_video': True,
         'url': 'https://fmovies.pink/tv-show/grimm-season-4/8AYUFEf4/xhb9e7eJ',
         'reference_url': 'https://fmovies.pink/tv-show/grimm-season-4/8AYUFEf4'},
        {'has_video': True,
         'url': 'https://xmovies08.org/watch?v=Game_of_Thrones_S3_E1_2013#video=qIFdN_XWeyDanCCCTk_7rhKZSxogofGwoRiSJdCK',
         'reference_url': 'https://xmovies08.org/watch?v=Game_of_Thrones_S3_E1_2013#video=Ik5sPrhWR2wx-3obFOng3LOEDlrxspFySNosUiZSxg'},
        {'has_video': True,
         'url': 'https://www4.fusionmovies.to/tv-series/game-of-thrones-season-6/pyMLtOvZ/NpHfLlAi',
         'reference_url': 'https://www4.fusionmovies.to/tv-series/game-of-thrones-season-6/pyMLtOvZ'},
        {'has_video': True,
         'url': 'https://www.123movieshd.icu/series/game-of-thrones-season-5/',
         'reference_url': 'https://www.123movieshd.icu/series/game-of-thrones-season-5/'},
        {'has_video': True,
         'url': 'https://movies123.show/tv-show/game-of-thrones-season-5/DX9HUges/5GR0w9Ad',
         'reference_url': 'https://movies123.show/tv-show/game-of-thrones-season-5/DX9HUges'},
        {'has_video': True,
         'url': 'https://www.123movieshd.icu/series/game-of-thrones-season-2/',
         'reference_url': 'https://www.123movieshd.icu/series/game-of-thrones-season-2/'},
        {'has_video': True,
         'url': 'https://bflix.watch/tvshow/game-of-thrones-2011/',
         'reference_url': 'https://bflix.watch/tvshow/game-of-thrones-2011/'},
        {'has_video': True,
         'url': 'https://cmovies.online//film/grimm-season-2-qeo',
         'reference_url': 'https://cmovies.online//film/grimm-season-2-qeo'},
        {'has_video': True,
         'url': 'https://www1.solarmovie.cr/tv/game-of-thrones-season-3-11626/',
         'reference_url': 'https://www1.solarmovie.cr/tv/game-of-thrones-season-3-11626/'},
        {'has_video': True,
         'url': 'https://ymovies.vip/film/game-of-thrones-the-last-watch-31141/',
         'reference_url': 'https://ymovies.vip/film/game-of-thrones-the-last-watch-31141/'},
        {'has_video': True,
         'url': 'https://1movies.life/series/grimm-season-3/28314/sockhIsc',
         'reference_url': 'https://1movies.life/series/grimm-season-3/28314'},
        {'has_video': True,
         'url': 'https://www.thetamilyogi.net/watch-game-of-thrones-season-8-episode-6-online/',
         'reference_url': 'https://www.thetamilyogi.net/watch-game-of-thrones-season-8-episode-6-online/'},
        {'has_video': True,
         'url': 'https://www.123movieshd.icu/series/game-of-thrones-season-4/',
         'reference_url': 'https://www.123movieshd.icu/series/game-of-thrones-season-4/'},
        {'has_video': True,
         'url': 'https://ww6.putlocker.vip/film/game-of-thrones-season-8-30429/',
         'reference_url': 'https://ww6.putlocker.vip/film/game-of-thrones-season-8-30429/'},
        {'has_video': True,
         'url': 'https://vw1.ffmovies.sc/tv/game-of-thrones-season-3/',
         'reference_url': 'https://vw1.ffmovies.sc/tv/game-of-thrones-season-3/'},
        {'has_video': True,
         'url': 'https://1movies.life/series/grimm-season-2/26519/WiDCFWHX',
         'reference_url': 'https://1movies.life/series/grimm-season-2/26519'},
        {'has_video': True,
         'url': 'https://www.thetamilyogi.net/watch-no-time-to-die-online-3/',
         'reference_url': 'https://www.thetamilyogi.net/watch-no-time-to-die-online-3/'},
        {'has_video': True,
         'url': 'https://123movieshub.fr/movies/no-time-to-die-2021/',
         'reference_url': 'https://123movieshub.fr/movies/no-time-to-die-2021/'},
        {'has_video': True,
         'url': 'https://movies123.show/tv-show/game-of-thrones-season-8/FWLtcAty/EFVVrFkS',
         'reference_url': 'https://movies123.show/tv-show/game-of-thrones-season-8/FWLtcAty'},
        {'has_video': True,
         'url': 'https://www.123-movies.gdn/game-of-thrones-a-day-in-the-life-watch-free/',
         'reference_url': 'https://www.123-movies.gdn/game-of-thrones-a-day-in-the-life-watch-free/'},
        {'has_video': True,
         'url': 'https://xmovies08.org/watch?v=Game_of_Thrones_E3_S9_2013#video=95EnvWCmUJrCsIa6OJeV2MVXVDi095_UTSxZ67Qf',
         'reference_url': 'https://xmovies08.org/watch?v=Game_of_Thrones_E3_S9_2013#video=Ik5sPrhWR2wx-3obFOng3LOEDlrxspFySNosUiZSxg'},
        {'has_video': True,
         'url': 'https://projectfreetvnew.fun/series/game-of-thrones-season-4/',
         'reference_url': 'https://projectfreetvnew.fun/series/game-of-thrones-season-4/'},
        {'has_video': True,
         'url': 'https://projectfreetvnew.fun/series/game-of-thrones/',
         'reference_url': 'https://projectfreetvnew.fun/series/game-of-thrones/'},
        {'has_video': True,
         'url': 'https://w2.putlockers.co/movie/game-of-thrones/',
         'reference_url': 'https://w2.putlockers.co/movie/game-of-thrones/'},
        {'has_video': True,
         'url': 'https://ww1.123moviesfree.net/season/game-of-thrones-season-2-1621',
         'reference_url': 'https://ww1.123moviesfree.net/season/game-of-thrones-season-2-1621'},
        {'has_video': True,
         'url': 'https://nyafilmer9.com/grimm/',
         'reference_url': 'https://nyafilmer9.com/grimm/'},
        {'has_video': True,
         'url': 'https://cmovies.online//film/no-time-to-die',
         'reference_url': 'https://cmovies.online//film/no-time-to-die'},
        {'has_video': True,
         'url': 'https://bmovies.vip/film/game-of-thrones-the-last-watch-31141/',
         'reference_url': 'https://bmovies.vip/film/game-of-thrones-the-last-watch-31141/'},
        {'has_video': True,
         'url': 'https://wwv.la123movies.com/movie/game-of-thrones-the-last-watch/',
         'reference_url': 'https://wwv.la123movies.com/movie/game-of-thrones-the-last-watch/'},
        {'has_video': True,
         'url': 'https://www.fmovies.top/movies/game-of-thrones-the-story-so-far/',
         'reference_url': 'https://www.fmovies.top/movies/game-of-thrones-the-story-so-far/'},
        {'has_video': True,
         'url': 'https://fmovies.pink/movie/no-time-to-die/BuxL2CKT/UZfMbdGu-watch-online-for-free.html',
         'reference_url': 'https://fmovies.pink/movie/no-time-to-die/BuxL2CKT-watch-online-for-free.html'},
        {'has_video': True,
         'url': 'https://w1.1-23movies.cc/watch-online/grimm-season-1-crp/episode/001',
         'reference_url': 'https://w1.1-23movies.cc/watch-online/grimm-season-1-crp/episode/001'},
        {'has_video': True,
         'url': 'https://yomovies.bz/no-time-to-die-2021-Watch-online-full-movie/',
         'reference_url': 'https://yomovies.bz/no-time-to-die-2021-Watch-online-full-movie/'},
        {'has_video': True,
         'url': 'https://ww3.watch0123movies.org/seasons/watch-game-of-thrones-season-4-online-free/',
         'reference_url': 'https://ww3.watch0123movies.org/seasons/watch-game-of-thrones-season-4-online-free/'},
        {'has_video': True,
         'url': 'https://123moviefree.sc/season/game-of-thrones-season-5/',
         'reference_url': 'https://123moviefree.sc/season/game-of-thrones-season-5/'},
        {'has_video': True,
         'url': 'https://123movieshub.fr/movies/game-of-thrones-a-day-in-the-life-2015/',
         'reference_url': 'https://123movieshub.fr/movies/game-of-thrones-a-day-in-the-life-2015/'},
        {'has_video': True,
         'url': 'https://www.123-movies.gdn/game-of-thrones-the-story-so-far-watch-free/',
         'reference_url': 'https://www.123-movies.gdn/game-of-thrones-the-story-so-far-watch-free/'},
        {'has_video': True,
         'url': 'https://m4uhd.net/watch-movie-ofdww-no-time-to-die-2021-movie-online-free-m4ufree.html',
         'reference_url': 'https://m4uhd.net/watch-movie-ofdww-no-time-to-die-2021-movie-online-free-m4ufree.html'},
        {'has_video': True,
         'url': 'https://cmovies.online//film/nobody',
         'reference_url': 'https://cmovies.online//film/nobody'},
        {'has_video': True,
         'url': 'https://ww1.123moviesfree.net/season/game-of-thrones-season-6-11494',
         'reference_url': 'https://ww1.123moviesfree.net/season/game-of-thrones-season-6-11494'},
        {'has_video': True,
         'url': 'https://ww3.watch0123movies.org/movies/watch-game-of-thrones-the-last-watch-online-free/',
         'reference_url': 'https://ww3.watch0123movies.org/movies/watch-game-of-thrones-the-last-watch-online-free/'},
        {'has_video': True,
         'url': 'https://www11.123movieshub.one/tv/game-of-thrones-season-6/',
         'reference_url': 'https://www11.123movieshub.one/tv/game-of-thrones-season-6/'},
        {'has_video': True,
         'url': 'https://ww1.123movies.link/series/9tAZB2Rj/medzPXaF-grimm-season-1',
         'reference_url': 'https://ww1.123movies.link/series/9tAZB2Rj-grimm-season-1'},
        {'has_video': True,
         'url': 'https://movies123.show/tv-show/grimm-season-5/bvDvksEx/pCVmNsXC',
         'reference_url': 'https://movies123.show/tv-show/grimm-season-5/bvDvksEx'},
        {'has_video': True,
         'url': 'https://ev01.to/movie/watch-nobody-online-69184',
         'reference_url': 'https://ev01.to/movie/watch-nobody-online-69184'},
        {'has_video': True,
         'url': 'https://free-putlockers.com/watch-series-online/grimm-season-1/ZOMO8iu3',
         'reference_url': 'https://free-putlockers.com/watch-series-online/grimm-season-1/ZOMO8iu3'},
        {'has_video': True,
         'url': 'https://cmovies.online//film/game-of-thrones-the-story-so-far',
         'reference_url': 'https://cmovies.online//film/game-of-thrones-the-story-so-far'},
        {'has_video': True,
         'url': 'https://www1.solarmovie.cr/tv/grimm-season-3-11852/',
         'reference_url': 'https://www1.solarmovie.cr/tv/grimm-season-3-11852/'},
        {'has_video': True,
         'url': 'https://ww6.putlocker.vip/film/grimm-season-1-crp-10142/',
         'reference_url': 'https://ww6.putlocker.vip/film/grimm-season-1-crp-10142/'},
        {'has_video': True,
         'url': 'https://ww6.putlocker.vip/film/game-of-thrones-season-4-zxb-10393/',
         'reference_url': 'https://ww6.putlocker.vip/film/game-of-thrones-season-4-zxb-10393/'},
        {'has_video': True,
         'url': 'https://w5.putlocker.to/71049-watch-game-of-thrones-the-last-watch-online-for-free-putlockers.html',
         'reference_url': 'https://w5.putlocker.to/71049-watch-game-of-thrones-the-last-watch-online-for-free-putlockers.html'},
        {'has_video': True,
         'url': 'https://vumoo.life/movies/game-of-thrones-the-last-watch/',
         'reference_url': 'https://vumoo.life/movies/game-of-thrones-the-last-watch/'},
        {'has_video': True,
         'url': 'https://mkvking.me/nobody-2021/',
         'reference_url': 'https://mkvking.me/nobody-2021/'},
        {'has_video': True,
         'url': 'https://www4.fusionmovies.to/tv-series/game-of-thrones-season-3/7XcTXzxP/xqdfSpL0',
         'reference_url': 'https://www4.fusionmovies.to/tv-series/game-of-thrones-season-3/7XcTXzxP'},
        {'has_video': True,
         'url': 'https://123moviefree.sc/season/game-of-thrones-season-8/',
         'reference_url': 'https://123moviefree.sc/season/game-of-thrones-season-8/'},
        {'has_video': True,
         'url': 'https://movies123.show/tv-show/grimm-season-4/cKmZh0ey/2vhamxbL',
         'reference_url': 'https://movies123.show/tv-show/grimm-season-4/cKmZh0ey'},
        {'has_video': True,
         'url': 'https://w1.1-23movies.cc/watch-online/game-of-thrones-season-7/episode/001',
         'reference_url': 'https://w1.1-23movies.cc/watch-online/game-of-thrones-season-7/episode/001'},
        {'has_video': True,
         'url': 'https://www1.solarmovie.cr/movie/no-time-to-die-47697/',
         'reference_url': 'https://www1.solarmovie.cr/movie/no-time-to-die-47697/'},
        {'has_video': True,
         'url': 'https://www9.0123movies.com/movies-grimm-season-1-2011-0123movies.html',
         'reference_url': 'https://www9.0123movies.com/movies-grimm-season-1-2011-0123movies.html'},
        {'has_video': True,
         'url': 'https://www.123-movies.gdn/series/game-of-thrones/',
         'reference_url': 'https://www.123-movies.gdn/series/game-of-thrones/'},
        {'has_video': True,
         'url': 'https://www1.solarmovie.cr/tv/grimm-season-6-16087/',
         'reference_url': 'https://www1.solarmovie.cr/tv/grimm-season-6-16087/'},
        {'has_video': True,
         'url': 'https://www11.123movieshub.one/tv/game-of-thrones-season-2/',
         'reference_url': 'https://www11.123movieshub.one/tv/game-of-thrones-season-2/'},
        {'has_video': True,
         'url': 'https://www1.solarmovies.movie/film/game-of-thrones-season-7',
         'reference_url': 'https://www1.solarmovies.movie/film/game-of-thrones-season-7'},
        {'has_video': True,
         'url': 'https://cmovies.online//film/grimm-season-6',
         'reference_url': 'https://cmovies.online//film/grimm-season-6'},
        {'has_video': True,
         'url': 'https://bmovies.vip/film/grimm-season-1-crp-10142/',
         'reference_url': 'https://bmovies.vip/film/grimm-season-1-crp-10142/'},
        {'has_video': True,
         'url': 'https://w2.putlockers.co/movie/game-of-thrones-the-last-watch-1/',
         'reference_url': 'https://w2.putlockers.co/movie/game-of-thrones-the-last-watch-1/'},
        {'has_video': True,
         'url': 'https://cmovies.online//film/game-of-thrones-the-last-watch',
         'reference_url': 'https://cmovies.online//film/game-of-thrones-the-last-watch'},
        {'has_video': True,
         'url': 'https://ymovies.vip/film/game-of-thrones-season-4-zxb-10393/',
         'reference_url': 'https://ymovies.vip/film/game-of-thrones-season-4-zxb-10393/'},
        {'has_video': True,
         'url': 'https://ww6.1todaypk.live/search/page/Game%20of%20Thrones/80',
         'reference_url': 'https://1todaypk.live/search/page/Game%20of%20Thrones/80'},
        {'has_video': True,
         'url': 'https://www1.solarmovie.cr/movie/game-of-thrones-the-story-so-far-36917/',
         'reference_url': 'https://www1.solarmovie.cr/movie/game-of-thrones-the-story-so-far-36917/'},
        {'has_video': True,
         'url': 'https://www1.solarmovies.movie/film/game-of-thrones-season-8',
         'reference_url': 'https://www1.solarmovies.movie/film/game-of-thrones-season-8'},
        {'has_video': True,
         'url': 'https://bmovies.vip/film/game-of-thrones-season-4-zxb-10393/',
         'reference_url': 'https://bmovies.vip/film/game-of-thrones-season-4-zxb-10393/'},
        {'has_video': True,
         'url': 'https://bmovies.vip/film/game-of-thrones-the-story-so-far-30428/',
         'reference_url': 'https://bmovies.vip/film/game-of-thrones-the-story-so-far-30428/'},
        {'has_video': True,
         'url': 'https://xmovies08.org/watch?v=Game_of_Thrones_Kill_the_Boy_2015#video=pr5fCm1Hwp44y_afwzv65vTcju9C79tcCpflxtSo',
         'reference_url': 'https://xmovies08.org/watch?v=Game_of_Thrones_Kill_the_Boy_2015#video=Ik5sPrhWR2wx-3obFOng3LOEDlrxspFySNosUiZSxg'},
        {'has_video': True,
         'url': 'https://vw1.ffmovies.sc/film/game-of-thrones-the-last-watch-2019/',
         'reference_url': 'https://vw1.ffmovies.sc/film/game-of-thrones-the-last-watch-2019/'},
        {'has_video': True,
         'url': 'https://w1.1-23movies.cc/watch-online/game-of-thrones-the-last-watch/episode/001',
         'reference_url': 'https://w1.1-23movies.cc/watch-online/game-of-thrones-the-last-watch/episode/001'},
        {'has_video': True,
         'url': 'https://fmovies.pink/tv-show/game-of-thrones-season-6/4NouOpNO/yks1Z18P',
         'reference_url': 'https://fmovies.pink/tv-show/game-of-thrones-season-6/4NouOpNO'},
        {'has_video': True,
         'url': 'https://www11.123movieshub.one/tv/game-of-thrones-season-5/',
         'reference_url': 'https://www11.123movieshub.one/tv/game-of-thrones-season-5/'},
        {'has_video': True,
         'url': 'https://w1.1-23movies.cc/watch-online/game-of-thrones-season-5-bsm/episode/001',
         'reference_url': 'https://w1.1-23movies.cc/watch-online/game-of-thrones-season-5-bsm/episode/001'},
        {'has_video': True,
         'url': 'https://www1.solarmovies.movie/film/game-of-thrones-season-5-bsm',
         'reference_url': 'https://www1.solarmovies.movie/film/game-of-thrones-season-5-bsm'},
        {'has_video': True,
         'url': 'https://ymovies.vip/film/game-of-thrones-season-5-bsm-10008/',
         'reference_url': 'https://ymovies.vip/film/game-of-thrones-season-5-bsm-10008/'},
        {'has_video': True,
         'url': 'https://fmovies.vision/movie/3733-game-of-thrones-the-last-watch-fmovies.html',
         'reference_url': 'https://fmovies.vision/movie/3733-game-of-thrones-the-last-watch-fmovies.html'},
        {'has_video': True,
         'url': 'https://www11.123movieshub.one/tv/game-of-thrones-season-7/',
         'reference_url': 'https://www11.123movieshub.one/tv/game-of-thrones-season-7/'},
        {'has_video': True,
         'url': 'https://w1.1-23movies.cc/watch-online/grimm-season-6/episode/001',
         'reference_url': 'https://w1.1-23movies.cc/watch-online/grimm-season-6/episode/001'},
        {'has_video': True,
         'url': 'https://123moviesd.com/game-of-thrones-the-last-watch/',
         'reference_url': 'https://123moviesd.com/game-of-thrones-the-last-watch/'},
        {'has_video': True,
         'url': 'https://vw1.ffmovies.sc/tv/game-of-thrones-season-2/',
         'reference_url': 'https://vw1.ffmovies.sc/tv/game-of-thrones-season-2/'},
        {'has_video': True,
         'url': 'https://ww2.m4ufree.com/watch-grimm-11624-tvshow-online-free-m4ufree.html',
         'reference_url': 'https://ww2.m4ufree.com/watch-grimm-11624-tvshow-online-free-m4ufree.html'},
        {'has_video': True,
         'url': 'https://filminvazio.hu/videa-film/grimm/',
         'reference_url': 'https://filminvazio.hu/videa-film/grimm/'},
        {'has_video': True,
         'url': 'https://fmovies.vision/movie/4306-no-time-to-die-fmovies.html',
         'reference_url': 'https://fmovies.vision/movie/4306-no-time-to-die-fmovies.html'},
        {'has_video': True,
         'url': 'https://123movieshub.fr/tvshows/grimm-2011/',
         'reference_url': 'https://123movieshub.fr/tvshows/grimm-2011/'},
        {'has_video': True,
         'url': 'https://ww2.putlockernew.site/watch-movie/nobody-2021_cw38oa8bg/37e3440-full-movie-online',
         'reference_url': 'https://ww2.putlockernew.site/watch-movie/nobody-2021_cw38oa8bg/37e3440-full-movie-online'},
        {'has_video': True,
         'url': 'https://1movies.life/series/game-of-thrones-season-2/113776',
         'reference_url': 'https://1movies.life/series/game-of-thrones-season-2/113776'},
        {'has_video': True,
         'url': 'https://123moviesgo.club/tvshows/game-of-thrones/',
         'reference_url': 'https://123moviesgo.club/tvshows/game-of-thrones/'},
        {'has_video': True,
         'url': 'https://www1.solarmovies.movie/film/grimm-season-5-tzy',
         'reference_url': 'https://www1.solarmovies.movie/film/grimm-season-5-tzy'},
        {'has_video': True,
         'url': 'https://www.123movieshd.icu/series/game-of-thrones-season-5/',
         'reference_url': 'https://www.123movieshd.icu/series/game-of-thrones-season-5/'},
        {'has_video': True,
         'url': 'https://jexmovie.com/watch_Game_of_Thrones_S3_E3_2013.html#video=Wv0tZCaKKX1suBJjw1ZB9lS4fudFLHmSvyTstw',
         'reference_url': 'https://jexmovie.com/watch_Game_of_Thrones_S3_E3_2013.html'}
    ]

    start = time.time()
    for url_element in urls_list:
        site = url_element['url']
        while not threading.active_count() < concurrent_threads:
            continue
        sys.stdout = original_stdout
        print(f"Launching medialookup on url : {site}")

        time.sleep(1)
        p = threading.Thread(target=worker_medialookup, args=[site, url, headers_medialookup])
        p.start()

    while threading.active_count() != 1:
        continue

    end = time.time()

    sys.stdout = original_stdout
    print(f'Execution time : {end - start}')

    with open(file_simple, 'a') as f:
        sys.stdout = f
        print(f'Final positives_list : {positives_list}')
        print(f'Length positives_list : {len(positives_list)}')


if __name__ == '__main__':
    concurrent_threads = int(os.getenv("CONCURRENT_THREADS"))
    current_dt = str(datetime.utcnow())
    api_token = os.getenv("API_TOKEN")
    file_complete = f'{current_dt}-completeLogs.txt'
    file_simple = f'{current_dt}-simpleLogs.txt'
    original_stdout = sys.stdout
    url = os.getenv("URL")
    positives_list = []
    urls_list = []
    exec_list = []
    main()
