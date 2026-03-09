from network import *
from graph import *
from answers import *

import sys 
from pathlib import Path

# Load the network

ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))
NET_DIR = ROOT / "examples"

network_file = "/home/onyxia/work/Emmanuelle-Chocron---Samuel-Placek/examples/small.txt"
network = Network.from_file(NET_DIR / "small.txt")

MODE = input("Que voulez vous lancer ? Appel de toutes les fonction (ALL) ou d'une fonctiion en particulier (P)")

if MODE == "ALL":
    



