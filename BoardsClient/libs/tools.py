# -*- coding: utf-8 -*-
#! /usr/bin/python
#
#sys.path.append('/usr/lib/enigma2/python/Plugins/Extensions/BoardsClient/')

from cookielib import CookieJar
import urllib, urllib2, re, time, os, sys 
from urllib2 import Request, urlopen, URLError, HTTPError
import time
import tarfile
from datetime import datetime
from Components.config import config
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_CONFIG


class CSelOneLink():

    def __init__(self, listOfLinks, getQualiyFun, maxRes):
       self.listOfLinks = listOfLinks
       self.getQualiyFun = getQualiyFun
       self.maxRes = maxRes
       
    def _cmpLinks(self, item1, item2):
        val1 = self.getQualiyFun(item1)
        val2 = self.getQualiyFun(item2)
        
        if val1 < val2:
            return -1
        elif val1 > val2:
            return 1
        else:
            return 0
            
    def getOneLink(self):
        printDBG('getOneLink start')

        sortList = self.listOfLinks[::-1]
        sortList.sort( self._cmpLinks )
            
        if len(self.listOfLinks) < 2:
            return self.listOfLinks
        
        retItem = None
        for item in sortList:
            linkRes = self.getQualiyFun(item)
            if linkRes <= self.maxRes:
                retItem = item
                printDBG('getOneLink use format %d/%d' % (linkRes, self.maxRes) )
                
        if retItem == None:
            retItem = sortList[0]
        
        return [retItem]
# end CSelOneLink

#############################################################
# debugowanie, czyli wypisywanie informacji na ekranie/pliku
#############################################################
# debugowanie
def printDBG( DBGtxt ):
    try:
        from Components.config import config
        DBG = config.plugins.BoardReader.debugprint.value
    except:
        #nie zainicjowany modul Config, sprawdzamy wartosc bezposredio w pliku
        DBG=''
        file = open(resolveFilename(SCOPE_CONFIG, "settings"))
        for line in file:
            if line.startswith('config.plugins.BoardReader.debugprint=' ) :
                DBG=line.split("=")[1].strip()
                break
        #print DBG
    try:
        if DBG == '':
            return
        elif DBG == 'console':
            print DBGtxt
        elif DBG == 'debugfile':
            f = open('/tmp/BoardsClient.dbg', 'a')
            f.write(DBGtxt + '\n')
            f.close
    except:
        pass
        
#####################################################
# get host list based on files in /hosts folder
#####################################################
def GetHostsList():
    printDBG('getHostsList begin')
    HOST_PATH = resolveFilename(SCOPE_PLUGINS, 'Extensions/BoardsClient/forums/')
    lhosts = [] 
    
    fileList = os.listdir( HOST_PATH )
    for wholeFileName in fileList:
        # separate file name and file extension
        fileName, fileExt = os.path.splitext(wholeFileName)
        nameLen = len( fileName )
        if fileExt in ['.pyo', '.pyc', '.py'] and nameLen >  5 and fileName[:5] == 'forum' and fileName.find('_blocked_') == -1:
            if fileName[5:] not in lhosts:
                lhosts.append( fileName[5:] )
                printDBG('BoardsClient.tools.getHostsList add host with fileName: "%s"' % fileName[5:])
    printDBG('BoardsClient.tools.getHostsList end')
    lhosts.sort()
    return lhosts
    
def IsHostEnabled( hostName ):
    hostEnabled  = False
    try:
        exec('if config.plugins.BoardReader.host' + hostName + '.value: hostEnabled = True')
    except:
        hostEnabled = False
    return hostEnabled

#####################################################
# czy mamy wystarczajaco wolnego miejsca?
#####################################################
def FreeSpace(katalog, WymaganeMB):
    try:
        s = os.statvfs(katalog)
        WolneMB=s.f_bavail * s.f_frsize / 1048576
        if WolneMB >= WymaganeMB:
            return True
        else:
            return False
    except:
        return False
        
#####################################################
# rekursywne tworzenie katalogow
#####################################################

def mkdirs(newdir):
    """ Create a directory and all parent folders.
        Features:
        - parent directories will be created
        - if directory already exists, then do nothing
        - if there is another filsystem object with the same name, raise an exception
    """
    printDBG('mkdirs: "%s"' % newdir)
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        raise OSError("cannot create directory, file already exists: '%s'" % newdir)
    else:
        head, tail = os.path.split(newdir)
        if head and not os.path.isdir(head) and not os.path.ismount(head) and not os.path.islink(head):
            mkdirs(head)
        if tail:
            os.mkdir(newdir)

