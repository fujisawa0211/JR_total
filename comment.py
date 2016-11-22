#!/usr/local/bin/python2
#coding: utf-8

import csv
import sys
import numpy as np
import subprocess


def import_csv(filename):
    data = [v for v in csv.reader(open(filename, 'rb')) if len(v) != 0]
    return data

def write_csv(write_arr, filename):
    f = open(filename, 'ab')
    csvWriter = csv.writer(f)
    for line in write_arr:
        csvWriter.writerow(line)
    f.close()

def import_txt(filename):
    f = open(filename)
    lines = f.readlines() # 1行ごとに全部読み込んでる
    f.close()
    return lines

def write_txt(write_arr, filename):
    f = open(filename, 'w')
    for line in write_arr:
        f.write(line)
    f.close()


if __name__ == "__main__":
    #読み込みファイルの指定
    files = []
    counter = 0

    arr5 = []

    for i_file in files:
        counter += 1
        r_data = import_csv("com/"+i_file)

        grp_n = i_file[0:1]

        a2 = []
        a2.append("\documentclass[a4paper,11pt]{jarticle}")
        a2.append("\n")
        a2.append("\usepackage{ascmac}")
        a2.append("\n")
        a2.append("\usepackage[top=20truemm,bottom=20truemm,left=20truemm,right=20truemm]{geometry}")
        a2.append("\\begin{document}")
        a2.append("\n")
        a2.append("\section*{"+grp_n+"班}")
        a2.append("\n")

        cnt2 = 0
        for i in r_data:
            if i[0] == "Answer2":
                if cnt2 != 0 and i[1] != "未解答":
                    a2.append("\n")
                    a2.append("\\begin{screen}")
                    a2.append("\n")
                    a2.append(i[1])
                    a2.append("\n")
                    a2.append("\end{screen}")
                    a2.append("\n")
                cnt2 += 1
        a2.append("\end{document}")
        write_txt(a2, "out/"+grp_n+".tex")


        cntid = 0
        idarr = []
        allarr = []
        for i in r_data:
            if i[0] == "ID":
                cntid += 1
                idarr.append(i[1])
            if i[0] == "Answer1":
                if cntid != 0:
                    idarr.append(i[1])
                    idarr.append(i_file[0])
                    allarr.append(idarr)
                    idarr = []
        arr5.extend(allarr)


    points = {}
    for i in arr5:
        if not points.has_key(i[0]):
            points[i[0]] = {}
        if i[1] != "未解答":
            points[i[0]][i[2]] = [-1 * (int(item) - 6) for item in i[1].split(",")]

    points2 = {}
    for i in points:
        points2[i] = {}
        points2[i]["dat"] = []
        for j in points[i]:
            points2[i]["dat"].extend(points[i])

    for i in points2:
        points2[i]["dat"] = [ int(item) for item in points2[i]["dat"]]
        points2[i]["mean"] = float(np.mean(points2[i]["dat"]))
        points2[i]["std"] = float(np.std(points2[i]["dat"]))


    npoints = {}
    for i in points:
        npoints[i] = {}
        for j in points[i]:
            npoints[i][j] = []
            for k in points[i][j]:
                npoints[i][j].append( float(points[i][j][k]-points2[i]["mean"])/points2[i]["std"] + 5)

#==============================================================================
#TeXコンパイル
    for i_file in files:
        grp_n = i_file[0:1]
        cmd = "platex ./out/%s.tex ; dvipdfmx %s.dvi" % (grp_n, grp_n)
        subprocess.call(cmd, shell=True)

#==============================================================================
#重み付け
    PROF = []
    TA = []
#==============================================================================

#Scoreの出力
    print "===SCORE======================="

    dpoints = {}
    for i in npoints:
        for j in npoints[i]:
            if not dpoints.has_key(j):
                dpoints[j] = 0
            if int(i) in PROF:
                dpoints[j] += 3 * sum(npoints[i][j])
            elif int(i) in TA:
                dpoints[j] += 2 * sum(npoints[i][j])
            else:
                dpoints[j] +=     sum(npoints[i][j])

    dpoints_sr = sorted(dpoints.items(), key=lambda x:x[1], reverse=True)
    cnt = 0
    for i in dpoints_sr:
        cnt += 1
        print str(cnt) + "位", str(i[0]) + "班" , i[1]
    print "==============================="
    cnt = 0
    for i in dpoints_sr:
        cnt += 1
        print str(cnt) + "位", str(i[0]) + "班"

    write_csv(points,"points.csv")


