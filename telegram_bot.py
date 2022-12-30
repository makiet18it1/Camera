import telegram

def sendMessage(photo_path="", caption=""):
    try:
        my_token = "5722526497:AAEI_FoFddGf55OJZlDtZgtsC3GaJn0SkNM"
        bot = telegram.Bot(token=my_token)
        bot.sendPhoto(chat_id="5408192472", photo=open(photo_path, "rb") ,caption=caption)
    except Exception as ex:
        print("Error sending message", ex)

    print("Sucess")




