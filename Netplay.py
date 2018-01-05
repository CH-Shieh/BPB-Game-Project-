from tkinter import *
import tkinter.messagebox as tkMessageBox
import tkinter.ttk as ttk

from socket import *
import time
import threading

HOST_PORT = 7777
UDP_PORT = 5000

WAIT_TIME = 5.0
LOCAL_IP = gethostbyname(gethostname())
LOCAL_IP_A = LOCAL_IP.split('.')

class Netplay:

    UDP_Scan_Time = 0.0
    Target_IP = ""
    server = socket(AF_INET, SOCK_STREAM)
    
    Buffer_Ball_Data = []
    Buffer_Ball_Data_Update = False
    Buffer_Current_Ball = []
    Buffer_DAMAGE = 0
    Buffer_Score = 0
    Buffer_KO = 0
    Buffer_Combo = 0
    alive = False
    TCP_Connected = False
    TCP_socket = 0
    
    def refresh():
        global socket_udp_rx

        Netplay.tree.delete(*Netplay.tree.get_children())
        Netplay.text_refresh.config(text = "Refreshing ...")
        Netplay.UDP_Scan_Time = time.time()
        Netplay.room_request()
            
    def send():
        socket_udp_tx = socket(AF_INET, SOCK_DGRAM)
        if (not Netplay.USERNAME.get() == ""):
            brocast = LOCAL_IP_A[0] + "." + LOCAL_IP_A[1] + "." + LOCAL_IP_A[2] + ".255"
            socket_udp_tx.sendto(bytes("BPB,/ROOMDATA,/"+Netplay.USERNAME.get()+",/P", "utf-8"), (brocast, UDP_PORT))
        else:
            tkMessageBox.showerror( "Notice", "請輸入名稱")

    def send2():
        global socket_tcp_rx
        socket_tcp_rx.send(b'BPB,/Testing!')
            
    def add():
        global socket_tcp_rx, server_handler
        print("selected items:")
        for item in Netplay.tree.selection():
            item_text = Netplay.tree.item(item,"values")
            Netplay.Target_IP = item_text[1]
            print(item_text[1])

            if (item_text[2][0] == 'P'):
                tkMessageBox.showerror( "Notice", "該房間遊玩中！")
                return
            
        address = (Netplay.Target_IP, HOST_PORT)
        socket_tcp_rx = socket(AF_INET, SOCK_STREAM)  
        try:
            socket_tcp_rx.connect(address)
            socket_tcp_rx.settimeout(10)
            Netplay.alive = False
            Netplay.TCP_Connected = True
            server_handler = threading.Thread(target=Netplay.TCP_Client_Thread)
            server_handler.start()
            Netplay.root.destroy()

        except:
            print("[TCP] 連線失敗！")

        
    def on_closing():
        if tkMessageBox.askokcancel("Notice", "結束多人連線?"):
            Netplay.TCP_socket = None
            Netplay.alive = False
            Netplay.TCP_Connected = False
            Netplay.root.destroy()
    def TCP_Server_Start():
        Netplay.server = socket(AF_INET, SOCK_STREAM)
        Netplay.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        Netplay.server.bind(('', HOST_PORT))
            
        Netplay.server.listen(1)
        
        Netplay.TCP_Connected = True
        print("在Port %d 建立了TCP Server." % HOST_PORT)
        
    
    def handle_client(client_socket):
        Netplay.TCP_socket = client_socket
        
        client_socket.settimeout(10)
        while True:
            if (Netplay.TCP_Connected == False):
                break
            try:
                data = client_socket.recv(1024)
                Netplay.packet_handle(data)

            except Exception as e:
                print("例外情況發生：")
                print(e)
                print ("[TCP] [Server] 連線發生錯誤, 結束連線.")
                client_socket.close()
                Netplay.TCP_Connected = False
                
    def TCP_Client_Thread():
        global socket_tcp_rx
        Netplay.TCP_socket = socket_tcp_rx
        while True:
            if (Netplay.TCP_Connected == False):
                break
            try:
                data = socket_tcp_rx.recv(1024)
                Netplay.packet_handle(data)

            except Exception as e:
                print("例外情況發生：")
                print(e)
                print("[TCP] [Client] 連線發生錯誤, 結束連線.")
                socket_tcp_rx.close()
                Netplay.TCP_Connected = False

                
    def packet_handle(data):
        str_data = data.decode('utf-8')
    
        try:
            if (str_data.startswith("BPB,/")):
                packet_data = str_data.split("\n")
                
                for i in packet_data:
                    game_data = i.split(',/')
                    if (len(game_data) < 3):
                        continue
                    
                    if (game_data[1] == "BallData"):
                        Ball_Data_String = game_data[2].split('=/')
                        all_intdata = []
                        for k in Ball_Data_String:
                            if (k == ''):
                                continue
                            intdata = []
                            rr = k.split(',')
                            for a in rr:
                                intdata.append(int(a))

                            all_intdata.append(intdata)

                        Netplay.Buffer_Ball_Data = all_intdata    
                    elif (game_data[1] == "CurrentBall"):
                        Ball_Data_String = game_data[2].split(',')
                        all_intdata = []

                        for k in Ball_Data_String:
                            if (k == ''):
                                continue
                            all_intdata.append(int(k))

                        Netplay.Buffer_Current_Ball = all_intdata
                        
                    elif (game_data[1] == "DAMAGE"):
                        if (not game_data[2] == ''):
                            Netplay.Buffer_DAMAGE = int(game_data[2])
                    elif (game_data[1] == "KO"):
                        if (not game_data[2] == ''):
                            Netplay.Buffer_KO = int(game_data[2])
                    elif (game_data[1] == "SCORE"):
                        if (not game_data[2] == ''):
                            Netplay.Buffer_Score = int(game_data[2])
                    elif (game_data[1] == "COMBO"):
                        if (not game_data[2] == ''):
                            Netplay.Buffer_Combo = int(game_data[2])
                            
        except Exception as e:
            print("例外情況發生：")
            print(e)
            
        #Netplay.Buffer_Ball_Data_Update = True
            

    def flush(self):
        Netplay.Buffer_Ball_Data_Update = False
        Netplay.Buffer_DAMAGE = 0

    def room_request():
        brocast = LOCAL_IP_A[0] + "." + LOCAL_IP_A[1] + "." + LOCAL_IP_A[2] + ".255"
        socket_udp_tx = socket(AF_INET, SOCK_DGRAM)
        socket_udp_tx.sendto(bytes("BPB,/ROOMQUEST", "utf-8"), (brocast, UDP_PORT))
    def TCP_Server_Thread():
        try:
            client, addr = Netplay.server.accept()
            print ("[*] Acepted connection from: %s:%d" % (addr[0],addr[1]))

            Netplay.alive = False
            Netplay.TCP_Connected = True
            client_handler = threading.Thread(target=Netplay.handle_client, args=(client,))
            client_handler.start()
            Netplay.root.destroy()
        except Exception as e:
            print("[Server] 接受連線過程中發生錯誤：")
            print(e)
    def UDP_Start():
        global socket_udp_rx
        Netplay.UDP_Scan_Time = time.time()
        print("Starting RX socket: UDP...")
        socket_udp_rx = socket(AF_INET, SOCK_DGRAM)
        print("UDP server bind")
        socket_udp_rx.bind(('',UDP_PORT))

    def UDP_Thread():
        global socket_udp_rx, socket_udp_tx
        while True:
            try:
                if (Netplay.alive == False and Netplay.TCP_Connected == False):
                    break
                socket_udp_rx.settimeout(1)
                data, (src_addr, src_port) = socket_udp_rx.recvfrom(512)
                    
                if len(data)>0:
                    if (Netplay.UDP_Scan_Time + WAIT_TIME > time.time()):
                        print("自 %s 收到了原始資料: %s" %(src_addr, data.decode('utf-8')))

                        str_data = data.decode('utf-8')
                        if (str_data.startswith("BPB,/")):
                            game_data = str_data.split(',/')
                            if (game_data[1] == "ROOMDATA"):
                                if (game_data[3] == "P"):
                                    game_data[3] = "Playing"
                                elif (game_data[3] == "W"):
                                    game_data[3] = "Waiting"
                                else:
                                    game_data[3] = "Unknown"
                                Netplay.tree.insert('', 'end', values=(game_data[2], src_addr, game_data[3]))

                            elif (game_data[1] == "ROOMQUEST"):
                                
                                if (Netplay.TCP_Connected and Netplay.Target_IP == ""):
                                    brocast = LOCAL_IP_A[0] + "." + LOCAL_IP_A[1] + "." + LOCAL_IP_A[2] + ".255"
                                    socket_udp_tx = socket(AF_INET, SOCK_DGRAM)
                                    if (Netplay.alive == False):
                                        socket_udp_tx.sendto(bytes("BPB,/ROOMDATA,/"+str(LOCAL_IP)+",/P", "utf-8"), (brocast, UDP_PORT))
                                    else:
                                        socket_udp_tx.sendto(bytes("BPB,/ROOMDATA,/"+str(LOCAL_IP)+",/W", "utf-8"), (brocast, UDP_PORT))
                    #else: 搜尋時間以外收到的封包 通通丟掉^O^
            except:
                if (Netplay.alive == True):
                    if (Netplay.UDP_Scan_Time + WAIT_TIME < time.time()):
                        if (len(Netplay.tree.get_children()) > 0):
                            Netplay.text_refresh.config(text = "搜尋完畢.")
                        else:
                            Netplay.text_refresh.config(text = "找不到任何伺服器.")
                    else:
                        Netplay.text_refresh.config(text = "Refreshing ...")
    def create():
        Netplay.TCP_Server_Start()
        Netplay.Tthread = threading.Thread(target = Netplay.TCP_Server_Thread)
        Netplay.Tthread.start()

    def UDP_send(data):
        global socket_udp_tx
        brocast = LOCAL_IP_A[0] + "." + LOCAL_IP_A[1] + "." + LOCAL_IP_A[2] + ".255"
        socket_udp_tx = socket(AF_INET, SOCK_DGRAM)
        socket_udp_tx.sendto(bytes(data, "utf-8"), (brocast, UDP_PORT))

    def show(self = 0):
        Netplay.alive = True
        Netplay.Target_IP = ""
        print("Netplay opened")
        root = Tk()
        root.title("Netplay UI")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        width = 500
        height = 400
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        root.geometry('%dx%d+%d+%d' % (width, height, x, y))
        root.resizable(0, 0)
        
        Right = Frame(root)
        Right.pack(fill=BOTH)
        scrollbary = Scrollbar(Right, orient=VERTICAL)
        scrollbarx = Scrollbar(Right, orient=HORIZONTAL)
        Netplay.tree = ttk.Treeview(Right, columns=("RoomName", "IP", "Playing"), selectmode="extended", height=15, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=Netplay.tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=Netplay.tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        Netplay.tree.heading('RoomName', text="房間名", anchor=W)
        Netplay.tree.heading('IP', text="IP", anchor=W)
        Netplay.tree.heading('Playing', text="遊玩中", anchor=W)

        Netplay.tree.column('#0', stretch=NO, minwidth=0, width=0)
        Netplay.tree.column('#1', stretch=NO, minwidth=0, width=240)
        Netplay.tree.column('#2', stretch=NO, minwidth=0, width=160)
        Netplay.tree.column('#3', stretch=NO, minwidth=0, width=60)
        Netplay.tree.pack(fill=BOTH)
        Netplay.text_refresh = Label(text="Refreshing ...")
        Netplay.text_refresh.pack(side=LEFT)
        #btn_send = Button(text="傳送", command = Netplay.send).pack(side=RIGHT)
        #btn_send2 = Button(text="傳送TCP", command = Netplay.send2).pack(side=RIGHT) 
        btn_refresh = Button(text="重新整理", command = Netplay.refresh).pack(side=RIGHT)

        btn_create = Button(text="新建遊戲", command = Netplay.create).pack(side=RIGHT)
        btn_join = Button(text="加入遊戲", command = Netplay.add).pack(side=RIGHT)

        Netplay.USERNAME = StringVar()


        
        username = Entry(root, textvariable=Netplay.USERNAME, width=30)
        username.pack(side=RIGHT)
        
        root.protocol("WM_DELETE_WINDOW", Netplay.on_closing)


        Netplay.UDP_Start()
        
        Netplay.Uthread = threading.Thread(target = Netplay.UDP_Thread, args = (), name = "UDP_Thread")
        Netplay.Uthread.start()

        Netplay.room_request()
        Netplay.root = root
        root.mainloop()
        print("Netplay closed")
#Netplay.show()
