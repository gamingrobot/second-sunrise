from Menu import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *


class ConsoleMenu(Menu):
    def __init__(self, root, prevmenu):
        Menu.__init__(self, root, prevmenu)

        self.playButton = self.addButton(
            text = ("Back"),
            pos=(1.2, -0.9),
            command=self.goBackMenu
            )

        self.chatFrame = DirectFrame(pos=(.2,0,-0.5))
        self.chatFrame.reparentTo(self.mainFrame)
        self.loadChat()

    def loadChat(self):
        self.chatList = DirectScrolledList(
        incButton_pos= (-0.4,0,-2.4),
        incButton_scale= (4,1,9),
        decButton_pos= (-0.4,0,-0.8),
        decButton_scale= (4,1,9),
        frameColor= (0,1,1,0),
        scale=0.05,
        pos=(-1,0,0.3),
        sortOrder=2,
        numItemsVisible = 4)

        self.chatList.reparentTo(self.chatFrame)
        self.loadChatEntry()
        

    def loadChatEntry(self):
        #like the name sais, its loading a DirectEntry field which serves as chat-input-field 
        #and reparents it to self.chatFrame.
        #executes self.sendChatMessage() if you press enter.
        self.chatEntry = DirectEntry(scale=0.05,
        text_scale=(1,1),
        frameColor=(.5,.5,1,.8),
        pos=(-1,0,0.05),
        command = self.sendChatMessage,
        relief=3,
        borderWidth=(.1,.1),
        width = 30,
        sortOrder=4,
        cursorKeys=1)
        self.chatEntry['focus'] = False
        self.chatEntry.reparentTo(self.chatFrame)

    def sendChatMessage(self,message):
    #if message is not empty.. display it.
        self.chatEntry.destroy()
        self.loadChatEntry()
        self.chatEntry['focus'] = True
        if message != "":
            self.chatEntry.enterText("")
            newText = DirectLabel(
                text=message,
                text_align=TextNode.ALeft,
                text_bg=(0,1,1,0),
                text_fg=(0,0,0,0.8),
                frameColor=(0,0,0,0))
            self.chatList.addItem( newText, True)
            self.chatList.scrollBy(1)
