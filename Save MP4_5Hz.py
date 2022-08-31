# -*- coding: utf-8 -*-

import cv2
import os

Tm = input("\n 請輸入錄影時間(sec) ? ")
Fname = input(" 請輸入檔案名稱 ? ")
##開啟攝像頭
cap = cv2.VideoCapture(0)                    #設定 #0攝影鏡頭

width = 640               #影片寬度 640點
height = 480              #影片高度 480點

##視訊大小設定，獲取幀寬度，獲取幀高度
sz = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

fps = 20
N = int(Tm)*fps + 1
# 輸出格式
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

##open and set props
vout = cv2.VideoWriter()

mp4DIR = "MP4"                              # 影片輸出目錄
if not os.path.exists(mp4DIR):              # 自動建立目錄
    os.makedirs(mp4DIR)

vout.open(mp4DIR+'/'+Fname+'.mp4', fourcc, fps, sz, True)

cnt = 1
while cnt < N:
    _, frame = cap.read()
    ##putText輸出到視訊上，各引數依次是：照片/新增的文字/左上角座標/字型/字型大小/顏色/字型粗細
    cv2.putText(frame, str(cnt), (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1, cv2.LINE_AA)
    vout.write(frame)
    cnt += 1

    cv2.imshow('video', frame)
    if cv2.waitKey(200) & 0xFF == ord("q"):
        break


cv2.destroyAllWindows()
vout.release()
cap.release()
