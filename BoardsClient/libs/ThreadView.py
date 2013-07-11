from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.config import config
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
#from Components.Sources.StaticText import StaticText
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from Plugins.Extensions.BoardsClient.libs.vbulletin import GetWebPage, GetDVHKforumContent, GetForumsList, GetThreadsList, GetFullThread as vb_GetFullThread

class ThreadView(Screen):
    def __init__(self, session,  WebPage , MainURL, ThreadURL ):
        self.session = session
        Screen.__init__(self, session)

        self["text"] = ScrollLabel("")
        #nasze ustawienia
        self.username = config.plugins.BoardReader.dvhk_login.value
        self.password = config.plugins.BoardReader.dvhk_password.value
        self.mainurl = MainURL
        self.ThreadURL = ThreadURL 
        self.ThreadPage = '&page='
        self.Plugin_PATH = resolveFilename(SCOPE_PLUGINS, 'Extensions/BoardsClient/')
        self.WebPage = WebPage[WebPage.find('\n')+1:]
        self.newtitle = WebPage[:WebPage.find('\n')]
        #print self.ThreadURL
        self.CurrentThreadPage = 1
        self.MaxThreadPage = 1
        self.MultiThreadPages = False
        if self.newtitle.find('Strona ') > 0 :
            tmpPage = self.newtitle[self.newtitle.find('Strona ') + len('Strona '):]
            tmpPage = tmpPage[:tmpPage.find(' ')].strip()
            if tmpPage.isdigit(): 
                self.MultiThreadPages = True
                self.CurrentThreadPage = int(tmpPage)
                self.MaxThreadPage = self.CurrentThreadPage
                #print "Aktualna strona: " + tmpPage
        
        if self.MultiThreadPages == False:
            skin = """
                <screen position="50,70" size="1180,600" title="ThreadView..." >
                    <widget name="text" position="0,0" size="1180,600" font="Console;24" />
                </screen>"""
            self.skin = skin
        
            self["actions"] = ActionMap(["WizardActions", "DirectionActions", "ColorActions"], 
            {
                "ok": self.cancel,
                "back": self.cancel,
                "left": self["text"].pageUp,
                "right": self["text"].pageDown,
                "up": self["text"].pageUp,
                "down": self["text"].pageDown
            }, -1)
        else:
            skin = """
                <screen position="50,70" size="1180,600" title="ThreadView..." >
                <ePixmap position="5,5" zPosition="4" size="30,30" pixmap="%s/icons/red.png" transparent="1" alphatest="on" />
                <ePixmap position="180,5" zPosition="4" size="30,30" pixmap="%s/icons/green.png" transparent="1" alphatest="on" />
                <ePixmap position="365,5" zPosition="4" size="30,30" pixmap="%s/icons/yellow.png" transparent="1" alphatest="on" />
                <ePixmap position="545,5" zPosition="4" size="30,30" pixmap="%s/icons/blue.png" transparent="1" alphatest="on" />
                <widget name="key_red" position="40,5" size="140,27" zPosition="5" valign="center" halign="left" backgroundColor="black" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
                <widget name="key_green" position="220,5" size="180,27" zPosition="5" valign="center" halign="left" backgroundColor="black" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
                <widget name="key_yellow" position="400,5" size="300,27" zPosition="5" valign="center" halign="left" backgroundColor="black" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
                <widget name="key_blue" position="580,5" size="140,27" zPosition="5" valign="center" halign="left" backgroundColor="black" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
                <widget name="text" position="0,40" size="1180,560" font="Console;24" />
                </screen>""" % (self.Plugin_PATH,self.Plugin_PATH,self.Plugin_PATH,self.Plugin_PATH)
            self.skin = skin
            self["key_red"] = Label("First page")
            self["key_green"] = Label("Previous page")
            self["key_yellow"] = Label("Current page")
            self["key_blue"] = Label("Current page")

            self["actions"] = ActionMap(["WizardActions", "DirectionActions", "ColorActions"], 
            {
                "ok": self.cancel,
                "back": self.cancel,
                "left": self["text"].pageUp,
                "right": self["text"].pageDown,
                "up": self["text"].pageUp,
                "down": self["text"].pageDown,
                "red": self.red_pressed,
                "green": self.green_pressed,
                "yellow": self.yellow_pressed,
                "blue": self.blue_pressed,
            }, -1)
          
        self.session.nav.event.append(self.__event)
        self.onShown.append(self.updateTitle)
        
        self.onLayoutFinish.append(self.startRun) # dont start before gui is finished

    def updateTitle(self):
        self.setTitle(self.newtitle)

    def startRun(self):
        self["text"].setText(self.WebPage)

    def cancel(self):
        self.close()

    def __event(self, ev):
        pass

    def SetLabels(self):
        if self.CurrentThreadPage == 1 :
            self["key_red"].setText("Current page")
            self["key_green"].setText("Current page")
            self["key_yellow"].setText("Next page")
            self["key_blue"].setText("Last page")
        elif self.CurrentThreadPage > 1 and self.CurrentThreadPage < self.MaxThreadPage :
            self["key_red"].setText("First page")
            self["key_green"].setText("Previous page")
            self["key_yellow"].setText("Next page")
            self["key_blue"].setText("Last page")
        elif self.CurrentThreadPage == self.MaxThreadPage :
            self["key_red"].setText("First page")
            self["key_green"].setText("Previous page")
            self["key_yellow"].setText("Current page")
            self["key_blue"].setText("Current page")
        return  

    def red_pressed(self):
        if self.CurrentThreadPage != 1:
            self.CurrentThreadPage = 1
            self.GetOtherThreadPage()
            self.SetLabels()
        return

    def green_pressed(self):
        if self.CurrentThreadPage > 1:
            self.CurrentThreadPage = self.CurrentThreadPage - 1
            self.GetOtherThreadPage()
            self.SetLabels()
        return

    def yellow_pressed(self):
        if self.CurrentThreadPage < self.MaxThreadPage:
            self.CurrentThreadPage = self.CurrentThreadPage + 1
            self.GetOtherThreadPage()
            self.SetLabels()
        return
 
    def blue_pressed(self):
        if self.CurrentThreadPage != self.MaxThreadPage:
            self.CurrentThreadPage = self.MaxThreadPage
            self.GetOtherThreadPage()
            self.SetLabels()
        return

    def GetOtherThreadPage(self):
        try:
            self.WebPage = vb_GetFullThread(GetWebPage(self.mainurl,self.ThreadURL + self.ThreadPage + str(self.CurrentThreadPage),self.username,self.password))
        except:
            pass
        self.newtitle = self.WebPage[:self.WebPage.find('\n')]
        self.WebPage = self.WebPage[self.WebPage.find('\n')+1:]
        self["text"].setText(self.WebPage)
        self.setTitle(self.newtitle)
        return