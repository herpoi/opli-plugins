# -*- coding: utf-8 -*-
#
#  IplaPlayer based on SHOUTcast
#
#  $Id$
#
# 
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Components.ActionMap import ActionMap, HelpableActionMap
from Components.Label import Label
from Tools.Directories import resolveFilename, SCOPE_PLUGINS

#from enigma import iPlayableService, iServiceInformation

from Components.Pixmap import Pixmap
from enigma import ePicLoad
from Components.ScrollLabel import ScrollLabel
import string
from enigma import getDesktop
from Components.config import config, ConfigSubsection, ConfigSelection, ConfigDirectory, ConfigYesNo, Config, ConfigInteger, ConfigSubList, ConfigText, getConfigListEntry, configfile
from Screens.MessageBox import MessageBox
from Components.Sources.StaticText import StaticText
from Screens.ChoiceBox import ChoiceBox
from Screens.VirtualKeyBoard import VirtualKeyBoard

from Components.Input import Input
from Screens.InputBox import InputBox 
from libs.tools import GetGITversion as iptvtools_GetGITversion, \
                      UpdateIPTV_from_GIT as iptvtools_UpdateIPTV_from_GIT, \
                      FreeSpace as iptvtools_FreeSpace, \
                      mkdirs as iptvtools_mkdirs, \
                      printDBG, GetHostsList, TranslateTXT as _
try:
    from _version import version as wersja
except:
    wersja="XX.YY.ZZ"
from Components.Console import Console #do buforowania w tle
from time import sleep as time_sleep
from ConfigMenu import ConfigMenu
from os import remove as os_remove, path as os_path

