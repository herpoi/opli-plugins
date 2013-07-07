from Screens.InfoBarGenerics import Screen, InfoBarSeek, InfoBarAudioSelection, InfoBarCueSheetSupport, InfoBarNotifications, \
    InfoBarShowHide, InfoBarServiceErrorPopupSupport, \
    InfoBarPVRState, InfoBarSimpleEventView, InfoBarServiceNotifications, \
    InfoBarMoviePlayerSummarySupport, InfoBarSubtitleSupport, InfoBarTeletextPlugin

from Screens.HelpMenu import HelpableScreen
from Components.ActionMap import HelpableActionMap
from Components.config import config
from Components.AVSwitch import eAVSwitch
from Screens.ChoiceBox import ChoiceBox


class customMoviePlayer(InfoBarShowHide, \
        InfoBarSeek, InfoBarAudioSelection, HelpableScreen, InfoBarNotifications,
        InfoBarServiceNotifications, InfoBarPVRState, InfoBarCueSheetSupport, InfoBarSimpleEventView,
        InfoBarMoviePlayerSummarySupport, Screen, InfoBarTeletextPlugin,
        InfoBarServiceErrorPopupSupport):

    STATE_IDLE = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    ENABLE_RESUME_SUPPORT = True
    ALLOW_SUSPEND = True
    
        
    def __init__(self, session, service):
        Screen.__init__(self, session)        
        self.skinName = "MoviePlayer"
        
        self["actions"] = HelpableActionMap(self, "MoviePlayerActions",
            {
                "aspectChange": (self.aspectChange, _("changing aspect")),
                "leavePlayer": (self.leavePlayer, _("leave movie player...")),
                "audioSelection": (self.audioSelection, _("Audio Options..."))
            }, -5)
            
        self["MediaPlayerActions"] = HelpableActionMap(self, "MediaPlayerActions",
            {
                "previous": (self.previousMarkOrEntry, _("play from previous mark or playlist entry")),
                "next": (self.nextMarkOrEntry, _("play from next mark or playlist entry")),
                "aspectratio" : (self.aspectChange, _("AspectRatioChange")),
            }, -2)
        
        for x in HelpableScreen, InfoBarShowHide, \
                InfoBarSeek, \
                InfoBarAudioSelection, InfoBarNotifications, InfoBarSimpleEventView, \
                InfoBarServiceNotifications, InfoBarPVRState, InfoBarCueSheetSupport, \
                InfoBarMoviePlayerSummarySupport, \
                InfoBarTeletextPlugin, InfoBarServiceErrorPopupSupport:
            x.__init__(self)
                    
        self.onClose.append(self.__onClose)
        self.session.nav.playService(service)
        #self.doSeek(0)
        self.returning = False
        self.aspectratiomode = "1"
    
    def nextMarkOrEntry(self):
        if not self.jumpPreviousNextMark(lambda x: x):
            self.is_closing = True
            self.close(1)

    def previousMarkOrEntry(self):
        if not self.jumpPreviousNextMark(lambda x:-x - 5 * 90000, start=True):
            self.is_closing = True
            self.close(-1)
    
    def aspectChange(self):
        print "Aspect Ratio"
        print  self.aspectratiomode
        if self.aspectratiomode == "1": #letterbox
            eAVSwitch.getInstance().setAspectRatio(0)
            self.aspectratiomode = "2"
            return
        elif self.aspectratiomode == "2": #nonlinear
            #eAVSwitch.getInstance().setAspectRatio(4)
            self.aspectratiomode = "3"
        elif self.aspectratiomode == "2": #nonlinear
            eAVSwitch.getInstance().setAspectRatio(2)
            self.aspectratiomode = "3"
        elif self.aspectratiomode == "3": #panscan
            eAVSwitch.getInstance().setAspectRatio(3)
            self.aspectratiomode = "1"        
            
    def leavePlayer(self):
        self.is_closing = True

        if config.usage.on_movie_stop.value == "ask":
            list = []
            list.append((_("Tak"), "quit"))
            list.append((_("Nie"), "continue"))
            if config.usage.setup_level.index >= 2: # expert+
                list.append((_("Od poczatku"), "restart"))
            self.session.openWithCallback(self.leavePlayerConfirmed, ChoiceBox, title=_("Zatrzymac odtwarzanie tego video?"), list=list)
        else:
            self.close(0)

    def leavePlayerConfirmed(self, answer):
        answer = answer and answer[1]
        if answer == "quit":
            self.close(0)
        elif answer == "restart":
            self.doSeek(0)

    def doEofInternal(self, playing):
        print "--- eofint movieplayer ---"
        self.is_closing = True
        self.close(1)
        
    def __onClose(self):
        self.session.nav.playService(None)
        
#####################################################
# movie player by j00zek
#####################################################
from Screens.InfoBar import MoviePlayer as standardMoviePlayer
from enigma import eServiceReference

class IPTVStandardMoviePlayer(standardMoviePlayer):
    def __init__(self, session, IplaFile, IplaFileName):
        self.session = session
        self.WithoutStopClose = True
        fileRef = eServiceReference(4097,0,IplaFile)
        fileRef.setName (IplaFileName)

        standardMoviePlayer.__init__(self, self.session, fileRef)
        self.skinName = "MoviePlayer"
        standardMoviePlayer.skinName = "MoviePlayer"


class IPTVMiniMoviePlayer(customMoviePlayer):
    def __init__(self, session, IplaFile, IplaFileName):
        self.session = session
        self.WithoutStopClose = True
        fileRef = eServiceReference(4097,0,IplaFile)
        fileRef.setName (IplaFileName)
        customMoviePlayer.__init__(self, self.session, fileRef)
#####################################################