#####################################################
# autoupdate
#####################################################

def GetGITversion():
    try:
        req = urllib2.Request("http://gitorious.org/opli-plugins/opli-plugins/blobs/master/BoardsClient/_version.py")
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        html_doc = str(response.read())
        response.close()
    except:
        html_doc="BLAD"
    printDBG("GetGITversion:" + html_doc)
    #znajdujemy wersje w pliku
    r=re.search( r'version=&quot;(.+)&quot;',html_doc)
    if r:
        znalezione=r.groups(1)
        wersjaGIT=znalezione[0]
        printDBG("Wersja GIT na gitorious: %s" % wersjaGIT)
        return wersjaGIT
    else:
        return "??"

def GetMaster(NaszTarFile="/tmp/plugin.tar.gz"):
    try:
        GITfile = urllib2.urlopen("http://gitorious.org/opli-plugins/opli-plugins/archive-tarball/master")
        output = open(NaszTarFile,'wb')
        output.write(GITfile.read())
        output.close()
        os.system('sync')
        return "OK"
    except:
        if os.path.exists(NaszTarFile):
            os.remove(NaszTarFile)
        return "Błąd pobierania master.tar.gz"
            
def UpdateIPTV_from_GIT(sciezkaTMP="/tmp/"):
    ret = ""
    Porzadki(sciezkaTMP)
    NaszTarFile=sciezkaTMP + 'plugin.tar.gz'
    ret = GetMaster(NaszTarFile)
    if os.path.exists(NaszTarFile) and ret == "OK":
        if not tarfile.is_tarfile(NaszTarFile):
            Porzadki(sciezkaTMP)
            #czasami archiwum nie jest od razu wygenerowane
            time.sleep(5)
            ret = GetMaster(NaszTarFile)
    else:
        time.sleep(5)
        ret = GetMaster(NaszTarFile)
    #jak teraz nie mamy archiwum, to blad
    if ret != "OK":
        return ret
    if not os.path.exists(NaszTarFile):
        return "Pobrany plik master.tar.gz nie znaleziony"
    else:
        if not tarfile.is_tarfile(NaszTarFile):
            #sprobujmy na pale rozpakowac bo mipsy jakies pokastorawne ze skryptow sa. ;)
            os.system('cd ' + sciezkaTMP + '; tar -xzf plugin.tar.gz; sync')
            if not os.path.exists(sciezkaTMP + 'opli-plugins-opli-plugins/BoardsClient'):
                return "Niepoprawny format pliku %s" % NaszTarFile
            else:
                if config.plugins.BoardReader.cleanup.value:
                   os.system('rm -rf /usr/lib/enigma2/python/Plugins/Extensions/BoardsClient/*')
                os.system('cp -rf %sopli-plugins-opli-plugins/BoardsClient/* /usr/lib/enigma2/python/Plugins/Extensions/BoardsClient/' % sciezkaTMP)
                os.system('sync')
                Porzadki(sciezkaTMP)
                return "OK"
        else:
            tar = tarfile.open(NaszTarFile)
            tar.extractall(path= sciezkaTMP)
            os.system('sync')
            if not os.path.exists(sciezkaTMP + 'opli-plugins-opli-plugins/BoardsClient'):
                return "Błąd rozpakowania pliku master.tar.gz"
            else:
                if config.plugins.BoardReader.cleanup.value:
                   os.system('rm -rf /usr/lib/enigma2/python/Plugins/Extensions/BoardsClient/*')
                os.system('cp -rf %sopli-plugins-opli-plugins/BoardsClient/* /usr/lib/enigma2/python/Plugins/Extensions/BoardsClient/' % sciezkaTMP)
                os.system('sync')
                Porzadki(sciezkaTMP)
                return "OK"
    return "Nieznany błąd"
        
def Porzadki(sciezkaTMP="/tmp/"):
    #porzadki w razie czego
    if os.path.exists(sciezkaTMP + 'plugin.tar.gz'):
        os.remove(sciezkaTMP + 'plugin.tar.gz')
    if os.path.exists(sciezkaTMP + 'opli-plugins-opli-plugins'):
        import shutil
        shutil.rmtree(sciezkaTMP + 'opli-plugins-opli-plugins')

                
########################################################
#                     For icon menager
########################################################
def checkIconName(name):
    #check if name is correct 
    nameIsOk = False
    if 36 == len(name) and '.jpg' == name[-4:]:
        #print("Icon name %s is correct" % name)
        try:
            tmp = int(name[:-4], 16)
            nameIsOk = True
        except:
            nameIsOk = False
            pass
    return nameIsOk
    
    
