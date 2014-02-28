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
from libs.tools import removeAllIconsFromPath, printDBG, GetHostsList, IsHostEnabled, TranslateTXT as _
from confighost import ConfigHostMenu

config.plugins.BoardReader = ConfigSubsection()
config.plugins.BoardReader.showcover = ConfigYesNo(default = True)
config.plugins.BoardReader.deleteIcons = ConfigSelection(default = "0", choices = [("0", _("always")),("1", _("after day")),("3", _("after 3 days")),("7", _("after week")),("30", _("after month")),("-1", _("never"))]) 
config.plugins.BoardReader.showinextensions = ConfigYesNo(default = True)
config.plugins.BoardReader.showinMainMenu = ConfigYesNo(default = False)
config.plugins.BoardReader.NaszaSciezka = ConfigText(default = "/hdd/movie/", fixed_size = False)
config.plugins.BoardReader.AktualizacjaWmenu = ConfigYesNo(default = False)
config.plugins.BoardReader.devHelper = ConfigYesNo(default = False)

config.plugins.BoardReader.SciezkaCache = ConfigText(default = "/tmp/IPTVCache/", fixed_size = False)
config.plugins.BoardReader.NaszaTMP = ConfigText(default = "/tmp/", fixed_size = False)

config.plugins.BoardReader.debugprint = ConfigSelection(default = "", choices = [("", "no"),("console", "yes, on console"),("debugfile", "yes, in /tmp/iptv.dbg file")]) 

#icons
config.plugins.BoardReader.IconsSize = ConfigSelection(default = "100", choices = [("135", "135x135"),("120", "120x120"),("100", "100x100")]) 
config.plugins.BoardReader.numOfRow = ConfigSelection(default = "0", choices = [("1", "1"),("2", "2"),("3", "3"),("4", "4"),("0", "auto")])
config.plugins.BoardReader.numOfCol = ConfigSelection(default = "0", choices = [("1", "1"),("2", "2"),("3", "3"),("4", "4"),("5", "5"),("6", "6"),("7", "7"),("8", "8"),("0", "auto")])

config.plugins.BoardReader.cleanup = ConfigYesNo(default = True)

########################################################
# Generate list of hosts options for Enabling/Disabling
########################################################
gListOfHostsNames = [] 
gListOfHostsNames = GetHostsList()
for hostName in gListOfHostsNames:
    try:
        printDBG("Set default options for host '%s'" % hostName)
        # as default all hosts are enabled
        exec('config.plugins.BoardReader.host' + hostName + ' = ConfigYesNo(default = True)')
    except:
        printDBG("Options import for host '%s' EXEPTION" % hostName)

