# -*- coding: utf-8 -*-
#
#  Player Selector
#
#  $Id$
#
# 
###################################################
# LOCAL import
###################################################
from tools import printDBG
try:
    from _version import version as wersja
except:
    wersja="XX.YY"

###################################################
# FOREIGN import
###################################################
from Components.ActionMap import ActionMap, HelpableActionMap
from Components.config import config
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.ProgressBar import ProgressBar
from enigma import ePicLoad, ePoint, getDesktop, eTimer, ePixmap, eEPGCache, eServiceReference
from Screens.Screen import Screen
from ServiceReference import ServiceReference
import threading
from time import localtime, time, strftime
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_SKIN_IMAGE, pathExists
from Tools.LoadPixmap import LoadPixmap

class Cover2(Pixmap):
    def __init__(self):
        Pixmap.__init__(self)
        self.picload = ePicLoad()
        self.picload.PictureData.get().append(self.paintIconPixmapCB)
        self.paramsSet = False

    def onShow(self):
        Pixmap.onShow(self)

    def paintIconPixmapCB(self, picInfo=None):
        t = threading.currentThread()
        ptr = self.picload.getData()
        if ptr != None:
            self.instance.setPixmap(ptr)
            self.show()

    def updateIcon(self, filename):
        t = threading.currentThread()
        if not self.paramsSet:
            self.picload.setPara((self.instance.size().width(), self.instance.size().height(), 1, 1, False, 1, "#00000000"))
            self.paramsSet = True
        self.picload.startDecode(filename)

class Cover3(Pixmap):
    def __init__(self):
        Pixmap.__init__(self)
        
    def onShow(self):
        Pixmap.onShow(self)

    def setPixmap(self, ptr):
        self.instance.setPixmap(ptr)

class SelectorWidget(Screen):
   
    def __init__(self, session, list, CurIdx = 0, sSL = None):
        self.currList = list
        self.sServiceList = sSL
        # numbers of items in self.currList
        self.numOfItems = len(self.currList)
        # load icons
        self.pixmapList = []
        for idx in range(0,self.numOfItems):
        #print resolveFilename(SCOPE_SKIN_IMAGE, 'picon/' + '_'.join(self.currList[idx][0].split(':',10)[:10]) + '.png')
            #self.pixmapList.append(LoadPixmap(resolveFilename(SCOPE_SKIN_IMAGE, 'picon/' + '_'.join(self.currList[idx][0].split(':',10)[:10]) + '.png')) )
            if pathExists(resolveFilename(SCOPE_SKIN_IMAGE, 'picon/' + '_'.join(self.currList[idx][0].split(':',10)[:10]) + '.png')):
                self.pixmapList.append("NONE")
            else:
                self.pixmapList.append("ShowName")

        sz_w = getDesktop(0).size().width() - 10
        sz_h = getDesktop(0).size().height() - 10
        if config.plugins.SparkWall.usePIG.value == True:
            try:
                PIG_X = int(config.plugins.SparkWall.PIGSize.value.split('x')[0])
                PIG_Y = int(config.plugins.SparkWall.PIGSize.value.split('x')[1])
            except:
                PIG_X = 0
                PIG_Y = 0

        # image size 100x60
        coverWidth = int(config.plugins.SparkWall.IconsSize.value.split('x')[0])
        coverHeight = int(config.plugins.SparkWall.IconsSize.value.split('x')[1])
        
         # marker size should be larger than img
        markerWidth = 10 + coverWidth
        markerHeight = 10 + coverHeight
        self.markerPixmap = LoadPixmap(resolveFilename(SCOPE_PLUGINS, 'Extensions/SparkWall/icons/marker%i.png' % coverWidth))
        
        # space/distance between images
        disWidth = markerWidth - coverWidth
        disHeight = markerHeight - markerHeight
        
        # position of first img = 0 + <overscan> + <size PIG> + <space between images>
        offsetCoverX = 30 + PIG_X + disWidth
        offsetCoverY = 30
        
        # position of first marker 
        offsetMarkerX = offsetCoverX - (markerWidth - coverWidth)/2
        offsetMarkerY = offsetCoverY - (markerHeight - coverHeight)/2

        #calculate rows/columns
        numOfCol = int((sz_w - 30 - PIG_X - 30)/markerWidth)
        numOfRow = int((sz_h - 20 - 20)/markerHeight)
      
        # how to calculate position of image with indexes indxX, indxY:
        #posX = offsetCoverX + (coverWidth + disWidth) * indxX
        #posY = offsetCoverY + (coverHeight + disHeight) * indxY
        
        # how to calculate position of marker for image with posX, posY
        #markerPosX = posX - (markerWidth - coverWidth)/2
        #markerPosY = posY - (markerHeight - coverHeight)/2
        
        tmpX = coverWidth + disWidth
        tmpY = coverHeight + disHeight
        
        self.numOfRow = numOfRow
        self.numOfCol = numOfCol
        # position of first cover
        self.offsetCoverX = offsetCoverX
        self.offsetCoverY = offsetCoverY
        # space/distance between images
        self.disWidth = disWidth
        self.disHeight = disHeight
        # image size
        self.coverWidth = coverWidth
        self.coverHeight = coverHeight
        # marker size should be larger than img
        self.markerWidth = markerWidth
        self.markerHeight = markerHeight

        # numbers of lines
        self.numOfLines = self.numOfItems / self.numOfCol
        if self.numOfItems % self.numOfCol > 0:
            self.numOfLines += 1

        # numbers of pages
        self.numOfPages = self.numOfLines / self.numOfRow
        if self.numOfLines % self.numOfRow > 0:
            self.numOfPages += 1

        self.currPage = int(CurIdx/(self.numOfCol*self.numOfRow))
        self.currLine = int((CurIdx - self.currPage*numOfCol*self.numOfRow)/self.numOfCol)

        self.dispX = CurIdx - self.currPage * self.numOfCol * self.numOfRow - self.currLine * self.numOfCol
        self.dispY = self.currLine
        
        print "Dane"
        print CurIdx
        print self.numOfCol
        print self.numOfRow
        print self.currPage
        print self.currLine
        print self.dispX
        print self.dispY

