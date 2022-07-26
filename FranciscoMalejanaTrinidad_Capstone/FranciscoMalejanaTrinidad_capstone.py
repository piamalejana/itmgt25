import telebot
import numpy as np
import requests
import pandas as pd
import datetime
import json
import csv
import emoji
from apscheduler.schedulers.blocking import BlockingScheduler
from pandas import json_normalize
from datetime import datetime, timedelta, date
from telebot import TeleBot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# FOR TIMESERIES
start_date = date.today() - timedelta(days=7)  # last week
end_date = date.today()
yesterday = date.today() - timedelta(days=1)
base = 'PHP'

url = f"https://api.apilayer.com/fixer/timeseries?start_date={start_date}&end_date={end_date}&base={base}"

payload = {}
headers = {"apikey": "HKicRME0R0STk0kw17QiCvY2MD95c1Si"}

response = requests.request("GET", url, headers=headers, data=payload)

status_code = response.status_code
result = response.text

# FOR CURRENCY NAME
url1 = "https://api.apilayer.com/fixer/symbols"

payload1 = {}
headers1 = {"apikey": "HKicRME0R0STk0kw17QiCvY2MD95c1Si"}

response1 = requests.request("GET", url1, headers=headers1, data=payload1)

status_code1 = response1.status_code
result1 = response1.text

dict = json.loads(result)
dict1 = json.loads(result1)
dict2 = {"AED": 'United Arab Emirates',"AFN": 'Afghanistan',"ALL": 'Albania',"AMD": 'Armenia',"ANG": 'Netherlands Antilles',"AOA": 'Angola',"ARS": 'Argentina',"AUD": 'Australia',"AWG": 'Aruba',"AZN": 'Azerbaijan',"BAM": 'Bosnia and Herzegovina',"BBD": 'Barbados',"BDT": 'Bangladesh',"BGN": 'Bulgaria',"BHD": 'Bahrain',"BIF": 'Burundi',"BMD": 'Bermuda',"BND": 'Brunei',"BOB": 'Bolivia',"BRL": 'Brazil',"BSD": 'Bahamas',"BTC": 'Bitcoin',"BTN": 'Bhutan',"BWP": 'Botswana',"BYN": 'Belarus',"BYR": 'Belarus',"BZD": 'Belize',"CAD": 'Canada',"CDF": 'Democratic Republic of the Congo',"CHF": 'Switzerland',"CLF": 'Chile',"CLP": 'Chile',"CNY": 'China',"COP": 'Colombia',"CRC": 'Costa Rica',"CUC": 'Cuba',"CUP": 'Cuba',"CVE": 'Cape Verde',"CZK": 'Czech Republic',"DJF": 'Djibouti',"DKK": 'Denmark',"DOP": 'Dominican Republic',"DZD": 'Algeria',"EGP": 'Egypt',"ERN": 'Eritrea',"ETB": 'Ethiopia',"EUR": 'European Union',"FJD": 'Fiji',"FKP": 'Falkland Islands',"GBP": 'United Kingdom',"GEL": 'Georgia',"GGP": 'Guernsey',"GHS": 'Ghana',"GIP": 'Gibraltar',"GMD": 'The Gambia',"GNF": 'Guinea',"GTQ": 'Guatemala',"GYD": 'Guyana',"HKD": 'Hong Kong',"HNL": 'Honduras',"HRK": 'Croatia',"HTG": 'Haiti',"HUF": 'Hungary',"IDR": 'Indonesia',"ILS": 'Israel',"IMP": 'Isle of Man',"INR": 'India',"IQD": 'Iraq',"IRR": 'Iran',"ISK": 'Iceland',"JEP": 'Jersey',"JMD": 'Jamaica',"JOD": 'Jordan',"JPY": 'Japan',"KES": 'Kenya',"KGS": 'Kyrgyzstan',"KHR": 'Cambodia',"KMF": 'Comoros',"KPW": 'North Korea',"KRW": 'South Korea',"KWD": 'Kuwait',"KYD": 'Cayman Islands',"KZT": 'Kazakhstan',"LAK": 'Laos',"LBP": 'Lebanon',"LKR": 'Sri Lanka',"LRD": 'Liberia',"LSL": 'Lesotho',"LTL": 'Lithuania',"LVL": 'Latvia',"LYD": 'Libya',"MAD": 'Morocco',"MDL": 'Moldova',"MGA": 'Madagascar',"MKD": 'North Macedonia',"MMK": 'Myanmar',"MNT": 'Mongolia',"MOP": 'Macau',"MRO": 'Mauritania',"MUR": 'Mauritius',"MVR": 'Maldives',"MWK": 'Malawi',"MXN": 'Mexico',"MYR": 'Malaysia',"MZN": 'Mozambique',"NAD": 'Namibia',"NGN": 'Nigeria',"NIO": 'Nicaragua',"NOK": 'Norway',"NPR": 'Nepal',"NZD": 'New Zealand',"OMR": 'Oman',"PAB": 'Panama',"PEN": 'Peru',"PGK": 'Papua New Guinea',"PHP": 'Philippines',"PKR": 'Pakistan',"PLN": 'Poland',"PYG": 'Paraguay',"QAR": 'Qatar',"RON": 'Romania',"RSD": 'Serbia',"RUB": 'Russia',"RWF": 'Rwanda',"SAR": 'Saudi Arabia',"SBD": 'Solomon Islands',"SCR": 'Seychelles',"SDG": 'Sudan',"SEK": 'Sweden',"SGD": 'Singapore',"SHP": 'Saint Helena',"SLL": 'Sierra Leone',"SOS": 'Somalia',"SRD": 'Suriname',"STD": 'S\u00e3o Tom\u00e9 and Pr\u00edncipe',"SVC": 'El Salvador',"SYP": 'Syria',"SZL": 'Eswatini',"THB": 'Thailand',"TJS": 'Tajikistan',"TMT": 'Turkmenistan',"TND": 'Tunisia',"TOP": 'Tonga',"TRY": 'Turkey',"TTD": 'Trinidad and Tobago',"TWD": 'Taiwan',"TZS": 'Tanzania',"UAH": 'Ukraine',"UGX": 'Uganda',"USD": 'United States',"UYU": 'Uruguay',"UZS": 'Uzbekistan',"VND": 'Vietnam',"VUV": 'Vanuatu',"WST": 'Samoa',"XAF": 'CEMAC',"XAG": 'Silver',"XAU": 'Gold',"XCD": 'Organisation of Eastern Caribbean States',"XDR": 'International Monetary Fund',"XOF": 'CFA',"XPF": "Collectivités d'Outre-Mer","YER": 'Yemen',"ZAR": 'South Africa',"ZMK": 'Zambia',"ZMW": 'Zambia',"ZWL": 'Zimbabwe'}
df = json_normalize(dict['rates'][str(start_date)]).transpose()
df.rename(columns={0: str(start_date)}, inplace=True)
df[str(yesterday)] = json_normalize(dict['rates'][str(yesterday)]).transpose()
df[str(end_date)] = json_normalize(dict['rates'][str(end_date)]).transpose()
df['1d difference'] = round((df[str(yesterday)] - df[str(end_date)]), 6)
df['1w difference'] = round((df[str(start_date)] - df[str(end_date)]), 6)
df['1d % change'] = round((((df[str(end_date)] - df[str(yesterday)]) / df[str(yesterday)]) * 100), 6)
df['1w % change'] = round((((df[str(end_date)] - df[str(start_date)]) / df[str(start_date)]) * 100),6)
df['currency name'] = json_normalize(dict1['symbols']).transpose()
df['country'] = dict2.values()

