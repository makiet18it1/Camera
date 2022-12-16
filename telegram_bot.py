import telegram

def sendMessage():
    try:
        my_token = "5722526497:AAEI_FoFddGf55OJZlDtZgtsC3GaJn0SkNM"
        bot = telegram.Bot(token=my_token)
        bot.sendMessage(chat_id="5408192472", text="Warning !!!")
    except Exception as ex:
        print("Error sending message", ex)

    print("Sucess")

