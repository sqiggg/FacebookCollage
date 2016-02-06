import functions as func
appSecret = "ae2390a60897c7973aa2ba5ba77deab5"
appId = "1530078440617793"
acessToken = func.getNewOauthKey(appId, appSecret)

width = 1344
height = 768

func.getRow(acessToken, height, width)

print("Done")
