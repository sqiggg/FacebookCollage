import requests
import json
import functions as func
from PIL import Image
appSecret = "ae2390a60897c7973aa2ba5ba77deab5"
appId = "1530078440617793"
acessToken = func.getNewOauthKey(appId, appSecret)

r = requests.get("https://graph.facebook.com/247660352007607/photos?limit=2&access_token=" + acessToken)
contentr = json.loads(r.text)

image0 = contentr['data'][0]['id']
imgURL = func.getImageUrl(image0, acessToken)

width = 1344
height = 768
#func.downloadImage("img", imgURL)

imgCount = 0
image = []
x = 0
while x < width:
    if imgCount == 2:
        next = contentr['paging']['cursors']['after']
        r = requests.get("https://graph.facebook.com/247660352007607/photos?limit=2&after="+ str(next) +"&access_token=" + acessToken)
        contentr = json.loads(r.text)

        image0 = contentr['data'][0]['id']
        imgURL = func.getImageUrl(image0, acessToken)

        imgCount = 0

    try:
        image.append(func.getImageUrl(contentr['data'][imgCount]['id'], acessToken))
        x += func.getImageSize(image[imgCount])[0]
        imgCount += 1
    except IndexError:
        print(x)
        break

name = 0
for x in image:
    func.downloadImage("img" + str(name), x)
    name += 1

#resizing them
name = 0
smallest = 0
for x in image:
    img = Image.open("images/img" + str(name) + '.jpg')
    print(img.size, name)
    h = img.size[1]
    w = img.size[0]

    if h > smallest:
        smallest = h
    name += 1


for x in range(0, len(image), 1):
    func.resize(smallest, "images/img" + str(x))

func.merge_images(['images/img0.jpg', 'images/img1.jpg', 'images/img2.jpg']).save('merged.jpg')

print("Done")
