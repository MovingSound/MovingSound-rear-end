import csv
import os
import librosa
import numpy as np

import librosa
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from keras.utils import np_utils
from math import sqrt
from functools import reduce
import csv
filename = os.listdir("./Chorus/")
data_set = []
for file in filename:
    # Songname="./Song/"+file
    Songname = "./Chorus/" + file.split(".")[0] + ".wav"
    y, sr = librosa.load(Songname, mono=True)
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    rmse = librosa.feature.rms(y=y)
    spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    to_append = f'{np.mean(chroma_stft)} {np.mean(rmse)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'
    # print(len(to_append))
    for e in mfcc:
        to_append += f' {np.mean(e)}'
    data_set.append([float(i) for i in to_append.split(" ")])
scaler = StandardScaler()
X = scaler.fit_transform(np.array(data_set, dtype=float))


csvFile = open(r"./csv/csvData.csv", "w",newline='',encoding='utf-8')            #创建csv文件
writer = csv.writer(csvFile)                  #创建写的对象
#先写入columns_name
writer.writerow(["song_no","song_name","song_label","song_feature"])     #写入列的名称
#写入多行用writerows
##写入多行
filelist=os.listdir("./Chorus/")
song_no=0
for file in filelist:
    song_no+=1
    print(song_no)
    song_name=file.split('_')[0]
    print(song_name)
    yy ,sr = librosa.load("./Chorus/"+file)
    onset_env = librosa.onset.onset_strength(yy, sr=sr, hop_length=512, aggregate=np.median)
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)#onset_envelope=onset_env
    song_label=tempo
    print(song_label)
    Xx=list(X[song_no-1])
    lis=[]
    lis.append(song_no)
    lis.append(song_name)
    lis.append(song_label)
    lis.append(Xx)
    print(lis)
    writer.writerows([lis])


csvFile.close()