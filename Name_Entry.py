from tkinter import *
import tkinter.messagebox as tkMessageBox
import tkinter.ttk as ttk

class Name_Entry:

    def __init__(self, name = "NoName"):
        ####視窗建立
        self.root = Tk()
        self.root.title("變更玩家名")

        ####變數
        self.CurrentName = name
        self.NewName = StringVar()
        self.NewName.set(name)

        ####控制項
        label1 = Label(self.root,text="請輸入玩家名字：")
        label1.pack()
        
        ent_username = Entry(self.root, textvariable=self.NewName, width=20)
        ent_username.pack()

        button1 = Button(self.root,text="確定", command = self.SetName).pack()

        self.root.mainloop()
        
    def SetName(self):
        if (self.NewName.get() == ""):
            tkMessageBox.showerror( "Notice", "請輸入名稱")
            return
        self.CurrentName = self.NewName.get()
        self.root.destroy()