#            <eLabel                       position="30,%d" size="%d,3"                zPosition="4" backgroundColor="#f4f4f4"/>
        skin = """
            <screen name="SkypeWallWidget" position="center,center" title="" size="%d,%d">
            <widget source="session.VideoPicture" position="30,30" size="417,243" render="Pig" backgroundColor="transparent" zPosition="1" />
            <widget name="marker"         position="%d,%d" size="%d,%d" zPosition="2" transparent="1" alphatest="on" />
            <widget name="curChannelName" position="30,%d" size="%d,30" font="Regular;26" halign="center" valign="center" transparent="1" zPosition="1"/>
            <widget name="NowEventTitle"  position="30,%d" size="%d,28" font="Regular;24" halign="center" valign="center" transparent="1" zPosition="2" foregroundColor="#fcc000" />
            <widget name="NowEventStart"  position="30,%d" size="%d,28" font="Regular;24" halign="left"   valign="center" transparent="1" zPosition="2" foregroundColor="#fcc000" />
            <widget name="vzProgress"     position="30,%d" size="%d,3"  transparent="1" zPosition="5" borderColor="#00c1ea02"/>
            <widget name="NowDuration"    position="30,%d" size="%d,28" font="Regular;24" halign="right"  valign="center" transparent="1" zPosition="2" foregroundColor="#fcc000" />
            <widget name="NextEventTitle" position="30,%d" size="%d,28" font="Regular;24" halign="center"   valign="center" transparent="1" zPosition="2"/>
            <widget name="NextEventStart" position="30,%d" size="%d,28" font="Regular;24" halign="left"   valign="center" transparent="1" zPosition="2"/>
            <widget name="NextDuration"   position="30,%d" size="%d,28" font="Regular;24" halign="right"  valign="center" transparent="1" zPosition="2"/>

            
            """  %(
                sz_w, sz_h, #wielkosc glownego okna
                offsetMarkerX, offsetMarkerY, # first marker position
                markerWidth, markerHeight,    # marker size
                30 + PIG_Y + 10, PIG_X, # widget name="curChannelName"
                30 + PIG_Y + 10 + 40, PIG_X, # widget name="NowEventTitle"
                30 + PIG_Y + 10 + 40 + 30, PIG_X, # widget name="NowEventStart"
                30 + PIG_Y + 10 + 40 + 30 + 30 + 5, PIG_X, # widget name="vzProgress"
                #30 + PIG_Y + 10 + 40 + 30 + 30 + 5, PIG_X, # eLabel
                30 + PIG_Y + 10 + 40 + 30, PIG_X, # widget name="NowDuration"
                30 + PIG_Y + 10 + 40 + 30 + 30 + 5 + 30, PIG_X, # widget name="NextEventTitle"
                30 + PIG_Y + 10 + 40 + 30 + 30 + 5 + 30 + 30, PIG_X, # widget name="NextEventStart"
                30 + PIG_Y + 10 + 40 + 30 + 30 + 5 + 30 + 30, PIG_X, # widget name="NextDuration"
                )
                
        for y in range(1,numOfRow+1):
            for x in range(1,numOfCol+1):
                skinCoverLine = """<widget name="chname_%s%s" position="%d,%d" size="%d,%d" font="Regular;20" halign="center" valign="center" transparent="1"/>""" % (x, y, 
                    (offsetCoverX + tmpX * (x - 1) ), # pos X image
                    (offsetCoverY + tmpY * (y - 1) ), # pos Y image
                    coverWidth, 
                    coverHeight
                )
                skin += '\n' + skinCoverLine
            for x in range(1,numOfCol+1):
                skinCoverLine = """<widget name="cover_%s%s" zPosition="4" position="%d,%d" size="%d,%d" transparent="1" alphatest="on" />""" % (x, y, 
                    (offsetCoverX + tmpX * (x - 1) ), # pos X image
                    (offsetCoverY + tmpY * (y - 1) ), # pos Y image
                    coverWidth, 
                    coverHeight
                )
                skin += '\n' + skinCoverLine
        skin += '</screen>'
                
        self.skin = skin
            
        self.session = session
        Screen.__init__(self, session)
        
        self.session.nav.event.append(self.__event)
        
        if list == None or len(list) <= 0:
            self.close(None)
            
        self["actions"] = ActionMap(["WizardActions", "DirectionActions", "ColorActions"],
        {
            "ok": self.ok_pressed,
            "back": self.back_pressed,
            "left": self.keyLeft,
            "right": self.keyRight,
            "up": self.keyUp,
            "down": self.keyDown,
        }, -1)
        
        self["curChannelName"] = Label(self.currList[CurIdx][1])
        self["marker"] = Cover3()

        self["NowEventStart"] = Label()
        self["NextEventStart"] = Label()
        self["NowEventEnd"] = Label()
        self["NextEventEnd"] = Label()
        self["NowEventTitle"] = Label()
        self["NextEventTitle"] = Label()
        self["NowDuration"] = Label()
        self["NextDuration"] = Label()
        self["vzProgress"] = ProgressBar()
        
        chnameidx = -1
        for y in range(1,self.numOfRow+1):
            for x in range(1,self.numOfCol+1):
                chnameidx += 1
                #name, in case of no picon
                chnameIndex = "chname_%s%s" % (x,y)
                self[chnameIndex] = Label(self.currList[chnameidx][1])
                #picons
                strIndex = "cover_%s%s" % (x,y)
                if config.plugins.SparkWall.ScaleIcons.value == False:
                    self[strIndex] = Cover3()
                else:
                    self[strIndex] = Cover2()

        self.epgcache = eEPGCache.getInstance()
                
        self.onLayoutFinish.append(self.onStart)
        self.visible = True
        
        self.zap = False
        if config.plugins.SparkWall.ZapMode.value == "2ok":
            self.zap = True
        
        
    #Calculate marker position Y
    def calcMarkerPosY(self):
        
        if self.currLine >  (self.numOfLines - 1):
            self.currLine = 0
        elif self.currLine < 0:
            self.currLine = (self.numOfLines - 1)
        
        # calculate new page number 
        newPage = self.currLine / self.numOfRow
        if newPage != self.currPage:
            self.currPage = newPage
            self.updateLabels()
            self.updateIcons()
        
        # calculate dispY pos 
        self.dispY = self.currLine - self.currPage * self.numOfRow 
        
        # if we are in last line dispX pos 
        # must be also corrected
        if self.currLine ==  (self.numOfLines - 1):
            self.numItemsInLine = self.numOfItems - ((self.numOfLines - 1) * self.numOfCol) 
            if self.dispX > (self.numItemsInLine - 1):
                self.dispX = self.numItemsInLine - 1
            
        return
        

    #Calculate marker position X
    def calcMarkerPosX(self):
        if self.currLine == self.numOfLines - 1:
            #calculate num of item in last line
            self.numItemsInLine = self.numOfItems - ((self.numOfLines - 1) * self.numOfCol) 
        else:
            self.numItemsInLine = self.numOfCol

        if self.dispX > (self.numItemsInLine - 1):
            self.dispX = 0
        elif self.dispX < 0:
            self.dispX = self.numItemsInLine - 1

        return
        
    def onStart(self):
        self.VideoSize()
        self["marker"].setPixmap( self.markerPixmap )
        self.updateIcons()
        self.moveMarker()
        return
        
    def fillpixmapList(self):
        for idx in range(0,self.numOfItems):
            if self.pixmapList[idx] == "NONE":
                self.pixmapList.append(LoadPixmap(resolveFilename(SCOPE_SKIN_IMAGE, 'picon/' + '_'.join(self.currList[idx][0].split(':',10)[:10]) + '.png')))
        return
        
        
    def updateLabels(self):
        idx = self.currPage * (self.numOfCol*self.numOfRow)
        for y in range(1,self.numOfRow+1):
            for x in range(1,self.numOfCol+1):
                chnameIndex = "chname_%s%s" % (x,y)
                if idx < self.numOfItems:
                    if self.pixmapList[idx] == "ShowName":
                        self[chnameIndex].setText(self.currList[idx][1])
                        idx += 1
                    else:
                        self[chnameIndex].setText("")
                else:
                    self[chnameIndex].setText("")
                        

    def updateIcons(self):
        idx = self.currPage * (self.numOfCol*self.numOfRow)
        for y in range(1,self.numOfRow+1):
            for x in range(1,self.numOfCol+1):
                chnameIndex = "chname_%s%s" % (x,y)
                strIndex = "cover_%s%s" % (x,y)
                print("updateIcon for self[%s]" % strIndex)
                if idx < self.numOfItems:
                    if config.plugins.SparkWall.ScaleIcons.value == True:
                        self[strIndex].updateIcon(resolveFilename(SCOPE_SKIN_IMAGE, 'picon/' + '_'.join(self.currList[idx][0].split(':',10)[:10]) + '.png'))
                    else:
                        if self.pixmapList[idx] == "NONE":
                            self.pixmapList[idx] = LoadPixmap(resolveFilename(SCOPE_SKIN_IMAGE, 'picon/' + '_'.join(self.currList[idx][0].split(':',10)[:10]) + '.png'))
                            #self.pixmapList[idx] = updateIcon(resolveFilename(SCOPE_SKIN_IMAGE, 'picon/' + '_'.join(self.currList[idx][0].split(':',10)[:10]) + '.png'))
                        try:
                            self[strIndex].setPixmap(self.pixmapList[idx])
                            self[strIndex].show()
                        except: pass
                    idx += 1
                else:
                    self[strIndex].hide()
    
    def __del__(self):       
        return
        
    def __onClose(self):
        return
        
    def keyRight(self):
        self.dispX += 1
        self.calcMarkerPosX()
        self.moveMarker()
        return
    def keyLeft(self):
        self.dispX -= 1
        self.calcMarkerPosX()
        self.moveMarker()
        return

    def keyDown(self):
        self.currLine += 1
        self.calcMarkerPosY()
        self.moveMarker()
        return
    def keyUp(self):
        self.currLine -= 1
        self.calcMarkerPosY()
        self.moveMarker()
        return
    
    def moveMarker(self):

        # calculate position of image
        imgPosX = self.offsetCoverX + (self.coverWidth + self.disWidth) * self.dispX
        imgPosY = self.offsetCoverY + (self.coverHeight + self.disHeight) * self.dispY

        # calculate postion of marker for current image
        x = imgPosX - (self.markerWidth - self.coverWidth)/2
        y = imgPosY - (self.markerHeight - self.coverHeight)/2
        
        #x =  30 + self.dispX * 180
        #y = 130 + self.dispY * 125
        self["marker"].instance.move(ePoint(x,y))
        
        idx = self.currLine * self.numOfCol +  self.dispX
        self["curChannelName"].setText(self.currList[idx][1])
        
        current = ServiceReference(self.currList[idx][0])
        nowepg, nowstart, nowend, nowname, nowduration, percentnow = self.getEPGNowNext(current.ref,0)
        nextepg, nextstart, nextend, nextname, nextduration, percentnext = self.getEPGNowNext(current.ref,1)
        self["NowEventStart"].setText(nowstart)
        self["NextEventStart"].setText(nextstart)
        self["NowEventEnd"].setText(nowend)
        self["NextEventEnd"].setText(nextend)
        self["NowEventTitle"].setText(nowname)
        self["NextEventTitle"].setText(nextname)
        self["NowDuration"].setText(nowduration)
        self["NextDuration"].setText(nextduration)
        self["vzProgress"].setValue(percentnow)
        if config.plugins.SparkWall.ZapMode.value == "2ok": self.zap = True
        return

    def back_pressed(self):
        self.close(None)
        return
    
    def hideWindow(self):
        self.visible = False
        self.hide()

    def showWindow(self):
        self.visible = True
        self.show()

    def Error(self, error = None):
        pass
        
    def __event(self, ev):
        pass
        
    def getEPGNowNext(self, ref, modus):
        # get now || next event
        if self.epgcache is not None:
            event = self.epgcache.lookupEvent(['IBDCT', (ref.toString(), modus, -1)])
            if event:
                if event[0][4]:
                    t = localtime(event[0][1])
                    begin = event[0][1]
                    duration = event[0][2]
                    now = int(time())
                    if modus == 0:
                        eventduration =_("+%d min") % (((event[0][1] + duration) - time()) / 60)
                        percent = int((now - begin) * 100 / duration)
                        eventname = event[0][4]
                        eventstart = strftime("%H:%M", localtime(begin))
                        eventend = strftime("%H:%M", localtime(begin + duration))
                        eventtimename = ("%02d:%02d   %s") % (t[3],t[4], event[0][4])
                    elif modus == 1:
                        eventduration =_("%d min") % (duration / 60)
                        percent = 0
                        eventname = event[0][4]
                        eventstart = strftime("%H:%M", localtime(begin))
                        eventend = strftime("%H:%M", localtime(begin + duration))
                        eventtimename = ("%02d:%02d   %s") % (t[3],t[4], event[0][4])
                    return eventtimename, eventstart, eventend, eventname, eventduration, percent
                else:
                    return _("No EPG data"), "", "", _("No EPG data"), "", ""
        return _("No EPG data"), "", "", _("No EPG data"), "", ""

    def VideoSize(X = 30, Y=30, W=417, H=253):
        mypath='/proc/stb/vmpeg/0/dst_all'
        try:
            f = open(mypath, "w")
            f.write('%s,%s,%s,%s' % (hex(int(X)),hex(int(Y)),hex(int(W)),hex(int(H))))
            f.close()
        except IOError:
            pass
        return
    
    def ok_pressed(self):
        idx = self.currLine * self.numOfCol +  self.dispX
        if idx < self.numOfItems:
            print "[SparkWall:selector:ok_pressed] selected " + str(self.currList[idx][0])
            if self.zap == True:
                printDBG("[SparkWall] preview host")
                service = eServiceReference(self.currList[idx][0])
                self.sServiceList.setCurrentSelection(service) #wybieramy serwis na liscie
                self.sServiceList.zap(enable_pipzap = True) # i przelaczamy 
                self.VideoSize()
                self.zap = False
            else:
                self.close(self.currList[idx])
        else:
            self.close(None)
        return