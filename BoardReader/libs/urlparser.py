# -*- coding: utf-8 -*-
# Based on (root)/trunk/xbmc-addons/src/plugin.video.polishtv.live/hosts/ @ 419 - Wersja 636

###################################################
# LOCAL import
###################################################
import pCommon
import maxvideoapi
#, anyfiles


###################################################
# FOREIGN import
###################################################
import re
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from Components.config import config

###################################################



class urlparser:
    def __init__(self):    
        self.cm = pCommon.common()
        self.pp = pageParser()

    def hostSelect(self, v):
        hostUrl = False
        i = 0
        if len(v) > 0:
            valTab = []
            for e in (v.values() if type(v) is dict else v):
                i=i+1
                valTab.append(str(i) + '. ' + self.getHostName(e, True))
            item = d.select("Wybor hostingu", valTab)
            if item >= 0: 
                hostUrl = v[item]
            else: 
                print('Brak linkow','Przykro nam, ale nie znalezlismy zadnego linku do video.', 'Sproboj ponownie za jakis czas')
        return hostUrl

    def getItemTitles(self, table):
        out = []
        for i in range(len(table)):
            value = table[i]
            out.append(value[0])
        return out

    def getHostName(self, url, nameOnly = False):
        hostName = ''
        match = re.search('http://(?:www.)?(.+?)/',url)
        if match:
            hostName = match.group(1)
            if (nameOnly):
                n = hostName.split('.')
                hostName = n[-2]
        return hostName
        
    def checkHostSupport(self, url):
        # -1 - not supported
        #  0 - unknown
        #  1 - supported
        
        ret = 0
        host = self.getHostName(url)
        print("video hosted by: " + host)
        print(url)

        if host == 'putlocker.com':
            ret = 1
        elif host == 'sockshare.com':
            ret = 1
        elif host == 'megustavid.com':
            ret = 1
        elif host == 'hd3d.cc':
            ret = 1
        elif host == 'sprocked.com':
            ret = 1
        elif host == 'odsiebie.pl':
            ret = 1
        elif host == 'wgrane.pl':
            ret = 1
        elif host == 'cda.pl':
            ret = 1
        elif host == 'maxvideo.pl' or host == 'nextvideo.pl':
            ret = 1
        elif host == 'video.anyfiles.pl':
            ret = 1
        elif host == 'videoweed.es' or host == 'videoweed.com' or host == 'embed.videoweed.es' or host == 'embed.videoweed.com':
            ret = 1
        elif host== 'novamov.com' or host == 'embed.novamov.com':
            ret = 1
        elif host== 'nowvideo.eu' or host == 'embed.nowvideo.eu':
            ret = 1
        elif host== 'rapidvideo.com':
            ret = 1
        elif host== 'videoslasher.com':
            ret = 1
        elif host== 'dailymotion.com':
            ret = 1
        elif host== 'video.sibnet.ru':
            ret = 1
        elif host== 'vk.com':
            ret = 1
        elif host== 'anime-shinden.info':
            ret = 1
        elif host== 'content.peteava.ro':
            ret = 1
        elif host== 'i.vplay.ro':
            ret = 1
        elif host== 'nonlimit.pl' or host == 'streamo.tv':
            ret = 1
        elif host== 'divxstage.eu' or host == 'movshare.net':
            ret = 1
        elif host== 'embed.movshare.net' or host == 'embed.divxstage.eu':
            ret = 1
        elif host== 'tubecloud.net' or host == 'played.to':
            ret = 1
        elif host== 'freedisc.pl':
            ret = 1
        elif host== 'dwn.so':
            ret = 1
        elif host== 'mightyupload.com':
            ret = 1
        elif host== 'ginbig.com':
            ret = 1
        elif host== 'qfer.net':
            ret = 1
        elif host== 'streamcloud.eu':
            ret = 1
        elif host== 'limevideo.net' or host == 'donevideo.com':
            ret = 1
        elif host== 'scs.pl':
            ret = 1
        elif host== 'youwatch.org':
            ret = 1
        elif host== 'allmyvideos.net':
            ret = 1

        return ret

    def getVideoLink(self, url):
        nUrl=''
        host = self.getHostName(url)
        print("video hosted by: " + host)
        print(url)

        if host == 'putlocker.com':
            nUrl = self.pp.parserPUTLOCKER(url)
        if host == 'sockshare.com':
            nUrl = self.pp.parserSOCKSHARE(url)
        if host == 'megustavid.com':
            nUrl = self.pp.parserMEGUSTAVID(url)
        if host == 'hd3d.cc':
            nUrl = self.pp.parserHD3D(url)
        if host == 'sprocked.com':
            nUrl = self.pp.parserSPROCKED(url)
        if host == 'odsiebie.pl':
            nUrl = self.pp.parserODSIEBIE(url)
        if host == 'wgrane.pl':
            nUrl = self.pp.parserWGRANE(url)
        if host == 'cda.pl':
            nUrl = self.pp.parserCDA(url)
        if host == 'maxvideo.pl' or host == 'nextvideo.pl':
            nUrl = self.pp.parserMAXVIDEO(url)
        if host == 'video.anyfiles.pl':
            nUrl = self.pp.parserANYFILES(url)
        if host == 'videoweed.es' or host == 'videoweed.com' or host == 'embed.videoweed.es' or host == 'embed.videoweed.com':
            nUrl = self.pp.parserVIDEOWEED(url)
        if host== 'novamov.com' or host == 'embed.novamov.com':
            nUrl = self.pp.parserNOVAMOV(url)
        if host== 'nowvideo.eu' or host == 'embed.nowvideo.eu':
            nUrl = self.pp.parserNOWVIDEO(url)
        if host== 'rapidvideo.com':
            nUrl = self.pp.parserRAPIDVIDEO(url)
        if host== 'videoslasher.com':
            nUrl = self.pp.parserVIDEOSLASHER(url)
        if host== 'dailymotion.com':
            nUrl = self.pp.parserDAILYMOTION(url)
        if host== 'video.sibnet.ru':
            nUrl = self.pp.parserSIBNET(url)
        if host== 'vk.com':
            nUrl = self.pp.parserVK(url)
        if host== 'anime-shinden.info':
            nUrl = url
        if host== 'content.peteava.ro':
            nUrl = self.pp.parserPETEAVA(url)
        if host== 'i.vplay.ro':
            nUrl = self.pp.parserVPLAY(url)
        if host== 'nonlimit.pl' or host == 'streamo.tv':
            nUrl = self.pp.parserIITV(url)
        if host== 'divxstage.eu' or host == 'movshare.net':
            nUrl = self.pp.parserDIVXSTAGE(url)
        if host== 'embed.movshare.net' or host == 'embed.divxstage.eu':
            nUrl = self.pp.parserembedDIVXSTAGE(url)
        if host== 'tubecloud.net' or host == 'played.to':
            nUrl = self.pp.parserTUBECLOUD(url)
        if host== 'freedisc.pl':
            nUrl = self.pp.parserFREEDISC(url)
        if host== 'dwn.so':
            nUrl = self.pp.parserDWN(url)
        if host== 'mightyupload.com':
            nUrl = self.pp.parserMIGHTYUPLOAD(url)
        if host== 'ginbig.com':
            nUrl = self.pp.parserGINBIG(url)
        if host== 'qfer.net':
            nUrl = self.pp.parserQFER(url)
        if host== 'streamcloud.eu':
            nUrl = self.pp.parserSTREAMCLOUD(url)
        if host== 'limevideo.net' or host == 'donevideo.com':
            nUrl = self.pp.parserLIMEVIDEO(url)
        if host== 'scs.pl':
            nUrl = self.pp.parserSCS(url)
        if host== 'youwatch.org':
            nUrl = self.pp.parserYOUWATCH(url)
        if host== 'allmyvideos.net':
            nUrl = self.pp.parserALLMYVIDEOS(url)
        return nUrl

