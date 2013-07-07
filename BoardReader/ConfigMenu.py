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
        from iptvtools import GetGITversion as iptvtools_GetGITversion
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
from iptvtools import removeAllIconsFromPath, printDBG, GetHostsList, IsHostEnabled
from confighost import ConfigHostMenu

config.plugins.iptvplayer = ConfigSubsection()
config.plugins.iptvplayer.showcover = ConfigYesNo(default = True)
config.plugins.iptvplayer.deleteIcons = ConfigSelection(default = "-1", choices = [("0", "zawsze"),("1", "po dniu"),("3", "po trzech dniach"),("7", "po tygodniu"),("30", "po miesiącu"),("-1", "nigdy")]) 
config.plugins.iptvplayer.showinextensions = ConfigYesNo(default = True)
config.plugins.iptvplayer.showinMainMenu = ConfigYesNo(default = False)
config.plugins.iptvplayer.ListaGraficzna = ConfigYesNo(default = True)
config.plugins.iptvplayer.NaszaSciezka = ConfigText(default = "/hdd/movie/", fixed_size = False)
config.plugins.iptvplayer.NaszPlik = ConfigText(default = "iptv.flv", fixed_size = False, visible_width = 8)
config.plugins.iptvplayer.buforowanie = ConfigYesNo(default = False)
config.plugins.iptvplayer.czasbuforowania = ConfigInteger(10, (5,120))
config.plugins.iptvplayer.NagrywanieRownolegle = ConfigYesNo(default = False)
config.plugins.iptvplayer.OpoznioneNagrywanie = ConfigSelection(default = "24x7", choices = [("24x7", "przez cały dzień"),("1x6", "pomiędzy 1:00 a 6:00"),("STNDBY", "w trybie uśpienia(sh4)")]) 
config.plugins.iptvplayer.AktualizacjaWmenu = ConfigYesNo(default = False)
config.plugins.iptvplayer.sortuj = ConfigYesNo(default = True)
config.plugins.iptvplayer.devHelper = ConfigYesNo(default = False)

try:
    import FreePlayer
    config.plugins.iptvplayer.NaszPlayer = ConfigSelection(default = "mini", choices = [("mini", "wewnętrzny"),("standard", "systemowy"),("freeplayer", "freeplayer")]) 
except:
    config.plugins.iptvplayer.NaszPlayer = ConfigSelection(default = "mini", choices = [("mini", "wewnętrzny"),("standard", "systemowy")]) 

config.plugins.iptvplayer.SciezkaCache = ConfigText(default = "/hdd/IPTVCache/", fixed_size = False)
config.plugins.iptvplayer.NaszaTMP = ConfigText(default = "/tmp/", fixed_size = False)
config.plugins.iptvplayer.ZablokujWMV = ConfigYesNo(default = True)
config.plugins.iptvplayer.mmsTOrtsp = ConfigYesNo(default = False)

config.plugins.iptvplayer.hd3d_login = ConfigText(default = "brak@brak.pl", fixed_size = False)
config.plugins.iptvplayer.hd3d_password = ConfigText(default = "brak", fixed_size = False)
config.plugins.iptvplayer.maxvideo_login = ConfigText(default = "", fixed_size = False)
config.plugins.iptvplayer.maxvideo_password = ConfigText(default = "", fixed_size = False)

config.plugins.iptvplayer.debugprint = ConfigSelection(default = "", choices = [("", "nie"),("console", "tak, na konsolę"),("debugfile", "tak, do pliku /hdd/iptv.dbg")]) 

config.plugins.iptvplayer.BlackList = ConfigYesNo(default = True)
config.plugins.iptvplayer.AutoSelecturl = ConfigYesNo(default = True)
config.plugins.iptvplayer.PrefferedServer = ConfigSelection(default = "putlocker", choices = [("putlocker", "putlocker"),("first", "pierwszy dostępny"),("last", "ostatni dostępny")]) 

#icons
config.plugins.iptvplayer.IconsSize = ConfigSelection(default = "135", choices = [("135", "135x135"),("120", "120x120"),("100", "100x100")]) 
config.plugins.iptvplayer.numOfRow = ConfigSelection(default = "0", choices = [("1", "1"),("2", "2"),("3", "3"),("4", "4"),("0", "auto")])
config.plugins.iptvplayer.numOfCol = ConfigSelection(default = "0", choices = [("1", "1"),("2", "2"),("3", "3"),("4", "4"),("5", "5"),("6", "6"),("7", "7"),("8", "8"),("0", "auto")])

config.plugins.iptvplayer.cleanup = ConfigYesNo(default = True)

