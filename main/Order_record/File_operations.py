import json 
import time
class log:
    def __init__(self) -> None:
       d = []
       self.data=d
       self.counter=1
    #    with open('./output.json', 'w') as f:
    #     json.dump(self.data, f ,indent = 3)
    def online(self,X=0,Y=0,Z=0,S=0):
        start = time.time()
        with open('./output.json') as f:
            self.data = json.load(f)
        print(type(self.data))
        list1=[self.counter, {'msg':"log.play",'X': X, 'Y': Y, 'Z': Z, 'S': S}]
        self.data.append(list1)
        with open('./text.json', 'w') as f:
            json.dump(self.data, f ,indent = 3)
        self.counter+=1    
        
        end = time.time()

        print("執行時間：%f 秒" % (end - start))
    def read_file(self,id,FILE):
        with open(FILE) as f:
            self.data = json.load(f)
        data=self.data[id-1][1]    
        return data,len(self.data)   

# global a
# a=1

# for s in  range(1000):
#     loop()   
#     if data[s][0]== s+1:
#         print(data[s])  

  