import librosa
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from keras.utils import np_utils
from math import sqrt
from functools import reduce
import csv
import pygame
import time

filename = os.listdir("./Chorus/")
# data_set = []
# for file in filename:
#     # Songname="./Song/"+file
#     Songname = "./Chorus/" + file.split(".")[0] + ".wav"
#     y, sr = librosa.load(Songname, mono=True)
#     chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
#     rmse = librosa.feature.rms(y=y)
#     spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
#     spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
#     rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
#     zcr = librosa.feature.zero_crossing_rate(y)
#     mfcc = librosa.feature.mfcc(y=y, sr=sr)
#     to_append = f'{np.mean(chroma_stft)} {np.mean(rmse)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'
#     # print(len(to_append))
#     for e in mfcc:
#         to_append += f' {np.mean(e)}'
#     data_set.append([float(i) for i in to_append.split(" ")])
# scaler = StandardScaler()
# X = scaler.fit_transform(np.array(data_set, dtype=float))
# print(X)


song_name = input("输入歌曲名：")
name_id_dic = {}
name_bpm_dic = {}
name_feature_dic = {}
csv_reader = csv.reader(open('./csv/csvData.csv', encoding='utf-8'))
for row in csv_reader:
    name_bpm_dic[row[1]] = row[2]
    name_id_dic[row[1]] = row[0]
    if row[3] != "song_feature":
        featureList = row[3]
        featureList = eval(featureList)
        name_feature_dic[row[1]] = featureList
# song_bpm = name_bpm_dic[song_name]
# target_name_feature_dic = {}
# target_name_id_dic = {}
# for key in name_feature_dic.keys():
#     if abs(float(name_bpm_dic[key]) - float(song_bpm)) < 10:
#         target_name_feature_dic[key] = name_feature_dic[key]
#         target_name_id_dic[key] = name_id_dic[key]
result = []
z = int(name_id_dic[song_name]) - 1
for j in filename:
    sum_ = 0
    j = j.split("_")[0]
    if (song_name == j):
        result.append(-99)
        continue
    else:
        for i in range(0, 26):
            sum_ += name_feature_dic[j][i] * name_feature_dic[song_name][i]
        A = sqrt(reduce(lambda x, y: x + y, map(lambda x: x * x, name_feature_dic[song_name])))
        B = sqrt(reduce(lambda x, y: x + y, map(lambda x: x * x, name_feature_dic[j])))
        answer = sum_ / (A * B)
        result.append(answer)
print(song_name + ":" + filename[result.index(max(result))].split(".")[0].split("_")[0] + ":%f" % (max(result)))
print(filename[result.index(max(result))].split(".")[0].split("_")[0])

pygame.mixer.init()
print("Now Playing " + filename[result.index(max(result))].split(".")[0].split("_")[0])
pygame.mixer.music.load("./SongWav/" + filename[result.index(max(result))].split(".")[0].split("_")[0] + ".wav")
pygame.mixer.music.play(start=0.0)
time.sleep(300)
pygame.mixer.music.stop()
