from Tools.Directories import resolveFilename, SCOPE_PLUGINS, fileExists
import os
import sys
from iptvtools import printDBG

def CleanUp(MyPath = '', resolve=True):
    if len(MyPath) > 5:
        if resolve == True:
            MyFile = resolveFilename(SCOPE_PLUGINS, "Extensions/IPTVPlayer/" + MyPath)
        else:
            MyFile = MyPath
        if fileExists(MyFile):
            try:
                os.remove(MyFile)
            except:
                os.system("rm -rf " + MyFile)

try:
    CleanUp('/hdd/iptv.dbg', False)
except:
    pass
try:
    #if  os.path.isfile("/proc/stb/info/vumodel"): #zablokowanie VU+ jest banalne, wiec troche szacunku do naszej pracy. Myslicie ze nie potrafie zrobic tego w CPP :P
    #    CleanUp('')
    import platform
    platformName = platform.machine()
    if platformName[:4] == '7401': # DM800HD clon
        platformName = 'mips'
    elif platformName[:4] == '7405': # DM800SE clon '7405d0-smp', DM500HD clon '7405b0-smp'
        platformName = 'mips'
    elif platformName[:4] == '7400': # DM8000 7400d0-smp clon
        platformName = 'mips'
       
except:
    if sys.version.find('STMicroelectronics') > 1:
        platformName = 'sh4'
        printDBG( "IPTV.init: brak modulu platform.py, inicjacja sh4 na podstawie python.version" )
    else:
        printDBG( "IPTV.init: brak modulu platform.py, inicjacja mips na podstawie python.version" )
        platformName = 'mips'

try:
    #j00zek:initial setup of the script
    if platformName == 'sh4':
        printDBG( "[IPTV.init] inicjacja sh4")
        if not fileExists(resolveFilename(SCOPE_PLUGINS, "Extensions/IPTVPlayer/iptv.rekorder")) and fileExists('/usr/lib/libssl.so.0.9.8'):
            os.symlink(resolveFilename(SCOPE_PLUGINS, "Extensions/IPTVPlayer/wget.sh4"), resolveFilename(SCOPE_PLUGINS, "Extensions/IPTVPlayer/iptv.rekorder"))
        if not fileExists(resolveFilename(SCOPE_PLUGINS, "Extensions/IPTVPlayer/iptv.wget")) and fileExists('/usr/lib/libssl.so.0.9.8'):
            os.symlink(resolveFilename(SCOPE_PLUGINS, "Extensions/IPTVPlayer/wget.sh4"), resolveFilename(SCOPE_PLUGINS, "Extensions/IPTVPlayer/iptv.wget"))
        os.system("chmod 775 %s" % resolveFilename(SCOPE_PLUGINS, "Extensions/IPTVPlayer/wget.sh4"))
        CleanUp('wget.mips')
    elif platformName == 'mips':
        printDBG( "[IPTV.init] inicjacja mips")
        if not fileExists(resolveFilename(SCOPE_PLUGINS, "Extensions/IPTVPlayer/iptv.rekorder")):
            os.symlink(resolveFilename(SCOPE_PLUGINS, "Extensions/IPTVPlayer/wget.mips"), resolveFilename(SCOPE_PLUGINS, "Extensions/IPTVPlayer/iptv.rekorder"))
        if not fileExists(resolveFilename(SCOPE_PLUGINS, "Extensions/IPTVPlayer/iptv.wget")):
            os.symlink(resolveFilename(SCOPE_PLUGINS, "Extensions/IPTVPlayer/wget.mips"), resolveFilename(SCOPE_PLUGINS, "Extensions/IPTVPlayer/iptv.wget"))
        os.system("chmod 775 %s" % resolveFilename(SCOPE_PLUGINS, "Extensions/IPTVPlayer/wget.mips"))
        CleanUp('wget.sh4')
    else:
        printDBG( "[IPTV.init] nieznana platforma sprzetowa !!!")
        CleanUp('iptv.rekorder')
        CleanUp('iptv.wget')

    #os.system("chmod 775 %s" % resolveFilename(SCOPE_PLUGINS, "Extensions/IPTVPlayer/iptv.wget"))
    os.system("chmod 775 %s" % resolveFilename(SCOPE_PLUGINS, "Extensions/IPTVPlayer/iptv.buffering"))
    os.system("chmod 775 %s" % resolveFilename(SCOPE_PLUGINS, "Extensions/IPTVPlayer/iptv.recording"))
    CleanUp('libs/tarfile.py')
    CleanUp('libs/simplejson')
    if fileExists(resolveFilename(SCOPE_PLUGINS, "Extensions/IPTVPlayer/hostipla_blocked_due_privacy_policy.py")):
        CleanUp('hostipla.py')
        CleanUp('hostipla.pyo')
        CleanUp('hostipla.pyc')


except OSError:
    printDBG( "[IPTV.init] blad konfiguracji!!!" )
                