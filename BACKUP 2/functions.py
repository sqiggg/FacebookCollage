from PIL import Image
import shutil
from io import BytesIO
import requests
import json

def resize(height, imgName):
    Height = height
    img = Image.open(imgName + '.jpg')
    wpercent = (Height / float(img.size[1]))
    Width = int((float(img.size[0]) * float(wpercent)))

    img = img.resize((Width, Height), Image.ANTIALIAS)
    img.save(imgName + '.jpg')
def merge_images(files):

    result_width = 0
    result_height = []

    for x in files: result_width = result_width + Image.open(x).size[0]
    for x in files: result_height += [Image.open(x).size[1]]


    #print(result_height)
    result_height = min(result_height)
    result = Image.new('RGB', (result_width, result_height))

    heightWidth = (0,0)
    for x in files:
        result.paste(im=Image.open(x), box=heightWidth)
        heightWidth = (heightWidth[0] + Image.open(x).size[0], 0)
    return result
def getNewOauthKey(appId, appSecret):
    z = requests.get("https://graph.facebook.com/oauth/access_token?grant_type=client_credentials&client_id="+ appId +"&client_secret=" + appSecret)
    return z.text[len("access_token="):len(z.text)]
def getImageUrl(id, token):
    p = requests.get("https://graph.facebook.com/"+ id +"?fields=source&access_token=" + token)
    contentp = json.loads(p.text)
    return contentp['source']
def downloadImage(name, imgURL):
    response = requests.get(imgURL, stream=True)
    try:
        with open("images/" + str(name) + '.jpg', 'wb') as out_file:
            out_file.truncate()
            shutil.copyfileobj(response.raw, out_file)
        return True
    except:
        print("Error in downloading:" + str(name))
        return False
def getImageSize(url):
    data = requests.get(url).content
    im = Image.open(BytesIO(data))
    return im.size
def resize_merged(width, images):
    for x in images:
        img = Image.open(x)
        wpercent = (width/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((width,hsize), Image.ANTIALIAS)
        img.save(x)
def merge_multiples(images):
    result_width = []
    result_height = []

    for x in images:
        result_width += [Image.open(x).size[0]]
        result_height += [Image.open(x).size[1]]

    result_width = min(result_width)
    result_height = sum(result_height)
    result = Image.new('RGB', (result_width, result_height))

    heightWidth = (0,0)
    for x in images:
        result.paste(im=Image.open(x), box=heightWidth)
        heightWidth = (0, heightWidth[1] + Image.open(x).size[1])
    result.save("NEW.jpg")


def getRow(acessToken, height, width):
    import functions as func

    count = 0

    page = 0
    y = 0
    name = 0
    imgCount = 0

    imagesPerRow = [0]

    while y < height:
        print("---")


        r = requests.get("https://graph.facebook.com/247660352007607/photos?limit=1&access_token=" + acessToken)
        contentr = json.loads(r.text)
        for x in range(page):
            next = contentr['paging']['cursors']['after']
            r = requests.get("https://graph.facebook.com/247660352007607/photos?limit=1&after="+ str(next) +"&access_token=" + acessToken)
            contentr = json.loads(r.text)

        image = []
        x = 0
        while x < width:
            if imgCount >= 1:
                next = contentr['paging']['cursors']['after']
                r = requests.get("https://graph.facebook.com/247660352007607/photos?limit=1&after="+ str(next) +"&access_token=" + acessToken)
                contentr = json.loads(r.text)
                page += 1

                imgCount = 0
            try:
                image.append(func.getImageUrl(contentr['data'][imgCount]['id'], acessToken))
                nextX = x + func.getImageSize(image[imgCount])[0]
                if nextX-100 <= width:
                    x += func.getImageSize(image[imgCount])[0]
                    imgCount += 1
                    print(x)
                else:
                    image.pop()
                    break

            except IndexError:
                break

        for x in image:
            func.downloadImage("img" + str(name), x)
            name += 1

        #resizing them
        smallest = 0
        smallestW = 0
        resizeName = 0
        for z in image:
            img = Image.open("images/img" + str(resizeName) + '.jpg')
            h = img.size[1]
            w = img.size[0]

            if h > smallest:
                smallest = h
            if w > smallestW:
                smallestW = w
            resizeName += 1


        imagesPerRow.append(name-imagesPerRow[count])
        imagesName = []

        print(name)
        for z in range(imagesPerRow[count], name, 1):
            func.resize(smallest, "images/img" + str(z))
            imagesName.append("images/img" + str(z) + ".jpg")
        print(imagesName)
        print(imagesPerRow)

        func.merge_images(imagesName).save('merged' + str(count) + '.jpg')

        count += 1
        y = y + smallestW

    resize_merged(width, ["merged0.jpg", "merged1.jpg"])
    merge_multiples(["merged0.jpg", "merged1.jpg"])
