import numpy as np
import cv2
#import pytesseract
import easyocr
import os
import re
import shutil


#scales of images in μm
scales = [100, 50, 100, 100, 200, 200, 500, 200, 200, 200, 100,
          100, 100, 200, 200, 200, 200, 20, 200, 200, 200, 200,
          200, 200, 200, 200, 50, 200, 1000, 200, 200, 50, 50,
          20, 100, 500, 500, 200, 200, 200, 200, 200, 50, 50,
          50, 200, 500, 500, 20, 50, 50, 500, 200, 200, 200,
          200, 200, 200, 200, 500, 1000, 100, 2000, 1000, 200, 50,
          200, 10, 200, 100, 100, 100, 100, 100, 100, 100, 1000,
          1000, 200, 50, 20, 100, 1000, 500, 500, 200, 200, 200,
          200, 200, 100, 200, 100, 200, 100, 100, 200, 100, 200,
          100, 200, 100, 100, 500, 500, 500, 500, 1000, 50, 200,
          100, 1000, 200, 1000, 20, 20, 10, 10, 50, 200, 500,
          50, 100, 10, 10, 50, 5, 10, 5, 10, 20, 10,
          10, 20, 20, 20, 10, 10, 10, 2, 5, 10, 2,
          5, 10, 200, 200, 100, 100, 100, 10, 10, 50, 100]

#Viewfield size in μm
scale_size = [355, 185, 616, 500, 700, 900, 2770, 1000, 1000, 823, 500,
              500, 510, 900, 900, 900, 823, 100, 1000, 1000, 1000, 1000,
              1000, 1000, 1000, 1000, 277, 1000, 4000, 823, 823, 185, 277,
              79.2, 616, 1850, 1850, 1000, 1000, 924, 823, 1390, 200, 200,
              200, 1390, 2000, 2000, 139, 250, 250, 2500, 1090, 823, 924,
              1000, 924, 823, 823, 2500, 4000, 500, 8000, 6160, 823, 268,
              1110, 62, 823, 500, 500, 500, 500, 500, 500, 555, 5000,
              4500, 700, 185, 92.4, 616, 4500, 1670, 1670, 677, 823, 823,
              823, 823, 500, 900, 500, 900, 500, 500, 900, 500, 900,
              500, 900, 500, 500, 1730, 2000, 2000, 2000, 4000, 277, 1390,
              555, 4030, 1460, 4950, 100, 100, 50, 50.4, 300, 1000, 2000,
              200, 500, 50, 50, 200, 20, 50, 20, 50, 100, 50,
              50, 150, 100, 150, 50, 50, 50, 15, 25, 50, 15,
              30, 50, 950, 950, 572, 400, 400, 40, 40, 277, 555]
              
              
#Coefficents got from GetCoefficents() method
coefficients = [0.3466796875, 0.1806640625, 0.6015625, 0.244140625, 0.341796875, 0.439453125, 2.705078125, 0.48828125, 0.48828125, 0.8037109375, 0.244140625,
                0.244140625, 0.2490234375, 0.439453125, 0.439453125, 0.439453125, 0.8037109375, 0.09765625, 0.9765625, 0.9765625, 0.1220703125, 0.1220703125,
                0.48828125, 0.48828125, 0.390625, 0.48828125, 0.2705078125, 0.48828125, 3.90625, 0.8037109375, 0.8037109375, 0.1806640625, 0.2705078125,
                0.07734375, 0.6015625, 1.806640625, 1.806640625, 0.48828125, 0.48828125, 0.90234375, 0.8037109375, 1.357421875, 0.1953125, 0.1953125,
                0.048828125, 1.357421875, 0.244140625, 0.244140625, 0.1357421875, 0.1220703125, 0.1220703125, 1.220703125, 1.064453125, 0.8037109375, 0.90234375,
                0.48828125, 0.90234375, 0.8037109375, 0.8037109375, 1.220703125, 3.90625, 0.244140625, 3.90625, 6.015625, 0.8037109375, 0.26171875,
                1.083984375, 0.060546875, 0.8037109375, 0.48828125, 0.48828125, 0.244140625, 0.244140625, 0.244140625, 0.1220703125, 0.5419921875, 1.220703125,
                4.39453125, 0.68359375, 0.1806640625, 0.090234375, 0.6015625, 2.197265625, 1.630859375, 1.630859375, 0.6611328125, 0.8037109375, 0.8037109375,
                0.8037109375, 0.8037109375, 0.244140625, 0.439453125, 0.244140625, 0.439453125, 0.244140625, 0.244140625, 0.439453125, 0.244140625, 0.439453125,
                0.244140625, 0.439453125, 0.244140625, 0.244140625, 0.8447265625, 0.244140625, 0.244140625, 0.244140625, 0.48828125, 0.2705078125, 1.357421875,
                0.5419921875, 1.9677734375, 0.17822265625, 2.4169921875, 0.0244140625, 0.0244140625, 0.01220703125, 0.0123046875, 0.0732421875, 0.78125, 0.48828125,
                0.15625, 0.1220703125, 0.01220703125, 0.01220703125, 0.048828125, 0.0048828125, 0.0390625, 0.015625, 0.01220703125, 0.0244140625, 0.01220703125,
                0.01220703125, 0.03662109375, 0.0244140625, 0.03662109375, 0.01220703125, 0.01220703125, 0.01220703125, 0.003662109375, 0.006103515625, 0.01220703125, 0.003662109375,
                0.00732421875, 0.01220703125, 0.4638671875, 0.4638671875, 0.279296875, 0.09765625, 0.09765625, 0.009765625, 0.009765625, 0.2705078125, 0.5419921875]


