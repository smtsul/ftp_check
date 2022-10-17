from ftplib import FTP
from time import sleep
import telebot
from config import *
import logging

bot = telebot.TeleBot(TOKEN, threaded=False)
ftp = FTP(ip)
ftp.login(user=userr, passwd=passwrd)

#bot.send_message(id_sms_telegram, 'присоединился к ФТП')


def checking():
    dir_anonc = './/Анонсы'
    dir_osn = './'
    first_prev = set(ftp.nlst(dir_anonc))
    sec_prev = set(ftp.nlst(dir_osn))
    while True:
        bot.infinity_polling()  # test
        first = set(ftp.nlst(dir_anonc))
        add, rem = first - first_prev, first_prev - first
        if add or rem:
            yield add, rem
        first_prev = first
        second = set(ftp.nlst(dir_osn))
        add_sec, rem_sec = second - sec_prev, sec_prev - second
        if add_sec or rem_sec:
            yield add_sec, rem_sec
        sec_prev = second
        sleep(5)


LOG_FILENAME = 'loger.log'
logging.basicConfig(format='%(asctime)s-%(levelname)s-%(message)s',
                    filename=LOG_FILENAME, level=logging.INFO, encoding='UTF-8')
for add, rem in checking():
    s = ''
    s += ('\n'.join('+ %s' % i for i in add))
    s += ('\n'.join('- %s' % i for i in rem))
    bot.send_message(id_sms_telegram, s)

for add_sec, rem_sec in checking():
    s = ''
    s += ('\n'.join('+ %s' % i for i in add_sec))
    s += ('\n'.join('- %s' % i for i in rem_sec))
    bot.send_message(id_sms_telegram, s)

ftp.quit()