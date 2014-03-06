# -*- coding: utf-8 -*-
#
#  SparkWall by j00zek, based on IPTV
# 
###################################################
# Import lokalnych skryptow
###################################################
try:
    from _version import version as wersja
except:
    wersja="XX.YY.ZZ"
from ConfigMenu import ConfigMenu
from tools import  printDBG, TranslateTXT as _
from selector import SelectorWidget #wybork kanalu po nazwie
####################################################
# Wywołanie wtyczki w roznych miejscach
####################################################
from Plugins.Plugin import PluginDescriptor

def Plugins(**kwargs):
    list = [PluginDescriptor(name="SparkWall", description=_("Emulates wall option introduced in Spark fw"), where = [PluginDescriptor.WHERE_PLUGINMENU], icon="icons/logo.png", fnc=main)] # always show in plugin menu
    list.append(PluginDescriptor(name="SparkWall", description=_("Emulates wall option introduced in Spark fw"), where = PluginDescriptor.WHERE_MENU, fnc=startSparkWallfromMenu))
    list.append(PluginDescriptor(name="SparkWall", description=_("Emulates wall option introduced in Spark fw"), where = PluginDescriptor.WHERE_MENU, fnc=startSparkWallfromMenu))
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
###################################################
# FOREIGN imports
###################################################
from Components.ActionMap import ActionMap, HelpableActionMap
from Components.config import config, Config

from Screens.Screen import Screen

from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.Sources.StaticText import StaticText

from enigma import ePicLoad, eServiceCenter, eServiceReference, iServiceInformation, getDesktop

from Tools.Directories import resolveFilename, SCOPE_PLUGINS

from xml.etree.cElementTree import parse
from ServiceReference import ServiceReference
######################################################
def main(session,**kwargs):
    session.open(SparkWallWidget, kwargs["servicelist"])

class SparkWallWidget(Screen):
    printDBG("[SparkWall] start\n")
   
    def __init__(self, session, servicelist = None):
        self.session = session
        Screen.__init__(self, session)
        self.started = 0
        # Ustawienia listy
        self.servicelist = servicelist
        self.curRef = ServiceReference(self.servicelist.getCurrentSelection())
        self.curChannel = self.servicelist.getCurrentSelection().toString()
        print "AQQ" + self.curChannel
        self.curBouquet = self.servicelist.getRoot()
        self.onShow.append(self.onStart)
        
    def onStart(self):
        if self.started == 0:
            self.selectSparkWallChannel()
            self.started = 1
        return

    def getListFromRef(self, ref): # pobieramy liste kanalow
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
            return list

    def selectSparkWallChannel(self):
        self.tv_list = self.getListFromRef(eServiceReference('1:7:1:0:0:0:0:0:0:0:(type == 1) || (type == 17) || (type == 195) || (type == 25) FROM BOUQUET "bouquets.tv" ORDER BY bouquet'))
        #self.radio_list = self.getListFromRef(eServiceReference('1:7:2:0:0:0:0:0:0:0:(type == 2) FROM BOUQUET "bouquets.radio" ORDER BY bouquet'))
        self.session.openWithCallback(self.selectSparkWallChannelCallback, SelectorWidget, list = self.tv_list)
        return
    
    def selectSparkWallChannelCallback(self, ret): # jako ret dostajemy dane wybranego kanalu i nazwe
        if ret:               
            printDBG("[SparkWall] Selected host" + ret[1] + " " + ret[0])
            service = eServiceReference(ret[0])
            self.servicelist.setCurrentSelection(service) #wybieramy serwis na liscie
            self.servicelist.zap(enable_pipzap = True) # i przelaczamy
        else:
            printDBG("[SparkWall] Nothing selected")
        self.close()
        return
