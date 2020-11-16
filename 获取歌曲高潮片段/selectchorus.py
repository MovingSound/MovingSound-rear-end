import os
import sys
from pychorus import find_and_output_chorus
class mxc:
    def mxccccccc(self):
        filelist=os.listdir("./SongWav/")
        for file in filelist:
            chorus_start_sec = find_and_output_chorus("./SongWav/"+file,"./Chorus/"+file.split(".")[0]+"_high.wav",15)