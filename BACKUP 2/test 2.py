from PIL import Image

Height = 200
img = Image.open('images/img0.jpg')
wpercent = (Height / float(img.size[0]))
Width = int((float(img.size[1]) * float(wpercent)))

img = img.resize((Width, Height), Image.ANTIALIAS)
img.save('imgResized.jpg')