########################################################
# Generate list of hosts options for Enabling/Disabling
########################################################
gListOfHostsNames = [] 
gListOfHostsNames = GetHostsList()
for hostName in gListOfHostsNames:
    try:
        printDBG("Set default options for host '%s'" % hostName)
        # as default all hosts are enabled
        exec('config.plugins.iptvplayer.host' + hostName + ' = ConfigYesNo(default = True)')
    except:
        printDBG("Options import for host '%s' EXEPTION" % hostName)

class ConfigMenu(Screen, ConfigListScreen):

    skin = """
    <screen name="IPTV config" position="center,center" size="540,440" title="" backgroundColor="#31000000" >

            <widget name="config" position="10,10" size="520,395" zPosition="1" transparent="0" backgroundColor="#31000000" scrollbarMode="showOnDemand" />
            <widget name="key_green" position="0,405" zPosition="2" size="100,35" valign="center" halign="right" font="Regular;22" transparent="1" foregroundColor="green" />
            <widget name="key_blue" position="100,405" zPosition="2" size="50,35" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="blue" />
            <widget name="key_red" position="150,405" zPosition="2" size="100,35" valign="center" halign="right" font="Regular;22" transparent="1" foregroundColor="red" />
            <widget name="key_yellow" position="250,405" zPosition="2" size="200,35" valign="center" halign="right" font="Regular;22" transparent="1" foregroundColor="yellow" />

    </screen>"""
    
    def __init__(self, session):
        Screen.__init__(self, session)
        
        # remember old
        self.showcoverOld = config.plugins.iptvplayer.showcover.value
        self.SciezkaCacheOld = config.plugins.iptvplayer.SciezkaCache.value

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
            exec( 'self.listConfigHostsEntries.append(getConfigListEntry("Player ' + hostName + ' więcej->[OK]", config.plugins.iptvplayer.host' + hostName + '))' )
        
        self.firstHostIdx = -1
        self.runSetup()
        self.onLayoutFinish.append(self.layoutFinished)
        
    def layoutFinished(self):
        self.setTitle("IPTV Player - ustawienia")

    def runSetup(self):

        # WYGLAD
        self.list = [ getConfigListEntry("Ikony na liście:", config.plugins.iptvplayer.showcover) ]
        if config.plugins.iptvplayer.showcover.value:
            self.list.append(getConfigListEntry("    Usuwaj ikony:", config.plugins.iptvplayer.deleteIcons))
        self.list.append(getConfigListEntry("Sortować listy?", config.plugins.iptvplayer.sortuj))            
        self.list.append(getConfigListEntry("Graficzna lista player-ów?", config.plugins.iptvplayer.ListaGraficzna))
        if config.plugins.iptvplayer.ListaGraficzna.value == True:
            self.list.append(getConfigListEntry("    Wielkość ikon", config.plugins.iptvplayer.IconsSize))
            self.list.append(getConfigListEntry("    Liczba wierszy", config.plugins.iptvplayer.numOfRow))
            self.list.append(getConfigListEntry("    Liczba kolumn", config.plugins.iptvplayer.numOfCol))
            
        self.list.append(getConfigListEntry("Katalog na dane cache:", config.plugins.iptvplayer.SciezkaCache))
        self.list.append(getConfigListEntry("Katalog na chwilowe dane (temp):", config.plugins.iptvplayer.NaszaTMP))
        
        #>>>>>>>>>> BUFOROWANIE <<<<<<<<<<
        self.list.append(getConfigListEntry("Włączyć tryb buforowania?", config.plugins.iptvplayer.buforowanie))
        if config.plugins.iptvplayer.buforowanie.value:
            self.list.append(getConfigListEntry("    Ścieżka dla nagrań/buforowania:", config.plugins.iptvplayer.NaszaSciezka))
            self.list.append(getConfigListEntry("    Buforuj przez (s):", config.plugins.iptvplayer.czasbuforowania))
            self.list.append(getConfigListEntry("    Nazwa pliku buforowania:", config.plugins.iptvplayer.NaszPlik))
        else:
            self.list.append(getConfigListEntry("Ścieżka dla nagrań:", config.plugins.iptvplayer.NaszaSciezka))

        self.list.append(getConfigListEntry("Nagrywanie równoległe?", config.plugins.iptvplayer.NagrywanieRownolegle))
        self.list.append(getConfigListEntry("Okienko nagrywania:", config.plugins.iptvplayer.OpoznioneNagrywanie))
        self.list.append(getConfigListEntry("Pomiń błędne linki?", config.plugins.iptvplayer.BlackList))
 
        self.list.append(getConfigListEntry("HD3D login:", config.plugins.iptvplayer.hd3d_login))
        self.list.append(getConfigListEntry("HD3D hasło:", config.plugins.iptvplayer.hd3d_password))
        self.list.append(getConfigListEntry("maxvideo.pl login:", config.plugins.iptvplayer.maxvideo_login))
        self.list.append(getConfigListEntry("maxvideo.pl hasło:", config.plugins.iptvplayer.maxvideo_password))
  
        self.list.append(getConfigListEntry("Wybór odtwarzacza:", config.plugins.iptvplayer.NaszPlayer))
        self.list.append(getConfigListEntry("Blokuj pliki wmv? (wymaga licencjonowanego sterownika):", config.plugins.iptvplayer.ZablokujWMV))
        self.list.append(getConfigListEntry("Zamiana mms na rtsp?:", config.plugins.iptvplayer.mmsTOrtsp))

        self.list.append(getConfigListEntry("Wyświetlać wtyczkę na liście rozszerzeń?", config.plugins.iptvplayer.showinextensions))
        self.list.append(getConfigListEntry("Wyświetlać wtyczkę w głównym menu?", config.plugins.iptvplayer.showinMainMenu))
        self.list.append(getConfigListEntry("Wyświetlać aktualizację w głównym menu?", config.plugins.iptvplayer.AktualizacjaWmenu))
        self.list.append(getConfigListEntry("Włączyć DEBUG?", config.plugins.iptvplayer.debugprint))
        #self.list.append(getConfigListEntry("automatyczny wybór linka?", config.plugins.iptvplayer.AutoSelecturl))
        #self.list.append(getConfigListEntry("Preferowany serwer:", config.plugins.iptvplayer.PrefferedServer))
        self.list.append(getConfigListEntry("Wyłączyć ochronę hostów? (Błąd wywołuje GS)", config.plugins.iptvplayer.devHelper))
        self.list.append(getConfigListEntry("Czyszczenie przy aktualizacji?", config.plugins.iptvplayer.cleanup))
        
        self.firstHostIdx = len(self.list)
        
        for hostConfItem in  self.listConfigHostsEntries:
            self.list.append( hostConfItem )
        
        self["config"].list = self.list
        self["config"].setList(self.list)

    def keyUpdate(self):
        self.save()

        #aktualizacja
        from iptvtools import UpdateIPTV_from_GIT as iptvtools_UpdateIPTV_from_GIT, FreeSpace as iptvtools_FreeSpace
        WersjaGIT=iptvtools_GetGITversion()
        msgtxt = 'Autorzy NIE ponoszą, żadnej odpowiedzialności za uszkodzenia tunera spowodowane działaniem tej wtyczki oraz wykorzystywaniem jej w celu nielegalnego pobierania materiałów video!!!'
        if iptvtools_FreeSpace(config.plugins.iptvplayer.NaszaTMP.value,2):
            StatusUpdate = iptvtools_UpdateIPTV_from_GIT(config.plugins.iptvplayer.NaszaTMP.value)
            if StatusUpdate == "OK":
                self.session.open(MessageBox, "Restart oPLI po aktualizacji wtyczki do wersji %s...\n Czytałeś już licencję?\nJeśli tak, to wiesz, że\n\n" % WersjaGIT + msgtxt, type = MessageBox.TYPE_INFO, timeout = 5 )
                from enigma import quitMainloop
                quitMainloop(3) 
            else:
                self.session.open(MessageBox, "Błąd aktualizacji wtyczki, spróbuj ponownie za jakiś czas.\n Status: %s \n\n Dla przypomnienia -\n\n" % StatusUpdate + msgtxt, type = MessageBox.TYPE_INFO, timeout = 10 )
                return
        else:
            self.session.open(MessageBox, "Brak wolnego miejsca w katalogu %s" % (config.plugins.iptvplayer.NaszaTMP.value), type = MessageBox.TYPE_INFO, timeout = 10 )
            return

    def keySave(self):
        self.save()
        self.close()
    
    def save(self):
        for x in self["config"].list:
            x[1].save()
        configfile.save()
        
        if self.showcoverOld != config.plugins.iptvplayer.showcover.value or \
           self.SciezkaCacheOld != config.plugins.iptvplayer.SciezkaCache.value:
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
        if self["config"].getCurrent()[1] in [config.plugins.iptvplayer.buforowanie,
                                              config.plugins.iptvplayer.showcover,
                                              config.plugins.iptvplayer.ListaGraficzna,
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
            