####################################################
# Wywołanie wtyczki w roznych miejscach
####################################################
def Plugins(**kwargs):
    list = [PluginDescriptor(name=_("Boards Client"), description=_("Various forums client"), where = [PluginDescriptor.WHERE_PLUGINMENU], icon="logo.png", fnc=main)] # always show in plugin menu
    list.append(PluginDescriptor(name=_("Boards Client"), description=_("Various forums client"), where = PluginDescriptor.WHERE_MENU, fnc=startIPTVfromMenu))
    if config.plugins.BoardReader.showinextensions.value:
        list.append (PluginDescriptor(name=_("Boards Client"), description=_("Various forums client"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=main))
    return list

####################################################
# Konfiguracja wtyczki
####################################################
def startIPTVfromMenu(menuid, **kwargs):
    #if menuid == "system":
        #return [(_("Configure Boards Client"), mainSetup, "boardsclient_config", None)]
    #el
    if menuid == "mainmenu" and config.plugins.BoardReader.showinMainMenu.value == True:
        return [(_("Boards Client"), main, "boardsclient_main", None)]
    else:
        return []
    
def mainSetup(session,**kwargs):
    session.open(ConfigMenu) 

####################################################
#                   For IPTV components
####################################################
from asynccall import AsyncMethod
from MyList import MyListComponent


#####################################################
#                     For hosts
#####################################################
# interface for hosts
from ihost import IHost, CDisplayListItem, RetHost, CUrlItem
######################################################
from iconmanager import IconManager
from cover import Cover

######################################################
#                   For mainThreadQueue
######################################################
from enigma import eTimer
from asynccall import CFunctionProxyQueue
######################################################
gMainFunctionsQueue = None

def main(session,**kwargs):
    session.open(BoardReaderWidget)

class BoardReaderWidget(Screen):
    Plugin_PATH = resolveFilename(SCOPE_PLUGINS, 'Extensions/BoardsClient/')
    sz_w = getDesktop(0).size().width() - 190
    sz_h = getDesktop(0).size().height() - 195
    printDBG("[BoardReader] desktop size %dx%d wersja[%s]\n" % (sz_w+90, sz_h+100, wersja) )
    if sz_h < 500:
        sz_h += 4
    skin = """
        <screen name="BoardReaderWidget" position="center,center" title="%s %s" size="%d,%d">
         <ePixmap position="5,9" zPosition="4" size="30,30" pixmap="%s/icons/red.png" transparent="1" alphatest="on" />
         <!--ePixmap position="180,9" zPosition="4" size="30,30" pixmap="%s/icons/yellow.png" transparent="1" alphatest="on" /-->
         <!--ePixmap position="385,9" zPosition="4" size="30,30" pixmap="%s/icons/green.png" transparent="1" alphatest="on" /-->
         <!--ePixmap position="670,9" zPosition="4" size="30,30" pixmap="%s/icons/blue.png" transparent="1" alphatest="on" /-->
         <widget render="Label" source="key_red" position="45,9" size="140,27" zPosition="5" valign="center" halign="left" backgroundColor="black" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
         <!--widget render="Label" source="key_yellow" position="220,9" size="180,27" zPosition="5" valign="center" halign="left" backgroundColor="black" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" /-->
         <!--widget render="Label" source="key_green" position="425,9" size="300,27" zPosition="5" valign="center" halign="left" backgroundColor="black" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" /-->
         <!--widget render="Label" source="key_blue" position="710,9" size="140,27" zPosition="5" valign="center" halign="left" backgroundColor="black" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" /-->
         <widget name="headertext" position="5,47" zPosition="1" size="%d,23" font="Regular;20" transparent="1"  backgroundColor="#00000000"/>
            <widget name="statustext" position="5,240" zPosition="1" size="%d,90" font="Regular;20" halign="center" valign="center" transparent="0"  backgroundColor="#00000000"/>
            <widget name="list" position="5,100" zPosition="2" size="%d,%d" scrollbarMode="showOnDemand" transparent="0"  backgroundColor="#00000000" />
            <widget name="titel" position="115,%d" zPosition="1" size="%d,40" font="Regular;18" transparent="1"  backgroundColor="#00000000"/>
            <widget name="station" position="115,%d" zPosition="1" size="%d,40" font="Regular;18" transparent="1"  backgroundColor="#00000000"/>
            <widget name="console" position="165,%d" zPosition="1" size="%d,140" font="Regular;20" transparent="1"  backgroundColor="#00000000"/>
            <widget name="cover" zPosition="2" position="5,%d" size="122,140" alphatest="blend" />     
            <widget name="playerlogo" zPosition="4" position="%d,20" size="120,40" alphatest="blend" />
            <ePixmap zPosition="4" position="5,%d" size="%d,5" pixmap="%s" transparent="1" />
        </screen>""" %(
            _("BoardsClient v."),
            wersja, # wersja wtyczki
            sz_w, sz_h, # size
            Plugin_PATH,Plugin_PATH,Plugin_PATH,Plugin_PATH, # icons
            sz_w - 135, # size headertext
            sz_w - 100, # size statustext
            sz_w - 10, sz_h - 255, # size list
            sz_h - 105, # position titel
            sz_w - 125, # size titel
            sz_h - 70, # position station
            sz_w - 125, # size station
            sz_h - 95, # position console
            sz_w - 155, # size console
            sz_h - 125, # position cover
            sz_w - 125, # position logo
            sz_h - 130, # position line bottom
            sz_w / 2, # size line bottom
            resolveFilename(SCOPE_PLUGINS, 'Extensions/BoardsClient/icons/line.png'),
            )
   
    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)
        self.BRConsole = Console() #j00zek
        self.nagrywanie=False #j00zek

        self.CurrentService = self.session.nav.getCurrentlyPlayingServiceReference()
        #self.session.nav.stopService()
        self.session.nav.event.append(self.__event)

        self["key_red"] = StaticText("Exit")
        #self["key_green"] = StaticText("Config")
        #self["key_yellow"] = StaticText("Show pictures")
        #self["key_blue"] = StaticText("Info")

        self["list"] = MyListComponent()
        self["list"].connectSelChanged(self.onSelectionChanged)
        self["statustext"] = Label("Pobieranie listy...")
        self["actions"] = ActionMap(["WizardActions", "DirectionActions", "ColorActions"],
        {
            "ok": self.ok_pressed,
            "back": self.back_pressed,
            "red": self.red_pressed,
            #"green": self.green_pressed,
            #"yellow": self.yellow_pressed,
            #"blue": self.blue_pressed,
           
        }, -1)     

        self["titel"] = Label()
        self["station"] = Label()
        self["headertext"] = Label()
        self["console"] = Label()
        
        self["cover"] = Cover()
        self["cover"].hide()
        
        self["playerlogo"] = Cover()
        
        self.showMessageNoFreeSpaceForIcon = False
        self.iconManager = None
        if config.plugins.BoardReader.showcover.value:
            if not os_path.exists(config.plugins.BoardReader.SciezkaCache.value):
                iptvtools_mkdirs(config.plugins.BoardReader.SciezkaCache.value)
            if iptvtools_FreeSpace(config.plugins.BoardReader.SciezkaCache.value,10):
                self.iconManager = IconManager(self.checkIconCallBack, True)
            else:
                self.showMessageNoFreeSpaceForIcon = True
                self.iconManager = IconManager(self.checkIconCallBack, False)
  
        self.onClose.append(self.__onClose)
        #self.onLayoutFinish.append(self.selectHost)
        self.onShow.append(self.onStart)
        
        #Defs
        self.searchPattern = ''
        self.searchType = None
        
        self.changeIcon = True
        
        self.started = 0
        self.workThread = None
        
        self.host = None
        self.hostName = ''
        
        self.nextSelIndex = 0
        self.currSelIndex = 0
        
        self.prevSelList = []
        self.categoryList = []
      
        self.currList = []
        self.currSelectedItemName = ""

        self.visible = True
        
    
        #################################################################
        #                      Inits for Proxy Queue
        #################################################################
       
        # register function in main Queue
        global gMainFunctionsQueue
        gMainFunctionsQueue = CFunctionProxyQueue()
        gMainFunctionsQueue.unregisterAllFunctions()
        gMainFunctionsQueue.clearQueue()
            
        gMainFunctionsQueue.registerFunction(self.reloadList)
        gMainFunctionsQueue.registerFunction(self.checkIconCallBack)
        gMainFunctionsQueue.registerFunction(self.updateCover)
        gMainFunctionsQueue.registerFunction(self.displayIcon)
        
        #main Queue
        self.mainTimer = eTimer()
        self.mainTimer.timeout.get().append(self.processProxyQueue)
        # every 100ms Proxy Queue will be checked  
        self.mainTimer.start(100)
        #################################################################
        
    #end def __init__(self, session):
        
    def __del__(self):       
        return
        
    def __onClose(self):
        self.session.nav.playService(self.CurrentService)
        self.session.nav.event.remove(self.__event)
        
        try:
            if self.mainTimer.Enabled():
                self.mainTimer.stop()
            global gMainFunctionsQueue
            gMainFunctionsQueue.unregisterAllFunctions()
            gMainFunctionsQueue.clearQueue()
            gMainFunctionsQueue = None
            self.BRConsole.ePopen('echo 1 > /proc/sys/vm/drop_caches')
        except:
            pass
        return

        
    def processProxyQueue(self):
        global gMainFunctionsQueue
        gMainFunctionsQueue.processQueue()
        
        return
        
        
    def isNotInWorkThread(self):
        return self.workThread == None or not self.workThread.Thread.isAlive()
 
    def red_pressed(self):
        self.close()
        return

    def green_pressed(self):
        return

    def yellow_pressed(self):
        self.session.open(MessageBox, "Yellow button pressed, Action TBD", type = MessageBox.TYPE_INFO, timeout = 10 )
        return
 
    def blue_pressed(self):
        self.session.open(MessageBox, "Blue button pressed, action TBD", type = MessageBox.TYPE_INFO, timeout = 10 )
        return

        
    # method called from IconManager when a new icon has been dowlnoaded
    def checkIconCallBack(self, ret):
        printDBG("checkIconCallBack")
 
        # ret - url for icon wich has been dowlnoaded
        global gMainFunctionsQueue
        
        #the proxy Queue will be used to call function from mainThread
        gMainFunctionsQueue.addToQueue("displayIcon", ret)
        return
        
        
    def displayIcon(self, ret = None):
        # check if displays icon is enabled in options
        if not config.plugins.BoardReader.showcover.value or None == self.iconManager :
            return
            
        
        if False == self.changeIcon:
            return
        
        selItem = self.getSelItem()
        # when ret is != None the method is called from IconManager 
        # and in this variable the url for icon which was downloaded 
        # is returned 
        if ret != None and selItem != None:
            # if icon for other than selected item has been downloaded 
            # the displayed icon will not be changed
            if ret != selItem.iconimage:
                return
            
        # Display icon
        if selItem and selItem.iconimage != '' and self.iconManager:
            self["cover"].hide()
            # check if we have this icon and get the path to this icon on disk
            iconPath = self.iconManager.getIconPathFromAAueue(selItem.iconimage)
            printDBG( 'displayIcon -> getIconPathFromAAueue: ' + selItem.iconimage )
            if iconPath != '':
                printDBG( 'updateIcon: ' + iconPath )
                self["cover"].decodeCover(iconPath, self.decodeCoverCallBack, "cover")
                self.changeIcon = False
        else:
            self["cover"].hide()
        return

            
    def decodeCoverCallBack(self, ret):
        printDBG("decodeIconIfNeedeCallBack")
        
        global gMainFunctionsQueue
        #the proxy Queue will be used to call function from mainThread
        gMainFunctionsQueue.addToQueue("updateCover", ret)
        
        return
            
    def updateCover(self, retDict):
        # retDict - return dictionary  {Ident, Pixmap, FileName, Changed}
        printDBG('updateCover')
        if retDict:
            printDBG("updateCover retDict for Ident: %s " % retDict["Ident"])
            if retDict["Changed"]:
                self[retDict["Ident"]].updatePixmap(retDict["Pixmap"], retDict["FileName"])
            else:
                printDBG("updateCover pixel map not changed")
                
            if 'cover' == retDict["Ident"]:
                #check if we have icon for right item on list
                selItem = self.getSelItem()
                if selItem and selItem.iconimage != '':
                    # check if we have this icon and get the path to this icon on disk
                    iconPath = self.iconManager.getIconPathFromAAueue(selItem.iconimage)
                    if iconPath == retDict["FileName"]:
                        # now we are sure that we have right icon, so let show it
                        self[retDict["Ident"]].show()
            else:
                self[retDict["Ident"]].show()
        else:
            printDBG("updateCover retDict empty")
            
        return

                
    def changeBottomPanel(self):
        self.changeIcon = True
        self.displayIcon()
        
        selItem = self.getSelItem()
        if selItem and selItem.description != '':
            data = selItem.description
            sData = data.replace('\n','')
            self["console"].setText(sData)
        else:
            self["console"].setText('')
            
        return
                
    
    def onSelectionChanged(self):
        self.changeBottomPanel()
        
        return

 
    def back_pressed(self):
        try:
            if not self.isNotInWorkThread():
                self.workThread.Thread._Thread__stop()
                self["statustext"].setText(_("Action cancelled!"))
                return
        except:
            return
            
        if self.visible:
                       
            if len(self.prevSelList) > 0:
                self.nextSelIndex = self.prevSelList.pop()
                self.categoryList.pop()
                printDBG( "back_pressed prev sel index %s" % self.nextSelIndex )
                self.requestListFromHost('Previous')
            else:
                #There is no prev categories, so exit
                #self.close()
                self.selectHost()
        else:
            self.showWindow()
            
        return

    def ok_pressed(self):
        if self.visible:
            sel = None
            try:
                sel = self["list"].l.getCurrentSelection()[0]
            except:
                printDBG( "ok_pressed except" )
                self.getRefreshedCurrList()
                return
            if sel is None:
                printDBG( "ok_pressed sel is None" )
                self.getInitialList()
                return
            elif len(self.currList) <= 0:
                printDBG( "ok_pressed list is empty" )
                self.getRefreshedCurrList()
                return
            else:
                printDBG( "ok_pressed selected item: %s" % (sel.name) )
                
                self.currSelectedItemName = sel.name             
                item = self.getSelItem()
                
                #Get current selection
                currSelIndex = self["list"].getCurrentIndex()
                #remember only prev categories
                if item.type == CDisplayListItem.TYPE_CATEGORY:
                        printDBG( "ok_pressed selected TYPE_CATEGORY" )
                        self.currSelIndex = currSelIndex
                        self.requestListFromHost('ForItem', currSelIndex, '')
                elif item.type == CDisplayListItem.TYPE_NEWTHREAD or item.type == CDisplayListItem.TYPE_OLDTHREAD:
                        printDBG( "ok_pressed selected TYPE_[NEW|OLD]THREAD" )
                        self.currSelIndex = currSelIndex
                        ThreadContent, mainURL, ThreadURL = self.host.getFullThread(self.currSelIndex)
                        printDBG("ThreadContent:" + ThreadContent)
                        from libs.ThreadView import ThreadView
                        self.session.openWithCallback(self.LeaveThreadView, ThreadView, ThreadContent, mainURL, ThreadURL)
                else:
                    printDBG( "ok_pressed selected TYPE_SEARCH" )
                    self.currSelIndex = currSelIndex
                    self.startSearchProcedure(item.possibleTypesOfSearch)
        else:
            self.showWindow()
            
        return
    #end ok_pressed(self):
    
    def LeaveThreadView(self):
        pass
    
    def getSelIndex(self):
        currSelIndex = self["list"].getCurrentIndex()
        return currSelIndex

    def getSelItem(self):
        currSelIndex = self["list"].getCurrentIndex()
        if len(self.currList) <= currSelIndex:
            printDBG( "ERROR: getSelItem there is no item with index: %d, listOfItems.len: %d" % (currSelIndex, len(self.currList)) )
            return
        return self.currList[currSelIndex]
        
    def getSelectedItem(self):
        sel = None
        try:
            sel = self["list"].l.getCurrentSelection()[0]
        except:return None
        return sel
        
    def onStart(self):
        if self.started == 0:
            self.selectHost()
            self.started = 1
        return
        
    def selectHost(self):
    
        self.host = None
        self.hostName = ''
        self.nextSelIndex = 0
        self.prevSelList = []
        self.categoryList = []
        self.currList = []
        self.currSelectedItemName = ""
        self.json_installed = False
        try:
            import simplejson
            self.json_installed = True
        except:
            pass
        try:
            import json as simplejson
            self.json_installed = True
        except:
            pass

        options = [] 
        hostsList = GetHostsList()
        brokenHostList = []
        for hostName in hostsList:
            hostEnabled  = False
            try:
                exec('if config.plugins.BoardReader.host' + hostName + '.value: hostEnabled = True')
            except:
                hostEnabled = False
            if True == hostEnabled:
                if not config.plugins.BoardReader.devHelper.value:
                    try:
                        _temp = __import__('forums.forum' + hostName, globals(), locals(), ['gettytul'], -1)
                        title = _temp.gettytul()
                        printDBG('host name "%s"' % hostName)
                    except:
                        printDBG('get host name exception for host "%s"' % hostName)
                        brokenHostList.append('host'+hostName)
                        continue # do not use default name if import name will failed
                else:
                    _temp = __import__('forums.forum' + hostName, globals(), locals(), ['gettytul'], -1)
                    title = _temp.gettytul()
                    printDBG('host name "%s"' % hostName)
                options.extend(((title, hostName),))
        options.sort()
        
        #if len(brokenHostList) > 0:
        #    self.session.open(MessageBox, "Poniższe playery są niepoprawne lub brakuje im pewnych modułów.\n" + '\n'.join(brokenHostList), type = MessageBox.TYPE_INFO, timeout = 10 )
     
        options.extend(((_("Config"), "config"),))
        from playerselector import PlayerSelectorWidget

        self.session.openWithCallback(self.selectHostCallback, PlayerSelectorWidget, list = options)
        return
    
    def selectHostCallback(self, ret):
        hasIcon = False
        if ret:               
            printDBG("Selected host" + ret[1])
            if ret[1] == "config":
                self.session.openWithCallback(self.selectHost, ConfigMenu)
                return
            else:
                if not config.plugins.BoardReader.devHelper.value:
                    try:
                        self.hostName = ret[1]
                        _temp = __import__('forums.forum' + self.hostName, globals(), locals(), ['MyHost'], -1)
                        self.host = _temp.MyHost()
                    except:
                        printDBG( 'Cannot import class MyHost for host: "%s"' % ret[1] )
                        self.close()
                        return
                else:
                    self.hostName = ret[1]
                    _temp = __import__('forums.forum' + self.hostName, globals(), locals(), ['MyHost'], -1)
                    self.host = _temp.MyHost()
                
            if self.showMessageNoFreeSpaceForIcon and hasIcon:
                self.showMessageNoFreeSpaceForIcon = False
                self.session.open(MessageBox, "Brak wolnego miejsca w katalogu %s. \nNowe ikony nie beda ściągane. \nAby nowe ikony były dostępne wymagane jest 10MB wolnego miejsca." % (config.plugins.BoardReader.SciezkaCache.value), type = MessageBox.TYPE_INFO, timeout = 10 )
        else:
            self.close()
            return
        
        #############################################
        #            change logo for player
        #############################################
        self["playerlogo"].hide()
        
        hRet= self.host.getLogoPath()
        if hRet.status == RetHost.OK and  len(hRet.value):
            logoPath = hRet.value[0]
                
            if logoPath != '':
                printDBG( 'Logo Path: ' + logoPath )
                self["playerlogo"].decodeCover(logoPath, \
                                               self.decodeCoverCallBack, \
                                               "playerlogo")
        #############################################
        
        # request initial list from host        
        self.getInitialList()
        
        return
        
    #end selectHostCallback(self, ret):

    def is_stream(self, url):
        if url[:7] == 'rtmp://':
            return True
        if url[:7] == 'rtsp://':
            return True
        if url[:6] == 'mms://':
            return True
        elif url[-5:] == '.m3u8':
            return True
        elif url[-7:] == '.stream':
            return True
        else:
            return False

    def requestListFromHost(self, type, currSelIndex = -1, videoUrl = ''):
        
        if self.isNotInWorkThread():
            self["list"].hide()
            
            if type != 'ForVideoLinks' and type != 'ResolveURL':
                #hide bottom panel
                self["cover"].hide()
                self["console"].setText('')
                
            if type == 'ForItem' or type == 'ForSearch':
                self.prevSelList.append(self.currSelIndex)
                if type == 'ForSearch':
                    self.categoryList.append('Wyniki wyszukiwania')
                else:
                    self.categoryList.append(self.currSelectedItemName) 
                #new list, so select first index
                self.nextSelIndex = 0
            
            selItem = None
            if currSelIndex > -1 and len(self.currList) > currSelIndex:
                selItem = self.currList[currSelIndex]
            
            if type == 'Refresh':
                self["statustext"].setText("Odświeżam...............")
                self.workThread = AsyncMethod(self.host.getCurrentList, self.callbackGetList)(1)
            elif type == 'Initial':
                self["statustext"].setText("Pobieranie..............")
                self.workThread = AsyncMethod(self.host.getInitList, self.callbackGetList)()
            elif type == 'Previous':
                self["statustext"].setText("Pobieranie..............")
                self.workThread = AsyncMethod(self.host.getPrevList, self.callbackGetList)()
            elif type == 'ForItem':
                self["statustext"].setText("Pobieranie..............")
                self.workThread = AsyncMethod(self.host.getListForItem, self.callbackGetList)(currSelIndex, 0, selItem)
            elif type == 'ForSearch':
                self["statustext"].setText("Szukam..................")
                self.workThread = AsyncMethod(self.host.getSearchResults, self.callbackGetList)(self.searchPattern, self.searchType)
            else:
                printDBG( 'requestListFromHost unknown list type: ' + type )
                        
        return
    
    #end requestListFromHost(self, type, currSelIndex = -1, videoUrl = ''):
        
    def startSearchProcedure(self, searchTypes):
        if searchTypes:
            self.session.openWithCallback(self.selectSearchTypeCallback, ChoiceBox, title = "Wybierz typ wyszukiwania", list = searchTypes)
        else:
            self.searchType = None
            self.session.openWithCallback(self.enterPatternCallBack, VirtualKeyBoard, title = (_("Wprowadz wzorzec")), text = self.searchPattern)
    
    def selectSearchTypeCallback(self, ret = None):
        if ret:
            self.searchType = ret[1]
            self.session.openWithCallback(self.enterPatternCallBack, VirtualKeyBoard, title = (_("Wprowadz wzorzec")), text = self.searchPattern)
        else:
            pass
            # zrezygnowal z wyszukiwania
            
    def enterPatternCallBack(self, callback = None):
        if callback is not None and len(callback):  
            self.searchPattern = callback
            self.requestListFromHost('ForSearch')
        else:
            pass
            # zrezygnowal z wyszukiwania
    
    def requestSearchListFromHost(self, searchPattern, searchType):
        self.workThread = AsyncMethod(self.host.getSearchResults, self.callbackGetList)(searchPattern, searchType)
    
            
    def callbackGetList(self, ret):
        printDBG( "plugin:callbackGetList" )
        
        global gMainFunctionsQueue
        #the proxy Queue will be used to call function from mainThread
        gMainFunctionsQueue.addToQueue("reloadList", ret)
        
        return

    def reloadList(self, ret):
        printDBG( "plugin:reloadList" )
        
        # ToDo: check ret.status if not OK do something :P
        if ret.status != RetHost.OK:
            printDBG( "++++++++++++++++++++++ callbackRefreshXML ret.status = %s" % ret.status )

        self.currList = ret.value
        print self.currList
        self["list"].setList([ (x,) for x in self.currList])
        
        
        ####################################################
        #                   iconManager
        ####################################################
        iconList = []
        # fill icon List for icon manager 
        # if an user whant to see icons
        if config.plugins.BoardReader.showcover.value and self.iconManager:
            for it in self.currList:
                if it.iconimage != '':
                    iconList.append(it.iconimage)
        
        if len(iconList):
            # List has been changed so clear old Queue
            self.iconManager.clearDQueue()
            # a new list of icons should be downloaded
            self.iconManager.addToDQueue(iconList)
        #####################################################
        
        
        self["headertext"].setText(self.getCategoryPath())
            
        if len(self.currList) <= 0:
            if ret.message and ret.message != '':
                self["statustext"].setText("%s \n\nNaciśnij OK, aby odświeżyć" % ret.message)
            else:
                self["statustext"].setText("Brak elementów do wyświetlenia.\nNaciśnij OK, aby odświeżyć")
            self["list"].hide()
        else:
            #restor previus selection
            if len(self.currList) > self.nextSelIndex:
                self["list"].moveToIndex(self.nextSelIndex)
            else:
                #selection will not be change so manualy call
                self.changeBottomPanel()
            
            self["statustext"].setText("")            
            self["list"].show()
    #end reloadList(self, ret):
    
    def getCategoryPath(self):
        str = self.hostName
        
        for cat in self.categoryList:
            str += ' > ' + cat
        return str
    
    def getRefreshedCurrList(self):
        self.requestListFromHost('Refresh')
        return
    
    def getInitialList(self):
        self.nexSelIndex = 0
        self.prevSelList = []
        self.categoryList = []
        self.currList = []
        self.currSelectedItemName = ""
        self["headertext"].setText(self.getCategoryPath())
        
        self.requestListFromHost('Initial')
        return
        

    def hideWindow(self):
        self.visible = False
        self.hide()

    def showWindow(self):
        self.visible = True
        self.show()          

    def Error(self, error = None):
        if error is not None:
            try:
                self["list"].hide()
                self["statustext"].setText(str(error.getErrorMessage()))
            except: pass
        
    def __event(self, ev):
        pass

    def createSummary(self):
        return BoardReaderLCDScreen
#class BoardReaderWidget


class BoardReaderLCDScreen(Screen):
    skin = """
    <screen position="0,0" size="132,64" title="BoardReader">
        <widget name="text1" position="4,0" size="132,14" font="Regular;12" halign="center" valign="center"/>
         <widget name="text2" position="4,14" size="132,49" font="Regular;10" halign="center" valign="center"/>
    </screen>"""

    def __init__(self, session, parent):
        Screen.__init__(self, session)
        self["text1"] =  Label("Board Reader")
        self["text2"] = Label("")

    def setText(self, text):
        self["text2"].setText(text[0:39])
