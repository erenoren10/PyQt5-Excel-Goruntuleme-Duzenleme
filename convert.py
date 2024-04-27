from PyQt5 import uic


with open("siparisler.py","w",encoding="utf-8") as fout:
    uic.compileUi("untitled.ui",fout)