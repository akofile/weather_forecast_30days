import requests
from bs4 import BeautifulSoup
import telebot


bot_api = ''

cloud={'//yastatic.net/weather/i/icons/funky/dark/bkn_-ra_d.svg':'солнечно, небольшой дождь.', '//yastatic.net/weather/i/icons/funky/dark/ovc_-ra.svg':'облачно',
       '//yastatic.net/weather/i/icons/funky/dark/ovc_ra.svg':'Дождь', '//yastatic.net/weather/i/icons/funky/dark/skc_d.svg':'солнечно',
       '//yastatic.net/weather/i/icons/funky/dark/ovc_sn.svg':'Снег', '//yastatic.net/weather/i/icons/funky/dark/bkn_d.svg':'переменная облачность'}

def yandex_parse(date):
    res = requests.get('https://yandex.ru/pogoda/16/month',headers={'user-agent': 'Mozilla Firefox/51.0.1'})
    html = res.content
    soup = BeautifulSoup(html, 'lxml')
    for el in soup.select('.climate-calendar-day'):
        if el.get_text().find(date)>0:
            text=el.get_text()
            response={}
            response['Температура днём']=text.split('°')[0].replace(date.split(' ')[0],'')+'°'
            response['ночью'] = text.split('°')[1]+'°'
            response['Давление'] = text.split('°')[5][:text.split('°')[5].find('ст.')+3]
            response['Влажность'] = text.split('°')[5][text.split('°')[5].find('ст.') + 3:].split('%')[0]+'%'

            try:
                response['Погода']=cloud[el.find_all('img')[0]['src']]
            except:
                response['Погода'] = 'Неясная вероятность дождя'
                return(response)

            return(response)


bot = telebot.TeleBot(bot_api)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Здравствуйте, чтобы узнать погоду введите "день месяц", например "30 июля" ' )


@bot.message_handler(content_types=['text'])
def handle(msg):
    if len(msg.text.split(' '))==2:
        if msg.text.split(' ')[0].isdigit():
            chat = msg.chat.id
            try:
                response=str(yandex_parse(msg.text)).replace('{','').replace('}','').replace("'",'')
                bot.send_message(str(msg.chat.id), response)
            except Exception as ex:
                bot.send_message(str(msg.chat.id)
                                 , 'Необработанная ошибка:' + str(ex))

        else:
            bot.send_message(str(msg.chat.id), 'Неверный формат ввода')
    else:
        bot.send_message(str(msg.chat.id), 'Неверный формат ввода')

bot.polling()
