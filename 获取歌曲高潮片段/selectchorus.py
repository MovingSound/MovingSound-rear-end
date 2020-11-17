import os
import sys
from pychorus import find_and_output_chorus
class mxc:
    def mxccccccc(self):
        filelist=os.listdir("./SongWav/")
        self.time=[30,15,10,5]
        for file in filelist:
            self.count = 0
            chorus_start_sec= find_and_output_chorus("./SongWav/"+file,"./Chorus/"+file.split(".")[0]+"_high.wav", 60)
            while chorus_start_sec ==None:
                chorus_start_sec = find_and_output_chorus("./SongWav/"+file,"./Chorus/"+file.split(".")[0]+"_high.wav", self.time[self.count])
                self.count += 1
                if self.count > 3:
                    break
