class a:
    def m(self,name):
        import os
        from math import sqrt
        from functools import reduce
        import csv
        filename = os.listdir(r"/home/Python_NetEaseMusicAPI/SongMp3/")

        song_name = name
        name_id_dic = {}
        name_bpm_dic = {}
        name_feature_dic = {}
        csv_reader = csv.reader(open(r'/home/Python_NetEaseMusicAPI/csvData.csv',encoding='utf8'))
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
            j = j.split(".")[0]
            if (song_name == j):
                result.append(-99)
                continue
            else:
                for i in range(0, 26):
                    try:
                        sum_ += name_feature_dic[j][i] * name_feature_dic[song_name][i]
                    except Exception as err:
                        print(err)
                A = sqrt(reduce(lambda x, y: x + y, map(lambda x: x * x, name_feature_dic[song_name])))
                B = sqrt(reduce(lambda x, y: x + y, map(lambda x: x * x, name_feature_dic[j])))
                answer = sum_ / (A * B)
                result.append(answer)

        name_1=filename[result.index(max(result))].split(".")[0].split("_")[0]
        print(name_1)
        return name_1