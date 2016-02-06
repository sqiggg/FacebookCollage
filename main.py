import functions as func
import tkinter

appSecret = "ae2390a60897c7973aa2ba5ba77deab5"
appId = "1530078440617793"
acessToken = func.getNewOauthKey(appId, appSecret)

width = 1344
height = 768

window = tkinter.Tk()
window.geometry("300x300")
window.title("Desktop Picture Creator")

def main():
    func.getRow(acessToken, height, width)
    window.quit()


var = tkinter.StringVar()
label = tkinter.Message(window, textvariable=var)

var.set("Press to to get started then wait till it closes")

B = tkinter.Button(window, text ="Go", command=main)


label.pack()
B.pack()
window.mainloop()