class ConfigMenu(Screen, ConfigListScreen):

    skin = """
    <screen name="Boards Client config" position="center,center" size="540,440" title="" backgroundColor="#31000000" >

            <widget name="config" position="10,10" size="520,395" zPosition="1" transparent="0" backgroundColor="#31000000" scrollbarMode="showOnDemand" />
            <widget name="key_green" position="0,405" zPosition="2" size="100,35" valign="center" halign="right" font="Regular;22" transparent="1" foregroundColor="green" />
            <widget name="key_blue" position="100,405" zPosition="2" size="50,35" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="blue" />
            <widget name="key_red" position="150,405" zPosition="2" size="100,35" valign="center" halign="right" font="Regular;22" transparent="1" foregroundColor="red" />
            <widget name="key_yellow" position="250,405" zPosition="2" size="200,35" valign="center" halign="right" font="Regular;22" transparent="1" foregroundColor="yellow" />

    </screen>"""
    
    def __init__(self, session):
        Screen.__init__(self, session)
        
        # remember old
        self.showcoverOld = config.plugins.BoardReader.showcover.value
        self.SciezkaCacheOld = config.plugins.BoardReader.SciezkaCache.value

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
                from libs.tools import GetGITversion as iptvtools_GetGITversion
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

        global gListOfHostsNames
        # prepar config entries for hosts Enabling/Disabling
        self.listConfigHostsEntries = []
        for hostName in gListOfHostsNames:
            exec( 'self.listConfigHostsEntries.append(getConfigListEntry( "%s" , config.plugins.BoardReader.host' % _("Press OK to set %s options") % hostName + hostName + '))' )
        
        self.firstHostIdx = -1
        self.runSetup()
        self.onLayoutFinish.append(self.layoutFinished)
        
    def layoutFinished(self):
        self.setTitle(_("Boards Client config"))

    def runSetup(self):

        # WYGLAD
        self.list = [ getConfigListEntry(_("Show icons:"), config.plugins.BoardReader.showcover) ]
        if config.plugins.BoardReader.showcover.value:
            self.list.append(getConfigListEntry(_("    Delete icons:"), config.plugins.BoardReader.deleteIcons))
        self.list.append(getConfigListEntry(_("Cache folder:"), config.plugins.BoardReader.SciezkaCache))
        self.list.append(getConfigListEntry(_("Temp folder:"), config.plugins.BoardReader.NaszaTMP))
        
        self.list.append(getConfigListEntry(_("Show plugin on the Extensions menu?"), config.plugins.BoardReader.showinextensions))
        self.list.append(getConfigListEntry(_("Show plugin in main menu?"), config.plugins.BoardReader.showinMainMenu))
        #self.list.append(getConfigListEntry("Wyświetlać aktualizację w głównym menu?", config.plugins.BoardReader.AktualizacjaWmenu))
        self.list.append(getConfigListEntry(_("Enable DEBUG?"), config.plugins.BoardReader.debugprint))
        self.list.append(getConfigListEntry(_("Disable secured mode? (error ends with GS)"), config.plugins.BoardReader.devHelper))
        self.list.append(getConfigListEntry(_("Clean folder during update?"), config.plugins.BoardReader.cleanup))
        
        self.firstHostIdx = len(self.list)
        
        for hostConfItem in  self.listConfigHostsEntries:
            self.list.append( hostConfItem )
        
        self["config"].list = self.list
        self["config"].setList(self.list)

    def keyUpdate(self):
        self.save()

        #aktualizacja
        from libs.tools import UpdateIPTV_from_GIT as iptvtools_UpdateIPTV_from_GIT, FreeSpace as iptvtools_FreeSpace
        WersjaGIT=self.iptvtools_GetGITversion
        msgtxt = "Autors don't take any responsibility for issues with tunners when using this plugin and using it to illegal download of the files"
        if iptvtools_FreeSpace(config.plugins.BoardReader.NaszaTMP.value,2):
            StatusUpdate = iptvtools_UpdateIPTV_from_GIT(config.plugins.BoardReader.NaszaTMP.value)
            if StatusUpdate == "OK":
                self.session.open(MessageBox, "Restart oPLI po aktualizacji wtyczki do wersji %s...\n Czytałeś już licencję?\nJeśli tak, to wiesz, że\n\n" % WersjaGIT + msgtxt, type = MessageBox.TYPE_INFO, timeout = 5 )
                from enigma import quitMainloop
                quitMainloop(3) 
            else:
                self.session.open(MessageBox, "Błąd aktualizacji wtyczki, spróbuj ponownie za jakiś czas.\n Status: %s \n\n Dla przypomnienia -\n\n" % StatusUpdate + msgtxt, type = MessageBox.TYPE_INFO, timeout = 10 )
                return
        else:
            self.session.open(MessageBox, "Brak wolnego miejsca w katalogu %s" % (config.plugins.BoardReader.NaszaTMP.value), type = MessageBox.TYPE_INFO, timeout = 10 )
            return

    def keySave(self):
        self.save()
        self.close()
    
    def save(self):
        for x in self["config"].list:
            x[1].save()
        configfile.save()
        
        if self.showcoverOld != config.plugins.BoardReader.showcover.value or \
           self.SciezkaCacheOld != config.plugins.BoardReader.SciezkaCache.value:
           # remove files from old path
           removeAllIconsFromPath(self.SciezkaCacheOld)
      
    def keyOK(self):
        self.save()
        
        if self.firstHostIdx > -1:
            curIndex = self["config"].getCurrentIndex()
            if curIndex >= self.firstHostIdx:
                # calculate index in hosts list
                idx = curIndex - self.firstHostIdx
                global gListOfHostsNames
                if idx < len(gListOfHostsNames):
                    hostName = gListOfHostsNames[idx]
                    if IsHostEnabled(hostName):
                        try:
                            self.host = __import__('forums.forum' + hostName, globals(), locals(), ['GetConfigList'], -1)
                            if( len(self.host.GetConfigList()) < 1 ):
                                printDBG('ConfigMenu host "%s" does not have additiona configs' % hostName)
                            self.session.open(ConfigHostMenu, hostName = hostName)
                        except:
                            printDBG('ConfigMenu host "%s" does not have method GetConfigList' % hostName)
        return

    def keyCancel(self):
        for x in self["config"].list:
            x[1].cancel()
        self.close()
        
    def changeSubOptions(self):
        if self["config"].getCurrent()[1] in [config.plugins.BoardReader.showcover]:
            self.runSetup()
        
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
            