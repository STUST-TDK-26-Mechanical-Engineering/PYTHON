# 底盤運動控制
## 使用說明
```py
control(self,portx,bps)
```   
* portx:串口序列端口號，請使用字串輸入
* bps:串口通訊速度，請輸入正整數，麥輪控制器預設115200
```py
control.play(self,X=0,Y=0,Z=0,s=1)
```   
* X:正負數控制前進後退
    接受整數輸入，數值為馬達本體的目標RPM 
* Y:橫向移動速度控制，其餘同上
* Z:旋轉運動
* 當兩種以上參數都有數值會實現斜向運動，或轉彎等