sizes = [(1430, 1280), (9152, 8192), (4576, 4096), (1144, 1024), (2860, 2560), (2288, 2048)]

def ImageNames(path = None):
    #return sorted(os.listdir(path) if path != None else os.listdir(), key = lambda x:int(x.replace('image', '').replace('.png', '')))
    return sorted(os.listdir(path) if path != None else os.listdir(), key = lambda x:int(re.findall('\d+',x)[0]))

def ResizeIm(imlist, shape):
    resized = []
    for i in imlist:
        resized. append(cv2.resize(i))
    return np.array(resized)

def train_allocate(ldir = 'labeled/', src = f'D:/task/task/data_resized/', dest = 'D:/task/task/data/train'):
    labels = os.listdir(ldir)
    # src = f'D:/task/task/data_resized/{file[:-3]}png'
    # dest = 'D:/task/task/data/train'
    # shutil.copy(src, dest)
    for i in labels:
        s = src + f"{i[:-3]}png"
        shutil.copy(s, dest)

def Rename(path):
    os.chdir(path)
    filenames = os.listdir()
    # print(filenames)
    c = 1
    for f in filenames:
        os.rename(f, "image" + str(c) + ".png")
        c += 1

def ImgResize(path):
    filenames = ImageNames(path)
    for f in filenames:
        im = cv2.imread(os.path.join(path, f))
        t = cv2.resize(im, (1024, 1144))
        cv2.imwrite(os.path.join("data_resized",f), t)

def ImgCutter(path):
    filenames = ImageNames(path)
    i = 1
    for f in filenames:
        img = cv2.imread(os.path.join(path, f))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h,w = img.shape
        scale = img[1024:1144, 0:1024]
        img = img[0:1024, 0:1024]
        cv2.imwrite(os.path.join('data_cropped', 'image'+ str(i) + '_c.png'), img)
        cv2.imwrite(os.path.join('data_scales','image'+ str(i) + '_s.png') , scale)
        i+=1

def GetCoefficents():
    #Coefficents = Image Width/Viewfield size
    
    os.chdir("C:\\Users\\HARUT\\PycharmProjects\\pythonProject1\\data") #path for data
    filenames = ImageNames()
    coeffs = []
    print(filenames)
    for i in range(len(filenames)):
        img = cv2.imread(filenames[i])
        h,w, _ = img.shape
        coeffs.append(scale_size[i]/w)
    print(img.shape)
    return coeffs

def ReadScale(img):
    reader = easyocr.Reader(['en'])
    # result = reader.readtext(input, allowlist='0123456789')

    # img = cv2.imread(imgName)
    config = ('-l eng --oem 1 --psm 3')
    result = reader.readtext(img, detail=0, paragraph=True)

    #scale, label = str(result)
    reslist = str(result).split(":")
    #reslist = str(result)
    print(reslist)
    p = '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
    # print(reslist.find("field"))

    for i in range(len(reslist)):
        if (reslist[i].find("field") != -1):
            print(reslist[i])
            t = reslist[i+1]
            num = float(re.findall(p, t)[0])
            print(num)
            tt = t.split()[1][:2]
            if tt.find("u") != -1:
                res = num
            else:
                res = (num*1000)
            print(res)
            return res

