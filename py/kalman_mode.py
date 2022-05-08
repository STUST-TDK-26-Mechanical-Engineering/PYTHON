import matplotlib.pyplot as plt

import numpy as np


#建立噪聲


num = 300


np.random.seed(4)


noise= np.random.randn(num)             #高斯分佈隨機噪聲


noise_std = np.random.randn(num)        #測量噪聲


x = [0]*num


y = [0]*num


#建立資料集


for i in range(1,num):
    x[i] =  np.sin(0.2*i)
    noise_std_ = np.square(np.var(noise_std))  #求方差
    noise_     = np.square(np.var(noise))
    p = [0]* num               #每次的最優偏差
    k = [0]* num               #卡爾曼增益
    s =  x + noise_std        #測量值

for i in range(1,num):
    p[i] =  np.square(p[i-1]) + 0.1*noise_
    k[i] =  0.1*np.sqrt( p[i]/( noise_std_ + p[i]))
    y[i] =  y[i-1] + k[i] * (s[i] - y[i-1])
    p[i] =  np.sqrt((1-k[i])*p[i])


    print(p[i])


plt.plot(x,color = 'r',label = '資料集')


plt.plot(s,color = 'g',label = '資料測量獲取值（帶噪聲）')


plt.plot(y,color = 'b',label = '過濾後的資料')


plt.show()

