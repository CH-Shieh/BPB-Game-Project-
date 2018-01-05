import os

Config_FileName = "config.ini"
class System_GameConfig:
    CurrentName = "NoName"
    ScreenShot = 1
    def __init__(self):
        
        if (os.path.exists(Config_FileName)):
            if (os.path.isfile(Config_FileName)):
                #Load File here
                #print("Load File")
                try:
                    f = open(Config_FileName, 'r')

                    for line in f:
                        token, data = line.split(" = ")
                        data = data.replace("\n", "")
                        if (token == "Name"):
                            self.CurrentName = data
                            #print("Loaded Name %s" % data)
                        elif (token == "ScreenShot"):
                            self.ScreenShot = int(data)
                    f.close()
                except:
                    print("檔案錯誤, 重新建立.")
                    self.load_default()
                    
            else:
                raise(IOError('請把config.ini 資料夾刪除.'))
        else:
            self.load_default()
    def load_default(self):
        f = open(Config_FileName, 'w')
        f.write("Name = NoName")
        f.write("ScreenShot = 1")
        f.close()
        
    def write(self):
        f = open(Config_FileName, 'w')
        f.write("Name = %s\n" % self.CurrentName)
        f.write("ScreenShot = %d\n" % self.ScreenShot)
        f.close()
