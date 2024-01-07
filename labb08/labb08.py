import tkinter as tk
import tkinter.scrolledtext as tksctxt
import socket

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.g_bConnected = False
        self.g_sock = None

    def create_widgets(self):
        # GUI components
        self.groupCon = tk.LabelFrame(bd=0)
        self.groupCon.pack(side="top")

        self.ipPortLbl = tk.Label(self.groupCon, text='IP:port', padx=10)
        self.ipPortLbl.pack(side="left")

        self.ipPort = tk.Entry(self.groupCon, width=20)
        self.ipPort.insert(tk.END, 'localhost:60003')
        self.ipPort.bind('<Return>', self.connectHandler)
        self.ipPort.pack(side="left")

        padder = tk.Label(self.groupCon, padx=5)
        padder.pack(side="left")

        self.connectButton = tk.Button(self.groupCon, command=self.connectButtonClick, width=10, text='Connect')
        self.connectButton.pack(side="left")

        padder = tk.Label(self.groupCon, padx=1)
        padder.pack(side="left")

        self.clearButton = tk.Button(self.groupCon, text='Clear Msg', command=self.clearButtonClick)
        self.clearButton.pack(side="left")

        self.msgText = tksctxt.ScrolledText(height=15, width=42, state=tk.DISABLED)
        self.msgText.pack(side="top")

        self.groupSend = tk.LabelFrame(bd=0)
        self.groupSend.pack(side="top")

        self.textInLbl = tk.Label(self.groupSend, text='Message', padx=10)
        self.textInLbl.pack(side="left")

        self.textIn = tk.Entry(self.groupSend, width=38)
        self.textIn.bind('<Return>', self.sendMessage)
        self.textIn.pack(side="left")

        padder = tk.Label(self.groupSend, padx=5)
        padder.pack(side="left")

        self.sendButton = tk.Button(self.groupSend, text='Send', command=self.sendButtonClick)
        self.sendButton.pack(side="left")

        self.ipPort.focus_set()

    def clearButtonClick(self):
        self.msgText.configure(state=tk.NORMAL)
        self.msgText.delete(1.0, tk.END)
        self.msgText.see(tk.END)
        self.msgText.configure(state=tk.DISABLED)

    def connectButtonClick(self):
        if self.g_bConnected:
            self.disconnect()
        else:
            self.tryToConnect()

    def sendButtonClick(self):
        self.sendMessage()

    def disconnect(self):
        if self.g_bConnected:
            if self.g_sock:
                self.g_sock.close()
            self.g_bConnected = False
            self.connectButton['text'] = 'Connect'
            self.printToMessages('Disconnected')

    def tryToConnect(self):
        if not self.g_bConnected:
            ip_port = self.ipPort.get()
            ip, port = ip_port.split(':')
            try:
                self.g_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.g_sock.settimeout(0.1)
                self.g_sock.connect((ip, int(port)))
                self.g_bConnected = True
                self.connectButton['text'] = 'Disconnect'
                self.printToMessages('Connected to ' + self.myAddrFormat(self.g_sock.getpeername()))
            except socket.error as e:
                self.printToMessages('Could not connect to ' + ip_port)
                if self.g_sock:
                    self.g_sock.close()
                self.g_sock = None
                self.g_bConnected = False

    def sendMessage(self):
        if self.g_bConnected:
            message = self.textIn.get()
            if message:
                self.textIn.delete(0, tk.END)
                try:
                    self.g_sock.sendall(message.encode('utf-8'))
                    #self.printToMessages('You: ' + message)
                except socket.error as e:
                    self.printToMessages('Message not sent')
                    self.disconnect()

    def pollMessages(self):
        if self.g_sock:
            try:
                self.g_sock.setblocking(False)
                data = self.g_sock.recv(1024)
                if data:
                    self.printToMessages('Server: ' + data.decode('utf-8'))
            except socket.error:
                pass
        self.after(200, self.pollMessages)

    def myAddrFormat(self, addr):
        return '{}:{}'.format(addr[0], addr[1])

    def printToMessages(self, message):
        self.msgText.configure(state=tk.NORMAL)
        self.msgText.insert(tk.END, message + '\n')
        self.msgText.see(tk.END)
        self.msgText.configure(state=tk.DISABLED)

    def connectHandler(self):
        if self.g_bConnected:
            self.disconnect()
        else:
            self.tryToConnect()

def main():
    root = tk.Tk()
    app = Application(master=root)
    app.master.title('Chat Client')
    app.after(200, app.pollMessages)
    app.mainloop()

if __name__ == '__main__':
    main()
