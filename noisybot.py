import os, subprocess, socket

hnbPATH = os.path.dirname(os.path.realpath(__file__))

hnbHOST = "irc.twitch.tv"
hnbPORT = 6667

hnbCHAN = "xxxxxxxx"
hnbNICK = "xxxxxxxx"
hnbPASS = "oauth:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
hnbCHAR = "!"

hnbDATA = hnbPATH + "/noisybot.txt"
hnbADIR = hnbPATH + "/sfx/"
hnbAEXT = ".ogg"
hnbACMD = "/usr/bin/play"
hnbAPAR = "-q"

hnbREAD = ""
hnbMODT = False

def _hnbSEND(hnbMESS):
    hnbMESS = "PRIVMSG #" + hnbCHAN + " :" + hnbMESS + "\r\n"
    hnbSOCK.send(hnbMESS.encode("utf-8"))

def _hnbPLAY(hnbFILE):
    subprocess.call([hnbACMD, hnbADIR + hnbFILE + hnbAEXT, hnbAPAR])

hnbSOCK = socket.socket()
hnbSOCK.connect((hnbHOST, hnbPORT))
hnbSOCK.send(("PASS " + hnbPASS + "\r\n").encode("utf-8"))
hnbSOCK.send(("NICK " + hnbNICK + "\r\n").encode("utf-8"))
hnbSOCK.send(("JOIN #" + hnbCHAN + " \r\n").encode("utf-8"))

while True:
    hnbREAD = hnbREAD + hnbSOCK.recv(1024).decode("utf-8")
    hnbTEMP = hnbREAD.split("\n")
    hnbREAD = hnbTEMP.pop()

    for hnbLINE in hnbTEMP:
        if (hnbLINE[0] == "PING"):
            hnbSOCK.send("PONG %s\r\n" % hnbLINE[1])
        else:
            hnbPART = hnbLINE.split(":")

            if "QUIT" not in hnbPART[1] and "JOIN" not in hnbPART[1] and "PART" not in hnbPART[1]:
                try:
                    hnbMESS = hnbPART[2][:len(hnbPART[2]) - 1]
                except:
                    hnbMESS = ""
                hnbNAME = hnbPART[1].split("!")
                hnbUSER = hnbNAME[0]
                
                if hnbMODT and hnbMESS:
                    
                    if hnbMESS[0] == hnbCHAR:
                        hnbAFIL = open(hnbDATA, "r")

                        for hnbALIN in hnbAFIL:
                            hnbBCMD = hnbALIN.split(":")
                            hnbBLEN = len(hnbBCMD[0]) + 1

                            if hnbMESS[:hnbBLEN].lower() == hnbCHAR + hnbBCMD[0]:
                                print(hnbUSER + ": " + hnbMESS)
                                if hnbBCMD[1]:
                                    hnbBCMD[1] = hnbBCMD[1].replace("{sender}", hnbUSER)
                                    hnbBCMD[1] = hnbBCMD[1].replace("{param}", hnbMESS[hnbBLEN:])
                                    _hnbSEND(hnbBCMD[1])
                                if hnbBCMD[2]:
                                    _hnbPLAY(hnbBCMD[2])

                        hnbAFIL.close()

                for hnbPLIN in hnbPART:
                    if "End of /NAMES list" in hnbPLIN:
                        hnbMODT = True
