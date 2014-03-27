# -*- coding: utf-8 -*-
#
#  PiconSelector by j00zek
# 
###################################################
# local imports
###################################################
from tools import  printDBG, TranslateTXT as _
from selector import SelectorWidget #wybork kanalu po nazwie
###################################################
# Import foreign scrits
###################################################
from Components.Console import Console
from Screens.Console import Console as Screens_Console
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.Directories import resolveFilename, pathExists, SCOPE_PLUGINS, SCOPE_SKIN_IMAGE
from os import walk as os_walk, path as os_path, remove as os_remove, listdir as os_listdir
from urllib2 import Request, urlopen, URLError, HTTPError
import tarfile

####################################################
# Wywołanie wtyczki w roznych miejscach
####################################################
from Plugins.Plugin import PluginDescriptor

def Plugins(**kwargs):
    list = [PluginDescriptor(name="PiconSelector", description=_("Graphical picons downloader"), where = [PluginDescriptor.WHERE_PLUGINMENU], icon="icons/logo.png", fnc=main)] # always show in plugin menu
    return list
######################################################
# main code
####################################################
def main(session,**kwargs):
    session.open(PiconsSelectorWidget)

class PiconsSelectorWidget(Screen):
    print("[PiconsSelector] starts\n")
   
    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)
        self.started = 0
        # Ustawienia listy
        self.myList = []
        self.onShow.append(self.onStart)
        self.curIndex = 0
        self.myURL='http://hybrid.xunil.pl/picons/'
        self.myPath=resolveFilename(SCOPE_PLUGINS, 'Extensions/PiconSelector')
        self.myPiconsPath=resolveFilename(SCOPE_PLUGINS, 'Extensions/PiconSelector/picons/')
        self.myItemsPath=resolveFilename(SCOPE_PLUGINS, 'Extensions/PiconSelector/picons/')
        self.SubTreesPath=resolveFilename(SCOPE_PLUGINS, 'Extensions/PiconSelector/MainSelection/')
        self.SubTreeSelected=False
        self.myConsole = Console()

    def onStart(self):
        if self.started == 0:
            self.started = 1
            self.myConsole.ePopen('%s/Downloader.sh "SYNC" "%s" "%s"' % (self.myPath,self.myItemsPath, self.myURL) , self.onStartcont() )
            
        return

    def onStartcont(self):
        self.prepareListForSelector(self.SubTreesPath, "" , "Select picons size")
        return
        
    def deletePicons(self):
        myPath = resolveFilename(SCOPE_SKIN_IMAGE, 'picon/')
        for root, dirs, files in os_walk(myPath):
            for name in files:
                #print name
                os_remove(os_path.join(root, name))
        
    
    def prepareListForSelector(self, myPath, myFilter = "" , SelectorTitle = "Select item" ):
        self.myList = []
        for root, dirs, files in os_walk(myPath):
            files.sort()
            for file in files:
                if file.endswith(".png"):
                    #print os_path.join(root, file)
                    if myFilter == "":
                        self.myList.append( ( file[:-4] , os_path.join(root, file) ) )
                    elif not file.find(myFilter):
                        self.myList.append( ( file[:-4] , os_path.join(root, file) ) )
                      
        #print self.myList
        if len(self.myList) >= 1:
            self.session.openWithCallback(self.SelectorCallback, SelectorWidget, list = self.myList, CurIdx = self.curIndex, Mytitle = SelectorTitle )
        else:
            self.close()
        return
    
    def SelectorCallback(self, ret): # jako ret dostajemy nazwe wybranego itemu w 0
        if self.SubTreeSelected == False:
            if ret:
                if ret[0] == "Clear picons folder":
                    self.deletePicons()
                    self.prepareListForSelector(self.SubTreesPath, "" , "Select picons size")
                    return
                else:
                    self.SubTreeSelected = True
                    self.prepareListForSelector(self.myItemsPath, ret[0], "Select Picons shape")
                    return
            else:
                self.close()
                return
        else: # we have picons selected, time to download them
            ArchiveURL = "http://hybrid.xunil.pl/picons/%s.tar.gz" % ret[0]
            ArchiveFile=resolveFilename(SCOPE_SKIN_IMAGE, 'picon/%s.tar.gz' % ret[0])

            self.session.openWithCallback(self.ArchiveDownloaded ,Screens_Console, title = _("Installing %s") % ret[0], 
                                          cmdlist = [ '%s/Downloader.sh "PICONS" "%s" "%s"' % (self.myPath, resolveFilename(SCOPE_SKIN_IMAGE, 'picon'), ArchiveURL) ])
            #self.myConsole.ePopen('wget http://hybrid.xunil.pl/picons/%s.picons -O %spicons.tgz; mv %spicons.tgz %spicons.tar.gz' % (ret[0] , resolveFilename(SCOPE_SKIN_IMAGE, 'picon/') ), self.ArchiveDownloaded )
        self.close()
        return

    def ArchiveDownloaded(self):
        if pathExists(resolveFilename(SCOPE_SKIN_IMAGE, 'picon/picons.tar.gz' )):
            self.session.openWithCallback( self.InstallArchive , MessageBox,"Picons archive downloaded, press OK to install it." , MessageBox.TYPE_YESNO, timeout=10 )
        return

    def InstallArchive(self):
        return

    def get_process(self, NazwaProcesu ):
        pids = []
        process = None
        for i in os_listdir('/proc'):
            if i.isdigit():
                pids.append(i)

        for pid in pids:
            proc = open(os_path.join('/proc', pid, 'status'), 'r').readline()
            print proc
            if proc.find(NazwaProcesu):
                process = pid

        return process          

    def is_running(self, pid):
        return os_path.exists("/proc/%s" % str(pid))