class pageParser:
    def __init__(self):
        self.cm = pCommon.common()
        self.captcha = captchaParser()
        
        #config
        self.COOKIE_PATH = resolveFilename(SCOPE_PLUGINS, 'Extensions/IPTVPlayer/cache/')
        self.hd3d_login = config.plugins.iptvplayer.hd3d_login.value
        self.hd3d_password = config.plugins.iptvplayer.hd3d_password.value
        
        self.maxvideo_login = config.plugins.iptvplayer.maxvideo_login.value
        self.maxvideo_password = config.plugins.iptvplayer.maxvideo_password.value

    def parserPUTLOCKER(self,url):
        query_data = { 'url': url.replace('file', 'embed'), 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        r = re.search('value="(.+?)" name="fuck_you"', link)
        if r:
            self.COOKIEFILE = self.COOKIE_PATH + "putlocker.cookie"
            query_data = { 'url': url.replace('file', 'embed'), 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True }
            postdata = {'fuck_you' : r.group(1), 'confirm' : 'Close Ad and Watch as Free User'}
            link = self.cm.getURLRequestData(query_data, postdata)
            match = re.compile("playlist: '(.+?)'").findall(link)
            if len(match) > 0:
                url = "http://www.putlocker.com" + match[0]
                query_data = { 'url': url, 'use_host': False, 'use_cookie': True, 'save_cookie': False, 'load_cookie': True, 'cookiefile': self.COOKIEFILE, 'use_post': False, 'return_data': True }
                link = self.cm.getURLRequestData(query_data)
                match = re.compile('</link><media:content url="(.+?)" type="video').findall(link)
                if len(match) > 0:
                    url = match[0].replace('&amp;','&')
                    return url
                else:
                    return False
            else:
                return False
        else:
            return False

    def parserMEGUSTAVID(self,url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match = re.compile('value="config=(.+?)">').findall(link)
        if len(match) > 0:
            p = match[0].split('=')
            url = "http://megustavid.com/media/nuevo/player/playlist.php?id=" + p[1]
            query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
            link = self.cm.getURLRequestData(query_data)
            match = re.compile('<file>(.+?)</file>').findall(link)
            if len(match) > 0:
                return match[0]
            else:
                return False
        else:
            return False

    def parserHD3D(self,url):
        if not 'html' in url:
            url = url + '.html?i'
        else:
            url = url
        username = self.hd3d_login
        password = self.hd3d_password
        urlL = 'http://hd3d.cc/login.html'
        self.COOKIEFILE = self.COOKIE_PATH + "hd3d.cookie"
        query_dataL = { 'url': urlL, 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True }
        postdata = {'user_login': username, 'user_password': password}
        data = self.cm.getURLRequestData(query_dataL, postdata)
        query_data = { 'url': url, 'use_host': False, 'use_cookie': True, 'save_cookie': False, 'load_cookie': True, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match = re.compile("""url: ["'](.+?)["'],.+?provider:""").findall(link)
        if len(match) > 0:
            ret = match[0]
        else:
         ret = False
        return ret

    def parserSPROCKED(self,url):
        url = url.replace('embed', 'show')
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match = re.search("""url: ['"](.+?)['"],.*\nprovider""",link)
        if match:
            return match.group(1)
        else:
            return False

    def parserODSIEBIE(self,url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        try:
            (v_ext, v_file, v_dir, v_port, v_host) = re.search("\|\|.*SWFObject",link).group().split('|')[40:45]
            url = "http://%s.odsiebie.pl:%s/d/%s/%s.%s" % (v_host, v_port, v_dir, v_file, v_ext);
        except:
            url = False
        return url

    def parserWGRANE(self,url):
        nUrl = 'http://m.wgrane.pl/video?v=' + url[-32:]
        query_data = { 'url': nUrl, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        #<a href='http://s1.wgrane.pl/mobile/video/171545?time=1335636021'>Odtwórz</a>
        match = re.search("""Dodano: <span class='black'>.+?</span></h3><div class='clear'></div><h1><a href='(.+?)'>Odtwórz</a>""",link)
        if match:
            return match.group(1)
        else:
            return False

    def parserCDA(self,url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match = re.search("""file: ['"](.+?)['"],""",link)
        if match:
            return match.group(1)
        else:
            return False

    def parserDWN(self,url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        match = re.compile('src="(.+?)" width=').findall(self.cm.getURLRequestData(query_data))
        if len(match) > 0:
            query_data1 = { 'url': match[0], 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
            match1 = re.compile("play4.swf(.+?)',").findall(self.cm.getURLRequestData(query_data1))
            if len(match1) > 0:
                query_data2 = { 'url': 'http://st.dwn.so/xml/videolink.php' + match1[0], 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
                match2 = re.compile('un="(.+?),0').findall(self.cm.getURLRequestData(query_data2))
                if len(match2) > 0:
                    linkvideo = 'http://' + match2[0]
                    return linkvideo
                else:
                    return False
            else:
                return False
        else:
            return False

    def parserANYFILES(self,url):
        self.anyfiles = anyfiles.serviceParser()
        retVal = self.anyfiles.getVideoUrl(url)
        return retVal

    def parserWOOTLY(self,url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        c = re.search("""c.value="(.+?)";""",link)
        if c:
            cval = c.group(1)
        else:
            return False
        match = re.compile("""<input type=['"]hidden['"] value=['"](.+?)['"].+?name=['"](.+?)['"]""").findall(link)
        if len(match) > 0:
            postdata = {};
            for i in range(len(match)):
                if (len(match[i][0])) > len(cval):
                    postdata[cval] = match[i][1]
                else:
                    postdata[match[i][0]] = match[i][1]
            self.COOKIEFILE = self.COOKIE_PATH + "wootly.cookie"
            query_data = { 'url': url, 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True }
            link = self.cm.getURLRequestData(query_data, postdata)
            match = re.search("""<video.*\n.*src=['"](.+?)['"]""",link)
            if match:
                return match.group(1)
            else:
                return False
        else:
            return False

    def parserMAXVIDEO(self, url):
            api = maxvideoapi.API()

            videoUrl = ''
            videoHash = url.split('/')[-1]
            
            login = api.Login(self.maxvideo_login, self.maxvideo_password)
            if (login):
                cookiefile = self.COOKIE_PATH + "maxvideo.cookie"
            else:
                cookiefile = ''
            videoUrl = api.getVideoUrl(videoHash, cookiefile)
            return videoUrl

    def parserVIDEOWEED(self, url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match_domain = re.compile('flashvars.domain="(.+?)"').findall(link)
        match_file = re.compile('flashvars.file="(.+?)"').findall(link)
        match_filekey = re.compile('flashvars.filekey="(.+?)"').findall(link)
        if len(match_domain) > 0 and len(match_file) > 0 and len(match_filekey) > 0:
            get_api_url = ('%s/api/player.api.php?user=undefined&codes=1&file=%s&pass=undefined&key=%s') % (match_domain[0], match_file[0], match_filekey[0])
            link_api = { 'url': get_api_url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
            link = self.cm.getURLRequestData(link_api)
            match = re.compile("url=(.+?)&title").findall(link)
            if len(match) > 0:
                linkVideo = match[0]
                print ('linkVideo ' + linkVideo)
                return linkVideo
            else:
                return False
        else:
            return False

    def parserNOVAMOV(self, url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match_file = re.compile('flashvars.file="(.+?)";').findall(link)
        match_key = re.compile('flashvars.filekey="(.+?)";').findall(link)
        if len(match_file) > 0 and len(match_key) > 0:
            get_api_url = ('http://www.novamov.com/api/player.api.php?key=%s&user=undefined&codes=1&pass=undefined&file=%s') % (match_key[0], match_file[0])
            query_data = { 'url': get_api_url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
            link = self.cm.getURLRequestData(query_data)
            match_url = re.compile('url=(.+?)&title').findall(link)
            if len(match_url) > 0:
                return match_url[0]
            else:
                return False
        else:
            return False

    def parserNOWVIDEO(self, url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match_file = re.compile('flashvars.file="(.+?)";').findall(link)
        match_key = re.compile('flashvars.filekey="(.+?)";').findall(link)
        if len(match_file) > 0 and len(match_key) > 0:
            get_api_url = ('http://www.nowvideo.eu/api/player.api.php?codes=1&key=%s&user=undefined&pass=undefined&file=%s') % (match_key[0], match_file[0])
            query_data = { 'url': get_api_url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
            link_api = self.cm.getURLRequestData(query_data)
            match_url = re.compile('url=(.+?)&title').findall(link_api)
            if len(match_url) > 0:
                return match_url[0]
            else:
                return False
        else:
            return False

    def parserSOCKSHARE(self,url):
        query_data = { 'url': url.replace('file', 'embed'), 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        r = re.search('value="(.+?)" name="fuck_you"', link)
        if r:
            self.COOKIEFILE = self.COOKIE_PATH + "sockshare.cookie"
            postdata = {'fuck_you' : r.group(1), 'confirm' : 'Close Ad and Watch as Free User'}
            query_data = { 'url': url.replace('file', 'embed'), 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True }
            link = self.cm.getURLRequestData(query_data, postdata)
            match = re.compile("playlist: '(.+?)'").findall(link)
            if len(match) > 0:
                url = "http://www.sockshare.com" + match[0]
                query_data = { 'url': url, 'use_host': False, 'use_cookie': True, 'save_cookie': False, 'load_cookie': True, 'cookiefile': self.COOKIEFILE, 'use_post': False, 'return_data': True }
                link = self.cm.getURLRequestData(query_data)
                match = re.compile('</link><media:content url="(.+?)" type="video').findall(link)
                if len(match) > 0:
                    url = match[0].replace('&amp;','&')
                    return url
                else:
                    return False
            else:
                return False
        else:
            return False

    def parserRAPIDVIDEO(self,url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        #"jw_set('http://176.9.7.56:8080/v/bc71afa327b1351b2d9abe5827aa97dc/240/130219976TEBYU50H0NN.flv','240p','176.9.7.56');"
        match = re.compile("jw_set\('(.+?)','(.+?)','.+?'\);").findall(link)
        if len(match) > 0:
            return match[0][0]
        else:
            return False

    def parserVIDEOSLASHER(self, url):
        self.COOKIEFILE = self.COOKIE_PATH + "videoslasher.cookie"
        query_data = { 'url': url.replace('embed', 'video'), 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True }
        postdata = {'confirm': 'Close Ad and Watch as Free User', 'foo': 'bar'}
        data = self.cm.getURLRequestData(query_data, postdata)

        match = re.compile("playlist: '/playlist/(.+?)'").findall(data)
        if len(match)>0:
            query_data = { 'url': 'http://www.videoslasher.com//playlist/' + match[0], 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': True, 'cookiefile': self.COOKIEFILE,  'use_post': True, 'return_data': True }
            data = self.cm.getURLRequestData(query_data)
            match = re.compile('<title>Video</title>.*?<media:content url="(.+?)"').findall(data)
            if len(match)>0:
                sid = self.cm.getCookieItem(self.COOKIEFILE,'authsid')
                if sid != '':
                    streamUrl = match[0] + '|Cookie="authsid=' + sid + '"'
                    return streamUrl
                else:
                    return False
            else:
                return False
        else:
            return False

    def parserDAILYMOTION(self,url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match = re.search('stream_h264_url":"(.+?)"',link)
        if match:
            movie = match.group(1).replace('\\', '')
            return movie
        else:
            return False

    def parserSIBNET(self, url):
        mid = re.search('videoid=(.+?)$',url)
        ourl = 'http://video.sibnet.ru'
        movie = 'http://video.sibnet.ru/v/qwerty/'+mid.group(1)+'.mp4?start=0'
        query_data = { 'url': ourl+'/video'+mid.group(1), 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match = re.search("'file':'(.+?)'",link)
        if match:
            return ourl+match.group(1)
        else:
            return False

    def parserVK(self, url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        video_host = re.search("var video_host = '(.+?)';", link)
        video_uid = re.search("var video_uid = '(.+?)';", link)
        video_vtag = re.search("var video_vtag = '(.+?)';", link)
        if video_host and video_uid and video_vtag:
            movie = video_host.group(1)+'u'+video_uid.group(1)+'/videos/'+video_vtag.group(1)+'.720.mp4'
            return movie
        else:
            return False

    def parserPETEAVA(self, url):
        mid = re.search("hd_file=(.+?_high.mp4)&", url)
        movie = "http://content.peteava.ro/video/"+mid.group(1)+"?token=PETEAVARO"
        return movie

    def parserVPLAY(self, url):
        vid = re.search("key=(.+?)$", url)
        query_data = { 'url': 'http://www.vplay.ro/play/dinosaur.do', 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True }
        postdata = {'key':vid.group(1)}
        link = self.cm.getURLRequestData(query_data, postdata)
        movie = re.search("nqURL=(.+?)&", link)
        return movie.group(1)

    def parserIITV(self, url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        query_data_non = { 'url': url + '.html?i&e&m=iitv', 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        if 'streamo' in url:
            match = re.compile("url: '(.+?)',").findall(self.cm.getURLRequestData(query_data))
        if 'nonlimit' in url:
            match = re.compile('url: "(.+?)",     provider:').findall(self.cm.getURLRequestData(query_data_non))
        if len(match) > 0:
            linkVideo = match[0]
            print ('linkVideo ' + linkVideo)
            return linkVideo
        else:
            print ('Przepraszamy','Obecnie zbyt dużo osób ogląda film za pomocą', 'darmowego playera premium.', 'Sproboj ponownie za jakis czas')
        return False

    def parserDIVXSTAGE(self,url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        video_host = re.search('flashvars.domain="(.+?)";', link)
        video_file = re.search('flashvars.file="(.+?)";', link)
        video_filekey = re.search('flashvars.filekey="(.+?)";', link)
        video_cid = re.search('flashvars.cid="(.+?)";', link)
        if video_file and video_filekey and video_cid > 0:
            url = video_host.group(1) + "/api/player.api.php?cid2=undefined&file=" + video_file.group(1) + "&key=" + video_filekey.group(1) + "&cid=" + video_cid.group(1) + "&cid3=undefined&user=undefined&pass=undefined"
            query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
            link = self.cm.getURLRequestData(query_data)
            match = re.compile('url=(.+?)&title=').findall(link)
            if len(match) > 0:
                linkvideo = match[0]
                return linkvideo
            else:
                return False
        else:
            return False

    def parserembedDIVXSTAGE(self,url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        video_host = re.search('flashvars.domain="(.+?)";', link)
        video_file = re.search('flashvars.file="(.+?)";', link)
        video_filekey = re.search('flashvars.filekey="(.+?)";', link)
        if video_file and video_filekey > 0:
            url = video_host.group(1) + "/api/player.api.php??cid2=undefined&cid3=undefined&cid=undefined&key=" + video_filekey.group(1) + "&user=undefined&pass=undefined&file=" + video_file.group(1)
            query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
            link = self.cm.getURLRequestData(query_data)
            match = re.compile('url=(.+?)&title=').findall(link)
            if len(match) > 0:
                linkvideo = match[0]
                return linkvideo
            else:
                return False
        else:
            return False

    def parserTUBECLOUD(self,url):
        self.COOKIEFILE = self.COOKIE_PATH + "tubecloud.cookie"
        query_data = { 'url': url, 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        ID = re.search('name="id" value="(.+?)">', link)
        FNAME = re.search('name="fname" value="(.+?)">', link)
        HASH = re.search('name="hash" value="(.+?)">', link)
        if ID and FNAME and HASH > 0:
            xbmc.sleep(10500)
            postdata = {'fname' : FNAME.group(1), 'hash' : HASH.group(1), 'id' : ID.group(1), 'imhuman' : 'Proceed to video', 'op' : 'download1', 'referer' : url, 'usr_login' : '' }
            query_data = { 'url': url, 'use_host': False, 'use_cookie': True, 'save_cookie': False, 'load_cookie': True, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True }
            link = self.cm.getURLRequestData(query_data, postdata)
            match = re.compile('file: "(.+?)"').findall(link)
            if len(match) > 0:
                linkvideo = match[0]
                return linkvideo
            else:
                return False
        else:
            return False

    def parserFREEDISC(self, url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        match = re.compile('controller.player.loadMoviePlayer(.+?);').findall(self.cm.getURLRequestData(query_data))
        if len(match) > 0:
            linkVideo = 'http://freedisc.pl/streaming/video.mp4?fileID=' + match[0].replace('(', '').replace(')', '') + '&start=0'
            print ('linkVideo ' + linkVideo)
            return linkVideo
        else:
            return False

    def parserMIGHTYUPLOAD(self,url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        ID = re.search('name="id" value="(.+?)">', link)
        RAND = re.search('name="rand" value="(.+?)">', link)
        if ID and RAND > 0:
            postdata = {'down_direct' : '1', 'id' : ID.group(1), 'method_free' : '', 'method_premium' : '', 'op' : 'download2', 'rand' : RAND.group(1), 'referer' : url }
            query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True }
            link = self.cm.getURLRequestData(query_data, postdata)
            match = re.compile('<a href="(.+?)">Download the file</a>').findall(link)
            if len(match) > 0:
                linkvideo = match[0]
                return linkvideo
            else:
                return False
        else:
            return False

    def parserGINBIG(self,url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        ID = re.search('name="id" value="(.+?)">', link)
        FNAME = re.search('name="fname" value="(.+?)">', link)
        if ID and FNAME > 0:
            postdata = { 'op': 'download1', 'id': ID.group(1), 'fname': FNAME.group(1), 'referer': url, 'method_free': 'Free Download', 'usr_login': '' }
            query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True }
            link = self.cm.getURLRequestData(query_data, postdata)
            data = link.replace('|', '<>')
            PL = re.search('<>player<>(.+?)<>flvplayer<>', data)
            HS = re.search('video<>(.+?)<>(.+?)<>file<>', data)
            if PL and HS > 0:
                linkVideo = 'http://' + PL.group(1) + '.ginbig.com:' + HS.group(2) + '/d/' + HS.group(1) + '/video.mp4?start=0'
                print ('linkVideo ' + linkVideo)
                return linkVideo
            else:
                return False
        else:
            return False

    def parserQFER(self, url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        match = re.compile('"PSST",url: "(.+?)"').findall(self.cm.getURLRequestData(query_data))
        if len(match) > 0:
            linkVideo = match[0]
            print ('linkVideo ' + linkVideo)
            return linkVideo
        else:
            return False

    def parserSTREAMCLOUD(self,url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        ID = re.search('name="id" value="(.+?)">', link)
        FNAME = re.search('name="fname" value="(.+?)">', link)
        if ID and FNAME > 0:
            xbmc.sleep(10500)
            postdata = {'fname' : FNAME.group(1), 'hash' : '', 'id' : ID.group(1), 'imhuman' : 'Watch video now', 'op' : 'download1', 'referer' : url, 'usr_login' : '' }
            query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True }
            link = self.cm.getURLRequestData(query_data, postdata)
            match = re.compile('file: "(.+?)"').findall(link)
            if len(match) > 0:
                linkVideo = match[0]
                print ('linkVideo ' + linkVideo)
                return linkVideo
            else:
                return False
        else:
            return False

    def parserLIMEVIDEO(self,url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        ID = re.search('name="id" value="(.+?)">', link)
        FNAME = re.search('name="fname" value="(.+?)">', link)
        if ID and FNAME > 0:
            xbmc.sleep(20500)
            postdata = {'fname' : FNAME.group(1), 'id' : ID.group(1), 'method_free' : 'Continue to Video', 'op' : 'download1', 'referer' : url, 'usr_login' : '' }
            query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True }
            link = self.cm.getURLRequestData(query_data, postdata)
            ID = re.search('name="id" value="(.+?)">', link)
            RAND = re.search('name="rand" value="(.+?)">', link)
            table = self.captcha.textCaptcha(link)
            value = table[0][0] + table [1][0] + table [2][0] + table [3][0]
            code = self.cm.html_entity_decode(value)
            print ('captcha-code :' + code)
            if ID and RAND > 0:
                postdata = {'rand' : RAND.group(1), 'id' : ID.group(1), 'method_free' : 'Continue to Video', 'op' : 'download2', 'referer' : url, 'down_direct' : '1', 'code' : code, 'method_premium' : '' }
                query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True }
                link = self.cm.getURLRequestData(query_data, postdata)
                data = link.replace('|', '<>')
                PL = re.search('<>player<>video<>(.+?)<>(.+?)<>(.+?)<><>(.+?)<>flvplayer<>', data)
                HS = re.search('image<>(.+?)<>(.+?)<>(.+?)<>file<>', data)
                if PL and HS > 0:
                    linkVideo = 'http://' + PL.group(4) + '.' + PL.group(3) + '.' + PL.group(2) + '.' + PL.group(1) + ':' + HS.group(3) + '/d/' + HS.group(2) + '/video.' + HS.group(1)
                    print ('linkVideo :' + linkVideo)
                    return linkVideo
                else:
                    return False
            else:
                return False
        else:
            return False

    def parserSCS(self,url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        ID = re.search('"(.+?)"; ccc', link)
        if ID > 0:
            postdata = {'f' : ID.group(1) }
            query_data = { 'url': 'http://scs.pl/getVideo.html', 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True }
            link = self.cm.getURLRequestData(query_data, postdata)
            match = re.compile("url: '(.+?)',").findall(link)
            if len(match) > 0:
                linkVideo = match[0]
                print ('linkVideo ' + linkVideo)
                return linkVideo
            else:
                print ('Przepraszamy','Obecnie zbyt dużo osób ogląda film za pomocą', 'darmowego playera premium.', 'Sproboj ponownie za jakis czas')
                return False
        else:
            return False

    def parserYOUWATCH(self,url):
        if 'embed' in url:
            Url = url
        else:
            Url = url.replace('org/', 'org/embed-') + '-640x360.html'
        query_data = { 'url': Url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match = re.compile('file: "(.+?)"').findall(link)
        if len(match) > 0:
            linkVideo = match[0]
            print ('linkVideo: ' + linkVideo)
            return linkVideo
        else:
            return False

    def parserALLMYVIDEOS(self,url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        ID = re.search('name="id" value="(.+?)">', link)
        FNAME = re.search('name="fname" value="(.+?)">', link)
        if ID and FNAME > 0:
            xbmc.sleep(10500)
            postdata = {'fname' : FNAME.group(1), 'method_free' : '1', 'id' : ID.group(1), 'x' : '82', 'y' : '13', 'op' : 'download1', 'referer' : url, 'usr_login' : '' }
            query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True }
            link = self.cm.getURLRequestData(query_data, postdata)
            match = re.compile('"file" : "(.+?)",').findall(link)
            if len(match) > 0:
                linkVideo = match[0]
                print ('linkVideo ' + linkVideo)
                return linkVideo
            else:
                return False
        else:
            return False

class captchaParser:
    def __init__(self):
        pass

    def textCaptcha(self, data):
        strTab = []
        valTab = []
        match = re.compile("padding-(.+?):(.+?)px;padding-top:.+?px;'>(.+?)<").findall(data)
        if len(match) > 0:
            for i in range(len(match)):
                value = match[i]
                strTab.append(value[2])
                strTab.append(int(value[1]))
                valTab.append(strTab)
                strTab = []
                if match[i][0] == 'left':
                    valTab.sort(key=lambda x: x[1], reverse=False)
                else:
                    valTab.sort(key=lambda x: x[1], reverse=True)
        return valTab

    def reCaptcha(self, data):
        pass
