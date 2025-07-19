import requests
from bs4 import BeautifulSoup

def get_program_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    

    program_name = soup.find('h1').text.strip()
    courses = soup.find_all('div', class_='course-item')  
    
    course_list = []
    for course in courses:
        course_name = course.find('span', class_='course-name').text.strip()
        course_description = course.find('span', class_='course-description').text.strip()
        course_list.append((course_name, course_description))
    
    return program_name, course_list


url1 = 'https://abit.itmo.ru/program/master/ai'
url2 = 'https://abit.itmo.ru/program/master/ai_product'

program1_name, program1_courses = get_program_data(url1)
program2_name, program2_courses = get_program_data(url2)


print(f"Программа 1: {program1_name}")
for course in program1_courses:
    print(course)

print(f"Программа 2: {program2_name}")
for course in program2_courses:
    print(course)
    
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Здравствуйте! Я помогу вам выбрать подходящую магистерскую программу и планировать учебу.')


def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text.lower()
    

    if 'ai' in user_message:
        update.message.reply_text(f"Вы интересуетесь программой '{program1_name}'. Вот ее курсы:\n" + "\n".join([course[0] for course in program1_courses]))
    elif 'ai product' in user_message:
        update.message.reply_text(f"Вы интересуетесь программой '{program2_name}'. Вот ее курсы:\n" + "\n".join([course[0] for course in program2_courses]))
    else:
        update.message.reply_text('Извините, я не понял ваш запрос. Могу помочь вам с выбором программы или объяснением учебных курсов.')


def main() -> None:
    updater = Updater("7452994690:AAFgFGdx2FgotjEtavCXA_BT6HHdnYjtKRM")
    dispatcher = updater.dispatcher
    
   
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    updater.start_polling()
    updater.idle()
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_background))
    
    updater.start_polling()
    updater.idle()


def get_background(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Пожалуйста, расскажите о вашем образовании (например, бакалавриат в области ИТ или другой технический опыт).')

def handle_background(update: Update, context: CallbackContext) -> None:
    user_background = update.message.text.lower()
    # Сопоставляем бэкграунд с программой
    if 'машинное обучение' in user_background:
        update.message.reply_text('Рекомендуем вам обратить внимание на курсы по машинному обучению в программе AI.')
    elif 'программирование' in user_background:
        update.message.reply_text('Если ваш опыт связан с программированием, программа AI Product будет хорошим выбором, так как она включает более глубокие аспекты разработки продуктов.')
    else:
        update.message.reply_text('Для вас могут подойти оба направления, мы поможем выбрать лучший вариант в дальнейшем.')


