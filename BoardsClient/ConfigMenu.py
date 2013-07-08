# -*- coding: utf-8 -*-
#
#  Konfigurator dla iptv 2013
#  autorzy: j00zek, samsamsam
#
#aktualizacja
try:
    import tarfile 
    UpdateAvailable = True
except:
    UpdateAvailable = False

if UpdateAvailable == True:
    try:
        from _version import version as wersja
        from libs.tools import GetGITversion as iptvtools_GetGITversion
        if iptvtools_GetGITversion() == wersja:
            UpdateAvailable = False
    except:
        pass
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Components.ActionMap import ActionMap, HelpableActionMap
from Components.Label import Label
from Components.config import config, ConfigSubsection, ConfigSelection, ConfigDirectory, ConfigYesNo, Config, ConfigInteger, ConfigSubList, ConfigText, getConfigListEntry, configfile
from Components.ConfigList import ConfigListScreen
from libs.tools import removeAllIconsFromPath, printDBG, GetHostsList, IsHostEnabled
from confighost import ConfigHostMenu

config.plugins.BoardReader = ConfigSubsection()
config.plugins.BoardReader.showcover = ConfigYesNo(default = True)
config.plugins.BoardReader.deleteIcons = ConfigSelection(default = "-1", choices = [("0", "zawsze"),("1", "po dniu"),("3", "po trzech dniach"),("7", "po tygodniu"),("30", "po miesiącu"),("-1", "nigdy")]) 
config.plugins.BoardReader.showinextensions = ConfigYesNo(default = True)
config.plugins.BoardReader.showinMainMenu = ConfigYesNo(default = False)
config.plugins.BoardReader.ListaGraficzna = ConfigYesNo(default = True) #do wywalenia uzywamy tylko graficznej
config.plugins.BoardReader.NaszaSciezka = ConfigText(default = "/hdd/movie/", fixed_size = False)
config.plugins.BoardReader.AktualizacjaWmenu = ConfigYesNo(default = False)
config.plugins.BoardReader.devHelper = ConfigYesNo(default = False)

config.plugins.BoardReader.SciezkaCache = ConfigText(default = "/hdd/IPTVCache/", fixed_size = False)
config.plugins.BoardReader.NaszaTMP = ConfigText(default = "/tmp/", fixed_size = False)

config.plugins.BoardReader.debugprint = ConfigSelection(default = "", choices = [("", "nie"),("console", "tak, na konsolę"),("debugfile", "tak, do pliku /hdd/iptv.dbg")]) 

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
        self.setup_title = "Konfiguracja ustawień"

        self["key_green"] = Label(_("Save"))
        self["key_red"] = Label(_("Cancel"))
        self["key_blue"] = Label('VK')
        if UpdateAvailable == True:
            self["key_yellow"] = Label('Aktualizacja')
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
            self["key_yellow"] = Label('Wersja aktualna')
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
            exec( 'self.listConfigHostsEntries.append(getConfigListEntry("Player ' + hostName + ' więcej->[OK]", config.plugins.BoardReader.host' + hostName + '))' )
        
        self.firstHostIdx = -1
        self.runSetup()
        self.onLayoutFinish.append(self.layoutFinished)
        
    def layoutFinished(self):
        self.setTitle("Boards Client config")

    def runSetup(self):

        # WYGLAD
        self.list = [ getConfigListEntry("Ikony na liście:", config.plugins.BoardReader.showcover) ]
        if config.plugins.BoardReader.showcover.value:
            self.list.append(getConfigListEntry("    Usuwaj ikony:", config.plugins.BoardReader.deleteIcons))
        self.list.append(getConfigListEntry("Katalog na dane cache:", config.plugins.BoardReader.SciezkaCache))
        self.list.append(getConfigListEntry("Katalog na chwilowe dane (temp):", config.plugins.BoardReader.NaszaTMP))
        
        self.list.append(getConfigListEntry("Wyświetlać wtyczkę na liście rozszerzeń?", config.plugins.BoardReader.showinextensions))
        self.list.append(getConfigListEntry("Wyświetlać wtyczkę w głównym menu?", config.plugins.BoardReader.showinMainMenu))
        self.list.append(getConfigListEntry("Wyświetlać aktualizację w głównym menu?", config.plugins.BoardReader.AktualizacjaWmenu))
        self.list.append(getConfigListEntry("Włączyć DEBUG?", config.plugins.BoardReader.debugprint))
        self.list.append(getConfigListEntry("Wyłączyć ochronę hostów? (Błąd wywołuje GS)", config.plugins.BoardReader.devHelper))
        self.list.append(getConfigListEntry("Czyszczenie przy aktualizacji?", config.plugins.BoardReader.cleanup))
        
        self.firstHostIdx = len(self.list)
        
        for hostConfItem in  self.listConfigHostsEntries:
            self.list.append( hostConfItem )
        
        self["config"].list = self.list
        self["config"].setList(self.list)

    def keyUpdate(self):
        self.save()

        #aktualizacja
        from libs.tools import UpdateIPTV_from_GIT as iptvtools_UpdateIPTV_from_GIT, FreeSpace as iptvtools_FreeSpace
        WersjaGIT=iptvtools_GetGITversion()
        msgtxt = 'Autorzy NIE ponoszą, żadnej odpowiedzialności za uszkodzenia tunera spowodowane działaniem tej wtyczki oraz wykorzystywaniem jej w celu nielegalnego pobierania materiałów video!!!'
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
                            self.host = __import__('hosts.host' + hostName, globals(), locals(), ['GetConfigList'], -1)
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
        if self["config"].getCurrent()[1] in [config.plugins.BoardReader.showcover,
                                              config.plugins.BoardReader.ListaGraficzna,
                                              ]:
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
                self.session.openWithCallback(self.keyVirtualKeyBoardCallBack, VirtualKeyBoard, title = (_("Wprowadź wartość")), text = text)
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
            