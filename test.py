from telegram_bot import sendMessage
import datetime


entry_time = datetime.datetime.now().strftime("%A, %I-%M-%S %p %d %B %Y")
sendMessage("Picture1.png",caption="Warning !!! " + entry_time)