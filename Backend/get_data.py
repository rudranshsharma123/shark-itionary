import os
cur_dir = os.path.dirname(os.path.abspath(__file__))
print(cur_dir )
img_dir = os.path.join(cur_dir, "./data/sharks")
print(img_dir)
data = {"name":[], "captions":[]}
def rename(dirName, name):
    for count, filename in enumerate(os.listdir(dirName)):
        # print(dirName)
        dst =dirName + str(count) + ".jpg"
        src =os.path.join(dirName,f'{filename}')
        os.rename(src, dst)
        data['name'].append(name+str(count) + '.jpg')

        data['captions'].append(name)
for count, filename in enumerate(os.listdir(img_dir)):
    rename(os.path.join(img_dir, filename), filename)
    
import pandas as pd
df = pd.DataFrame(data= data)
df.to_csv('1.csv')