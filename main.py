from ftplib import FTP
from time import sleep
import telebot
from config import *
import logging

bot = telebot.TeleBot(TOKEN, threaded=False)


def checking():
    dir_anonc = './/Анонсы'
    dir_osn = './'
    ftp = FTP(ip)
    ftp.login(user=userr, passwd=passwrd)
    first_prev = set(ftp.nlst(dir_anonc))
    sec_prev = set(ftp.nlst(dir_osn))
    ftp.quit()
    sleep(5)  # так нужно
    k = 100
    while True:
        ftp = FTP(ip)
        ftp.login(user=userr, passwd=passwrd)
        if k == 100:
            bot.send_message(id_sms_telegram, 'присоединился к ФТП ')
            k = 5
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
        sleep(180) # так тоже нужно


LOG_FILENAME = 'loger.log'
logging.basicConfig(format='%(asctime)s-%(levelname)s-%(message)s',
                    filename=LOG_FILENAME, level=logging.INFO, encoding='UTF-8')
logging.info('start bot')

for add, rem in checking():
    s, g = '', ''
    s += ('\n'.join('+ %s' % i for i in add))  # добавление файла
    g += ('\n'.join('- %s' % i for i in rem))  # удаление фала
    logging.info(s)
    logging.info(g)
    bot.send_message(id_sms_telegram, s)

for add_sec, rem_sec in checking():
    s, g = '', ''
    s += ('\n'.join('+ %s' % i for i in add_sec))  # добавление файла
    g += ('\n'.join('- %s' % i for i in rem_sec))  # удаление фала
    logging.info(s)
    logging.info(g)
    bot.send_message(id_sms_telegram, s)

# ftp.quit()