def removeAllIconsFromPath(path):
    print "removeAllIconsFromPath"
    try:
        list = os.listdir(path)
        for item in list:
            filePath = path + '/' + item
            if checkIconName(item) and os.path.isfile(filePath):
                print 'removeAllIconsFromPath img: ' + filePath
                try:
                    os.remove(filePath)
                except error:
                    print "ERROR while removing file %s" % filePath
    except:
        print 'ERROR: in removeAllIconsFromPath'
        pass
    return 
    
def getModifyDeltaDateInDays(fullPath):
    ret = -1
    try:
        modifiedTime = os.path.getatime(fullPath)
        currTime = datetime.now()
        modTime = datetime.fromtimestamp(modifiedTime)
        deltaTime = currTime - modTime
        ret = deltaTime.days
    except:
        ret = -1 
    
    return ret
    
def remove_html_markup(s):
    tag = False
    quote = False
    out = ""

    for c in s:
            if c == '<' and not quote:
                tag = True
            elif c == '>' and not quote:
                tag = False
            elif (c == '"' or c == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + c

    return re.sub('&\w+;', ' ',out)
    

class CSearchHistoryHelper():
    def __init__(self, name):
        printDBG('CSearchHistoryHelper.__init__')
        try:
            printDBG('CSearchHistoryHelper.__init__ name = "%s"' % name)
            self.PATH = config.plugins.BoardReader.SciezkaCache.value + "/SearchHistory"
            self.PATH = self.PATH.replace('//', '/')
            mkdirs(self.PATH)
            self.PATH_FILE = self.PATH + '/' + name + ".txt"

        except:
            printDBG('CSearchHistoryHelper.__init__ EXCEPTION')

    def getHistoryList(self):
        printDBG('CSearchHistoryHelper.getHistoryList from file = "%s"' % self.PATH_FILE)
        historyList = []
    
        try:
            file = open( self.PATH_FILE, 'r' )
            for line in file:
                value = line.replace('\n', '').strip()
                if len(value) > 0:
                    historyList.insert(0, value.encode('utf-8'))
            file.close()
        except:
            printDBG('CSearchHistoryHelper.getHistoryList EXCEPTION')
            return []
        
        orgLen = len(historyList)
        # remove duplicates
        # last 50 searches patterns are stored
        historyList = historyList[:50]
        uniqHistoryList = []
        for i in historyList:
            if i not in uniqHistoryList:
                uniqHistoryList.append(i)
        historyList = uniqHistoryList

        # save file without duplicates
        if orgLen > len(historyList):
            self._saveHistoryList(historyList)
            
        return historyList
    
    def addHistoryItem(self, itemValue):
        printDBG('CSearchHistoryHelper.addHistoryItem to file = "%s"' % self.PATH_FILE)
        try:
            file = open( self.PATH_FILE, 'a' )
            file.write(itemValue + '\n')
            printDBG('Added pattern: "%s"' % itemValue) 
            file.close
        except:
            printDBG('CSearchHistoryHelper.addHistoryItem EXCEPTION')


    def _saveHistoryList(self, list):
        printDBG('CSearchHistoryHelper._saveHistoryList to file = "%s"' % self.PATH_FILE)
        try:
            file = open( self.PATH_FILE, 'w' )
            l = len(list)
            for i in range( l ):
                file.write( list[l - 1 -i] + '\n' )
            file.close
        except:
            printDBG('CSearchHistoryHelper._saveHistoryList EXCEPTION')

# end CSearchHistoryHelper

#localization part
from Components.Language import language
import gettext

PluginLanguageDomain = "TranslatedTexts"
PluginLanguagePath = "Extensions/BoardsClient/locale"

def localeInit():
	lang = language.getLanguage()[:2] # getLanguage returns e.g. "fi_FI" for "language_country"
	os.environ["LANGUAGE"] = lang # Enigma doesn't set this (or LC_ALL, LC_MESSAGES, LANG). gettext needs it!
	printDBG(PluginLanguageDomain + " set language to " + lang)
	gettext.bindtextdomain(PluginLanguageDomain, resolveFilename(SCOPE_PLUGINS, PluginLanguagePath))

def TranslateTXT(txt):
	t = gettext.dgettext(PluginLanguageDomain, txt)
	if t == txt:
		#print PluginLanguageDomain, "fallback to default translation for", txt
		t = gettext.gettext(txt)
	return t

localeInit()
language.addCallback(localeInit)