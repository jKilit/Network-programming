import firebase_admin
from firebase_admin import db
import tkinter as tk
import tkinter.scrolledtext as tksctxt

cred = firebase_admin.credentials.Certificate('/Users/jonathankilit/Library/CloudStorage/OneDrive-JonkopingUniversity/JTH/Kurser/Nätverks/labb12/labb12-natverk-database.json')
firebase_admin.initialize_app(cred, {'databaseURL':'https://labb12-natverk-default-rtdb.firebaseio.com/'})
ref = firebase_admin.db.reference('/')

DEFAULT_HOST = 'localhost:60003'


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.groupCon = tk.LabelFrame(bd=0)
        self.groupCon.pack(side="top")
        
        self.nameLbl = tk.Label(self.groupCon, text='Name', padx=10)
        self.nameLbl.pack(side="left")
        
        self.name = tk.Entry(self.groupCon, width=20)
        self.name.insert(tk.END, "")

        self.name.pack(side="left")

        padder = tk.Label(self.groupCon, padx=5)
        padder.pack(side="left")

        self.msgText = tksctxt.ScrolledText(height=15, width=42, state=tk.DISABLED)
        self.msgText.pack(side="top")

        self.groupSend = tk.LabelFrame(bd=0)
        self.groupSend.pack(side="top")

        self.textInLbl = tk.Label(self.groupSend, text='message', padx=10)
        self.textInLbl.pack(side="left")

        self.textIn = tk.Entry(self.groupSend, width=38)

        self.textIn.bind('<Return>', sendMessage)
        self.textIn.pack(side="left")

        padder = tk.Label(self.groupSend, padx=5)
        padder.pack(side="left")

        self.sendButton = tk.Button(self.groupSend, text='send', command=sendButtonClick)
        self.sendButton.pack(side="left")


def clearButtonClick():
    g_app.msgText.configure(state=tk.NORMAL)
    g_app.msgText.delete(1.0, tk.END)
    g_app.msgText.see(tk.END)
    g_app.msgText.configure(state=tk.DISABLED)


def sendButtonClick():
    sendMessage(g_app)


def handleMessage(message):
    printToMessages(message["name"]+": "+message["text"])

def streamHandler(incomingData): #lyssnar efter ändringar 
    if incomingData.event_type == 'put':
        if incomingData.path == '/':

            if incomingData.data != None:
                for key in incomingData.data:
                    message = incomingData.data[key]
                    handleMessage(message)
        else:

            message = incomingData.data
            handleMessage(message)
            
def printToMessages(message):
    print(message)
    g_app.msgText.configure(state=tk.NORMAL)
    g_app.msgText.insert(tk.END, message + '\n')
    # scroll to the end, so the new message is visible at the bottom
    g_app.msgText.see(tk.END)
    g_app.msgText.configure(state=tk.DISABLED)
    
def on_closing():
    myQuit()
    
def myQuit():
    g_root.destroy()
    messages_stream.close()
    
def sendMessage(master):
    newMessage = {'name': master.name.get(), 'text': master.textIn.get()}
    ref.child('messages').push(newMessage)

g_root = tk.Tk()
g_app = Application(master=g_root)

messages_stream = ref.child('messages').listen(streamHandler)

g_root.protocol("WM_DELETE_WINDOW", on_closing)


g_app.mainloop()