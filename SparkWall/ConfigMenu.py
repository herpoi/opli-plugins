# -*- coding: utf-8 -*-
#
#  Konfigurator dla iptv 2013
#  autorzy: j00zek, samsamsam
#
#aktualizacja
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Components.ActionMap import ActionMap, HelpableActionMap
from Components.Label import Label
from Components.config import config, ConfigSubsection, ConfigSelection, ConfigDirectory, ConfigYesNo, Config, ConfigInteger, ConfigSubList, ConfigText, getConfigListEntry, configfile
from Components.ConfigList import ConfigListScreen
from tools import printDBG, TranslateTXT as _
from confighost import ConfigHostMenu

config.plugins.SparkWall = ConfigSubsection()
config.plugins.SparkWall.showinextensions = ConfigYesNo(default = True)
config.plugins.SparkWall.showinMainMenu = ConfigYesNo(default = False)
config.plugins.SparkWall.AktualizacjaWmenu = ConfigYesNo(default = False)
config.plugins.SparkWall.debugprint = ConfigSelection(default = "", choices = [("", "no"),("console", "yes, on console"),("debugfile", "yes, in /tmp/debug.log file")]) 
#icons
config.plugins.SparkWall.IconsSize = ConfigSelection(default = "100", choices = [("100", "Picon 100x60")("220", "XPicon 220x132")]) 
config.plugins.SparkWall.numOfRow = ConfigSelection(default = "0", choices = [("1", "1"),("2", "2"),("3", "3"),("4", "4"),("0", "auto")])
config.plugins.SparkWall.numOfCol = ConfigSelection(default = "0", choices = [("1", "1"),("2", "2"),("3", "3"),("4", "4"),("5", "5"),("6", "6"),("7", "7"),("8", "8"),("0", "auto")])

class ConfigMenu(Screen, ConfigListScreen):

    skin = """
    <screen name="SparkWall config" position="center,center" size="540,440" title="" backgroundColor="#31000000" >

            <widget name="config" position="10,10" size="520,395" zPosition="1" transparent="0" backgroundColor="#31000000" scrollbarMode="showOnDemand" />
            <widget name="key_green" position="0,405" zPosition="2" size="100,35" valign="center" halign="right" font="Regular;22" transparent="1" foregroundColor="green" />
            <widget name="key_blue" position="100,405" zPosition="2" size="50,35" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="blue" />
            <widget name="key_red" position="150,405" zPosition="2" size="100,35" valign="center" halign="right" font="Regular;22" transparent="1" foregroundColor="red" />
            <widget name="key_yellow" position="250,405" zPosition="2" size="200,35" valign="center" halign="right" font="Regular;22" transparent="1" foregroundColor="yellow" />

    </screen>"""
    
    def __init__(self, session):
        Screen.__init__(self, session)
        
        self.onChangedEntry = [ ]
        self.list = [ ]
        ConfigListScreen.__init__(self, self.list, session = session, on_change = self.changedEntry)
        self.setup_title = "Settings config"

        self["key_green"] = Label(_("Save"))
        self["key_red"] = Label(_("Cancel"))
        self["key_blue"] = Label('VK')
        self.iptvtools_GetGITversion = ''
        try:
            import tarfile 
            UpdateAvailable = True
        except:
            UpdateAvailable = False

        if UpdateAvailable == True:
            try:
                from _version import version as wersja
                from tools import GetGITversion as iptvtools_GetGITversion
                self.iptvtools_GetGITversion = iptvtools_GetGITversion()
                if iptvtools_GetGITversion() == wersja:
                    UpdateAvailable = False
            except:
                pass
        if UpdateAvailable == True:
            self["key_yellow"] = Label(_('Update'))
            self["actions"] = ActionMap(["SetupActions", "ColorActions"],
                {
                    "cancel": self.keyCancel,
                    "green": self.keySave,
                    "ok": self.keyOK,
                    "red": self.keyCancel,
                    "blue": self.keyVirtualKeyBoard,
                    "yellow": self.keyUpdate,
                }, -2)
        else:
            self["key_yellow"] = Label(_('v. up-2-date'))
            self["actions"] = ActionMap(["SetupActions", "ColorActions"],
                {
                    "cancel": self.keyCancel,
                    "green": self.keySave,
                    "ok": self.keyOK,
                    "red": self.keyCancel,
                    "blue": self.keyVirtualKeyBoard,
                }, -2)

        self.firstHostIdx = -1
        self.runSetup()
        self.onLayoutFinish.append(self.layoutFinished)
        
    def layoutFinished(self):
        self.setTitle(_("Boards Client config"))

    def runSetup(self):

        # WYGLAD
        self.list.append(getConfigListEntry(_("Show plugin on the Extensions menu?"), config.plugins.SparkWall.showinextensions))
        self.list.append(getConfigListEntry(_("Show plugin in main menu?"), config.plugins.SparkWall.showinMainMenu))
        #self.list.append(getConfigListEntry("Wyświetlać aktualizację w głównym menu?", config.plugins.SparkWall.AktualizacjaWmenu))
        self.list.append(getConfigListEntry(_("Enable DEBUG?"), config.plugins.SparkWall.debugprint))
        
        self.firstHostIdx = len(self.list)
        
        for hostConfItem in  self.listConfigHostsEntries:
            self.list.append( hostConfItem )
        
        self["config"].list = self.list
        self["config"].setList(self.list)

    def keyUpdate(self):
        self.save()

        #aktualizacja
        from tools import UpdateIPTV_from_GIT as iptvtools_UpdateIPTV_from_GIT, FreeSpace as iptvtools_FreeSpace
        WersjaGIT=self.iptvtools_GetGITversion
        msgtxt = "Autors don't take any responsibility for issues with tunners when using this plugin and using it to illegal download of the files"

        StatusUpdate = iptvtools_UpdateIPTV_from_GIT('/tmp')
        if StatusUpdate == "OK":
            self.session.open(MessageBox, "Restart oPLI po aktualizacji wtyczki do wersji %s...\n Czytałeś już licencję?\nJeśli tak, to wiesz, że\n\n" % WersjaGIT + msgtxt, type = MessageBox.TYPE_INFO, timeout = 5 )
            from enigma import quitMainloop
            quitMainloop(3) 
        else:
            self.session.open(MessageBox, "Błąd aktualizacji wtyczki, spróbuj ponownie za jakiś czas.\n Status: %s \n\n Dla przypomnienia -\n\n" % StatusUpdate + msgtxt, type = MessageBox.TYPE_INFO, timeout = 10 )
            return

    def keySave(self):
        self.save()
        self.close()
    
    def save(self):
        for x in self["config"].list:
            x[1].save()
        configfile.save()
        
    def keyOK(self):
        self.save()
        return

    def keyCancel(self):
        for x in self["config"].list:
            x[1].cancel()
        self.close()
        
    def changeSubOptions(self):
        return
        
    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.changeSubOptions()

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.changeSubOptions()

    def changedEntry(self):
        for x in self.onChangedEntry:
            x() 
            
    def keyVirtualKeyBoard(self):
        try:
            if isinstance( self["config"].getCurrent()[1], ConfigText ):
                from Screens.VirtualKeyBoard import VirtualKeyBoard
                text = self["config"].getCurrent()[1].value
                self.session.openWithCallback(self.keyVirtualKeyBoardCallBack, VirtualKeyBoard, title = (_("Enter value")), text = text)
        except:
            pass
            
    def keyVirtualKeyBoardCallBack(self, callback):
        try:
            if callback:  
                self["config"].getCurrent()[1].value = callback
            else:
                pass
        except:
            pass
            