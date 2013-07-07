from Components.GUIComponent import GUIComponent
from enigma import eListboxPythonMultiContent, eListbox, gFont, \
    RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_VALIGN_CENTER
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import resolveFilename, SCOPE_PLUGINS

from ihost import CDisplayListItem

class IPTVListComponent(GUIComponent, object):
    ICON_CATEGORY = 'Extensions/IPTVPlayer/icons/CategoryItem.png'
    ICON_VIDEO = 'Extensions/IPTVPlayer/icons/VideoItem.png'
    ICON_SEARCH = 'Extensions/IPTVPlayer/icons/SearchItem.png'
    ICON_NEWTHREAD = 'Extensions/IPTVPlayer/icons/forum_new.png'
    ICON_OLDTHREAD = 'Extensions/IPTVPlayer/icons/forum_old.png' 
    def buildEntry(self, item):
        width = self.l.getItemSize().width()
        res = [ None ]

        res.append((eListboxPythonMultiContent.TYPE_TEXT, 45, 3, width-45, 20, 1, RT_HALIGN_LEFT|RT_VALIGN_CENTER, item.name))
        
        if CDisplayListItem.TYPE_CATEGORY == item.type:
            res.append((eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST, 3, 1, 33, 33, self.categoryPIX))
        elif CDisplayListItem.TYPE_VIDEO == item.type:
            res.append((eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST, 3, 1, 33, 33, self.videoPIX))
        elif CDisplayListItem.TYPE_SEARCH == item.type:
            res.append((eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST, 3, 1, 33, 33, self.searchPIX))
        elif CDisplayListItem.TYPE_NEWTHREAD == item.type:
            res.append((eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST, 3, 1, 33, 33, self.newthreadPIX))
        elif CDisplayListItem.TYPE_OLDTHREAD == item.type:
            res.append((eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST, 3, 1, 33, 33, self.oldthreadPIX))
         
        return res

    def __init__(self):
        GUIComponent.__init__(self)
        self.l = eListboxPythonMultiContent()
        self.l.setFont(0, gFont("Regular", 24))
        self.l.setFont(1, gFont("Regular", 18))
  
        self.l.setBuildFunc(self.buildEntry)
        #self.l.setItemHeight(65)
        self.l.setItemHeight(35)
        self.onSelectionChanged = [ ]
        
        try:
            self.categoryPIX = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, IPTVListComponent.ICON_CATEGORY))
            self.videoPIX = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, IPTVListComponent.ICON_VIDEO))
            self.searchPIX = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, IPTVListComponent.ICON_SEARCH))
            self.newthreadPIX = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, IPTVListComponent.ICON_NEWTHREAD))
            self.oldthreadPIX = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, IPTVListComponent.ICON_OLDTHREAD))
        except:
            self.categoryPIX = None
            self.videoPIX = None
            self.searchPIX = None
            self.newthreadPIX = None
            self.oldthreadPIX = None
            print("Problem with loading markers for IPTV List")

    def connectSelChanged(self, fnc):
        if not fnc in self.onSelectionChanged:
            self.onSelectionChanged.append(fnc)

    def disconnectSelChanged(self, fnc):
        if fnc in self.onSelectionChanged:
            self.onSelectionChanged.remove(fnc)

    def selectionChanged(self):
        for x in self.onSelectionChanged:
            x()
   
    def getCurrent(self):
        cur = self.l.getCurrentSelection()
        return cur and cur[0]
   
    GUI_WIDGET = eListbox
   
    def postWidgetCreate(self, instance):
        instance.setContent(self.l)
        instance.selectionChanged.get().append(self.selectionChanged)

    def preWidgetRemove(self, instance):
        instance.setContent(None)
        instance.selectionChanged.get().remove(self.selectionChanged)

    def moveToIndex(self, index):
        self.instance.moveSelectionTo(index)

    def getCurrentIndex(self):
        return self.instance.getCurrentIndex()

    def setList(self, list):
        self.l.setList(list)
        
    currentIndex = property(getCurrentIndex, moveToIndex)
    currentSelection = property(getCurrent)
