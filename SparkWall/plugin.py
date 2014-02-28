# -*- coding: utf-8 -*-
#
#  SparkWall by j00zek, based on IPTV
# 
from Plugins.Plugin import PluginDescriptor

from Screens.Screen import Screen

from Components.ActionMap import ActionMap, HelpableActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.config import config, ConfigSubsection, ConfigSelection, ConfigDirectory, ConfigYesNo, Config, ConfigInteger, ConfigSubList, ConfigText, getConfigListEntry, configfile
from Components.Sources.StaticText import StaticText

from enigma import ePicLoad, eServiceCenter, eServiceReference, iServiceInformation, getDesktop

from Screens.MessageBox import MessageBox

from Tools.Directories import resolveFilename, SCOPE_PLUGINS

from tools import  printDBG, TranslateTXT as _
from xml.etree.cElementTree import parse
import string

try:
    from _version import version as wersja
except:
    wersja="XX.YY.ZZ"
from time import sleep as time_sleep
from ConfigMenu import ConfigMenu

####################################################
# Wywołanie wtyczki w roznych miejscach
####################################################
def Plugins(**kwargs):
    list = [PluginDescriptor(name=_("SparkWall"), description=_("Emulates wall option introduced in Spark fw"), where = [PluginDescriptor.WHERE_PLUGINMENU], icon="icons/logo.png", fnc=main)] # always show in plugin menu
    list.append(PluginDescriptor(name=_("SparkWall"), description=_("Emulates wall option introduced in Spark fw"), where = PluginDescriptor.WHERE_MENU, fnc=startSparkWallfromMenu))
    if config.plugins.SparkWall.showinextensions.value:
        list.append (PluginDescriptor(name=_("SparkWall"), description=_("Emulates wall option introduced in Spark fw"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=main))
    return list

####################################################
# Konfiguracja wtyczki
####################################################
def startSparkWallfromMenu(menuid, **kwargs):
    if menuid == "mainmenu" and config.plugins.SparkWall.showinMainMenu.value == True:
        return [(_("SparkWall"), main, "SparkWall_main", None)]
    else:
        return []
    
def mainSetup(session,**kwargs):
    session.open(ConfigMenu) 

####################################################
#                   For IPTV components
####################################################
from asynccall import AsyncMethod


#####################################################
#                     For hosts
#####################################################
# interface for hosts
from ihost import RetHost
######################################################
#                   For mainThreadQueue
######################################################
from enigma import eTimer
from asynccall import CFunctionProxyQueue
######################################################
gMainFunctionsQueue = None

def main(session,**kwargs):
    session.open(SparkWallWidget)

class SparkWallWidget(Screen):
    Plugin_PATH = resolveFilename(SCOPE_PLUGINS, 'Extensions/SparkWall/')
    sz_w = getDesktop(0).size().width() - 190
    sz_h = getDesktop(0).size().height() - 195
    printDBG("[SparkWall] desktop size %dx%d wersja[%s]\n" % (sz_w+90, sz_h+100, wersja) )
    if sz_h < 500:
        sz_h += 4
    skin = """
        <screen name="SparkWallWidget" position="center,center" title="%s %s" size="%d,%d">
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
            <!--widget name="cover" zPosition="2" position="5,%d" size="122,140" alphatest="blend" /-->     
            <widget name="playerlogo" zPosition="4" position="%d,20" size="120,40" alphatest="blend" />
            <ePixmap zPosition="4" position="5,%d" size="%d,5" pixmap="%s" transparent="1" />
        </screen>""" %(
            _("SparkWall v."),
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
            resolveFilename(SCOPE_PLUGINS, 'Extensions/SparkWall/icons/line.png'),
            )
   
    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)

        self.CurrentService = self.session.nav.getCurrentlyPlayingServiceReference()

        #self.session.nav.stopService()
        self.session.nav.event.append(self.__event)

        #self["key_red"] = StaticText("Exit")
        #self["key_green"] = StaticText("Config")
        #self["key_yellow"] = StaticText("Show pictures")
        #self["key_blue"] = StaticText("Info")

        self["statustext"] = Label("Pobieranie listy...")
        self["actions"] = ActionMap(["WizardActions", "DirectionActions", "ColorActions"],
        {
            #"ok": self.ok_pressed,
            #"back": self.back_pressed,
            #"red": self.red_pressed,
            #"green": self.green_pressed,
            #"yellow": self.yellow_pressed,
            #"blue": self.blue_pressed,
           
        }, -1)     

        self["titel"] = Label()
        self["station"] = Label()
        self["headertext"] = Label()
        self["console"] = Label()
        
        #self["cover"] = Cover()
        #self["cover"].hide()
        
        #self["playerlogo"] = Cover()
        
        self.showMessageNoFreeSpaceForIcon = False
  
        self.onClose.append(self.__onClose)
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
                       
        self.selectSparkWallChannel()
        return
    
    def LeaveThreadView(self):
        pass
    
    def onStart(self):
        if self.started == 0:
            self.selectSparkWallChannel()
            self.started = 1
        return
        
    def getListFromRef(self, ref):
        list = []

        serviceHandler = eServiceCenter.getInstance()
        services = serviceHandler.list(ref)
        bouquets = services and services.getContent("SN", True)

        for bouquet in bouquets:
            services = serviceHandler.list(eServiceReference(bouquet[0]))
            channels = services and services.getContent("SN", True)
            for channel in channels:
                if not channel[0].startswith("1:64:"): # Ignore marker
                    list.append((channel[0] , channel[1].replace('\xc2\x86', '').replace('\xc2\x87', '')))
#options.extend((("aqq", "qqa"),))
            return list

    def selectSparkWallChannel(self):
    
        self.host = None
        self.hostName = ''
        self.nextSelIndex = 0
        self.prevSelList = []
        self.categoryList = []
        self.currList = []
        self.currSelectedItemName = ""

        self.tv_list = self.getListFromRef(eServiceReference('1:7:1:0:0:0:0:0:0:0:(type == 1) || (type == 17) || (type == 195) || (type == 25) FROM BOUQUET "bouquets.tv" ORDER BY bouquet'))
        self.radio_list = self.getListFromRef(eServiceReference('1:7:2:0:0:0:0:0:0:0:(type == 2) FROM BOUQUET "bouquets.radio" ORDER BY bouquet'))

        from selector import SelectorWidget

        self.session.openWithCallback(self.selectSparkWallChannelCallback, SelectorWidget, list = self.tv_list)
        return
    
    def selectSparkWallChannelCallback(self, ret): #tutaj update EPG i ewentualnie innych pierdol
        if ret:               
            printDBG("[SparkWall] Selected host" + ret[1])
        else:
            printDBG("[SparkWall] Nothing selected")
        self.close()
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
