from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.ScrollLabel import ScrollLabel

class ThreadView(Screen):
    skin = """
        <screen position="50,70" size="1180,600" title="ThreadView..." >
            <widget name="text" position="0,0" size="1180,600" font="Console;24" />
        </screen>"""
        
    def __init__(self, session,  WebPage = '?????'):
        self.session = session
        Screen.__init__(self, session)

        self["text"] = ScrollLabel("")
        self["actions"] = ActionMap(["WizardActions", "DirectionActions"], 
        {
            "ok": self.cancel,
            "back": self.cancel,
            "up": self["text"].pageUp,
            "down": self["text"].pageDown
        }, -1)
        
        self.WebPage = WebPage[WebPage.find('\n')+1:]
        self.newtitle = WebPage[:WebPage.find('\n')]
        
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