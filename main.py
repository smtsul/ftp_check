from ftplib import FTP
import time
import telebot
from config import *
import logging

bot = telebot.TeleBot(TOKEN, threaded=False)
LOG_FILENAME = 'loger.log'
logging.basicConfig(format='%(asctime)s-%(levelname)s-%(message)s',
                    filename=LOG_FILENAME, level=logging.INFO, encoding='UTF-8')


def checking(first_prev, sec_prev):  # есть предположение, что падает раз в 6 дней
    dir_anonc = './/Анонсы'
    dir_osn = './'
    s, s1 = '', ''
    ftp = FTP(ip)
    ftp.login(user=userr, passwd=passwrd)
    first = set(ftp.nlst(dir_anonc))
    second = set(ftp.nlst(dir_osn))
    add = first - first_prev
    add_sec = second - sec_prev
    s += ('\n'.join('+ %s' % i for i in add))
    s1 += ('\n'.join('+ %s' % i for i in add_sec))
    while s == "" or s1 == "":
        first = set(ftp.nlst(dir_anonc))
        second = set(ftp.nlst(dir_osn))
        add = first - first_prev
        add_sec = second - sec_prev
        s += ('\n'.join('+ %s' % i for i in add))
        s1 += ('\n'.join('+ %s' % i for i in add_sec))
        time.sleep(180)
        if s != '' or s1 != '':
            return s, s1
    else:
        return s, s1


# надо завернуть в мэйн=нэйм, ебануть еще один цикл и не сойти с ума
def restart():
    try:
        dir_anonc = './/Анонсы'
        dir_osn = './'
        ftp = FTP(ip)
        ftp.login(user=userr, passwd=passwrd)
        first_prev = set(ftp.nlst(dir_anonc))
        sec_prev = set(ftp.nlst(dir_osn))
        # time.sleep(10)
        ftp.quit()
        s, s1 = checking(first_prev, sec_prev)
        if s != '':
            bot.send_message(id_sms_telegram, s)
            logging.info(s)
        if s1 != '':
            bot.send_message(id_sms_telegram, s1)
            logging.info(s1)
        restart()
    except Exception as e:
        logging.info(e)
        restart()


if __name__ == '__main__':
    bot.send_message(id_sms_telegram, 'bot started on test mode')
    logging.info('start main_test.pyw')
    restart()