bot = telebot.TeleBot("5402039692:AAFPg1QDAb4MwzVEGsD_KbV5p5yNsvEFVMk")

# INSERT INTRO HERE - includes what currencies they want updates on (base currency PHP)
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,emoji.emojize("Hi! Juan Peso at your service.:man: I'm here to give you the latest currency updates.:money_bag:\n \n Press :chart_increasing:UPDATE:chart_increasing: if you need updates with the current currency exchange.\n\nPress :money_with_wings:CONVERTER:money_with_wings: if you want to manually convert PHP to another currency\n\nPress :world_map:GENERATE CURRENCY CODE:world_map: if you do not know your country\'s currency code\n\nLastly, press :calendar:SCHEDULE UPDATE:calendar: if you want to be updated with regards to currency exchange"), reply_markup=markup())

def markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton(emoji.emojize(":chart_increasing:UPDATE:chart_increasing:"), callback_data="update"),
             InlineKeyboardButton(emoji.emojize(":money_with_wings:CONVERTER:money_with_wings:"), callback_data="converter"),
             InlineKeyboardButton(emoji.emojize(":world_map:GENERATE CURRENCY CODE:world_map:"), callback_data="generate"),
             InlineKeyboardButton(emoji.emojize(":calendar:SCHEDULE UPDATE:calendar:"), callback_data="schedule"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    
    #IF USER CHOSE UPDATE
    if call.data == "update":
        # UPDATE CODE
        bot.send_message(call.message.chat.id,emoji.emojize("To get an :chart_increasing:UPDATE:chart_increasing:, send me a message like this:\nupdate [currency code] - (ex. update USD)\n- This allows you to see the latest exchange rate and percent change of a currency of your choice using PHP as the base currency."))
        def update_request(message):
            request = message.text.split()
            if len(request) < 2 or request[0].lower() not in "update":
                return False
            else:
                return True

        @bot.message_handler(func=update_request)
        def send_update(message):
            request = message.text.split()[1]
            if request in df.index:
                data = list(df.loc[request])
                print(data)
                bot.send_message(message.chat.id,emoji.emojize(f"Hello! Here's your :chart_increasing:UPDATE:chart_increasing::\nCURRENCY: {data[7]}\nCOUNTRY: {data[8]}\nRATE: {data[2]}\n1D CHANGE: {data[5]}%\n1W CHANGE: {data[6]}%"))
            else:
                bot.send_message(message.chat.id,emoji.emojize(":warning:Sorry, we don't have this data. Please try again.:warning:"))
                
    #IF USER CHOSE CONVERT
    elif call.data == "converter":
        #CONVERTER CODE
        bot.send_message(call.message.chat.id,emoji.emojize("If you want to :money_with_wings:CONVERT:money_with_wings: PHP to another currency, send:\n convert [amount] to [currency code] - (ex. convert 1000 to USD)\n"))  
        def converter_request(message):
            request = message.text.split()
            if len(request) < 4 or request[0].lower() not in "convert":
                return False
            else:
                return True
            
        @bot.message_handler(func=converter_request)
        def send_convert(message):
            request = message.text.split()[3]
            amount = int(message.text.split()[1])
            data = list(df.loc[request])
            convert_formula = amount * data[2]
            if data is None:
                bot.send_message(message.chat.id, emoji.emojize(":warning:Sorry, we don't have this data. Please try again.:warning:"))
            else:
                print(convert_formula)
                bot.send_message(message.chat.id,emoji.emojize(f"Here you go!\n CURRENCY EXCHANGE: {convert_formula} :dollar_banknote:"))
                
    #IF USER CHOSE GENERATE
    elif call.data == "generate":
        # GENERATE CURRENCY CODE
        bot.send_message(call.message.chat.id, emoji.emojize("\n\nIf you don't know the :world_map:CURRENCY CODE:world_map:, you can send the following message to generate it:\ngencode [country name] - (ex. gencode United States)"))
        def code_request(message):
            request = message.text.split(' ', 1)
            if len(request) < 2 or request[0].lower() not in "gencode":
                return False
            else:
                return True
            
        @bot.message_handler(func=code_request)
        def send_code(message):
            request = message.text.split(' ', 1)[1]
            if df['country'].eq(request).any():
                code = df.index[df['country'] == request].tolist()
                name = list(df[df['country'] == request]['currency name'])
                dictionary = {code: name for code, name in zip(code, name)}
                keys = list(dictionary.keys())
                values = list(dictionary.values())
                if len(dictionary) == 1:
                    print(dictionary)
                    bot.send_message(message.chat.id,f"{request}\nCODE: {keys[0]} | {values[0]}")
                elif len(dictionary) == 2:
                    print(dictionary)
                    bot.send_message(message.chat.id,f"{request}\n1) {keys[0]} | {values[0]}\n2) {keys[1]} | {values[1]}")
            else:
                bot.send_message(message.chat.id,"Sorry, we don't have this data. Please try again.")
                
    #IF USER CHOSE SCHEDULE
    elif call.data == "schedule":
        # SET CURRENCY FOR DAILY UPDATES (storing their message)
        bot.send_message(call.message.chat.id,"Okay Sure! Type /set to get started!")
        # CREATING STORAGE
        columns = ['ID', 'currency code']
        with open('code.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(columns)
        
        @bot.message_handler(commands=['set'])
        def set_daily_updates(message):
            sent = bot.send_message(call.message.chat.id,"Send me the code of the currency you want to get daily updates on (example: 'USD')")
            bot.register_next_step_handler(sent, store_code)
            
        def store_code(message):
            if message.text in df.index:
                data = [message.chat.id, message.text]
                csv.writer(open('code.csv', 'a', newline="")).writerow(data)
                button_yes = types.InlineKeyboardButton('Yes', callback_data='yes')
                button_no = types.InlineKeyboardButton("No. Please cancel my request.",callback_data='no')
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(button_yes)
                keyboard.add(button_no)
                bot.send_message(message.chat.id,f"CODE: {message.text}\nGot this! Proceed with setup?",reply_markup=keyboard)
            else:
                bot.send_message(message.chat.id,"Sorry, we don't have this data. Try scheduling another one.")
          
        # SCHEDULE THE UPDATES
        @bot.callback_query_handler(func=lambda call: True)
        def update_callback(call):
            if call.data == 'yes':
                sched = BlockingScheduler()
                bot.send_message(call.message.chat.id, f"You're scheduled. See you!")
                
                storage = pd.read_csv('code.csv').groupby('ID')['currency code'].apply(' '.join).reset_index()
                storage['updated code'] = storage['currency code'].str[-3:]
                code = list(storage.loc[storage['ID'] == call.message.chat.id,'updated code'])[0]
                
                def send_update():
                    data = list(df.loc[code])
                    print(data)
                    bot.send_message(call.message.chat.id,f"Hello! Here's your update for the day:\nCURRENCY: {data[7]}\nCOUNTRY: {data[8]}\nRATE: {data[2]}\n1D CHANGE: {data[5]}%\n1W CHANGE: {data[6]}%")
                
                sched.add_job(send_update, trigger="cron", hour=22.25, id='job_id')
                sched.start()
                
            elif call.data == 'no':
                bot.send_message(call.message.chat.id, "Oh okay! Have a nice day!")
                
bot.polling()