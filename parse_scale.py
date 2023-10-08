import easyocr
import re

def parser(img):
    reader = easyocr.Reader(['en'])
    # result = reader.readtext(input, allowlist='0123456789')

    # img = cv2.imread(imgName)
    config = ('-l eng --oem 1 --psm 3')
    result = reader.readtext(img, detail=0, paragraph=True)

    #scale, label = str(result)
    reslist = str(result).split(":")
    #reslist = str(result)
    # print(reslist)
    p = '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
    # print(reslist.find("field"))

    for i in range(len(reslist)):
        if (reslist[i].find("field") != -1):
            # print(reslist[i])
            t = reslist[i+1]
            num = float(re.findall(p, t)[0])
            # print(num)
            tt = t.split()[1][:2]
            if tt.find("u") != -1:
                res = num
            else:
                res = (num*1000)
            # print(res)
            return res, 'um'