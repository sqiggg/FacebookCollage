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


    print(result_height)
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
def getResolution():
    h = int(input("Enter the height of your monitor in Px: "))
    w = int(input("Enter the width of your monitor in Px: "))
    return (w, h)
def getImageSize(url):
    data = requests.get(url).content
    im = Image.open(BytesIO(data))
    return im.size