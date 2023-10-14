import easyocr
import re


def parse(img):
    reader = easyocr.Reader(['en'])

    config = ('-l eng --oem 1 --psm 3')
    result = reader.readtext(img, detail=0, paragraph=True)

    reslist = str(result).split(":")
    p = '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'

    for i in range(len(reslist)):
        if (reslist[i].find("field") != -1):
            t = reslist[i+1]
            num = float(re.findall(p, t)[0])
            tt = t.split()[1][:2]
            if tt.find("u") != -1:
                res = num
            else:
                res = (num*1000)
            return res, 'um'


def save():
    pass


def load():
    pass
