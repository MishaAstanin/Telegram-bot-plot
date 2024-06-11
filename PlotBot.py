import telebot
from telebot import types
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('agg')

Bot = telebot.TeleBot('5841839336:AAFLSTbBroadPnrfAujIzmDm8AJ5Sk3kGnI')

bot_text = {
    'menu': 'Выберите тип графика:',
    'lin_p': 'Линейный график 📈',
    'bar_p': 'Столбчатая диаграмма 📊',
    'cir_p': 'Круговая диаграмма ⭕',
    'read': 'Считать',
    'read_f': 'Считать данные файла',
    'read_data': 'Данные обрабатываются',
    'color_lin': 'Выберите цвет графика:',
    'color_bar': 'Выберите цвет столбцов:',
    'axis_choice': 'Выберите названия осей:',
    'axis_yes': 'Настроить названия осей',
    'axis_no': 'Названия осей по умолчанию',
    'axis_input': 'Введите наименования осей\nПожалуйста, используйте формат:\n\nимя_оси_X\nимя_оси_Y',
    'lin_input': 'Введите координы точек\nПожалуйста, используйте формат:\n\nкоордината_X1 координата_Y1\nкоордината_X2 координата_Y2',
    'bar_input': 'Введите наименования столбцов и их значения\nПожалуйста, используйте формат:\n\nстолбец_1 значение_1\nстолбец_2 значение_2',
    'cir_input': 'Введите наимнование величины и её значение\nПожалуйста, используйте формат:\n\nвеличина_1 значение_1\nвеличина_2 значение_2',
    'err_choice': 'Я вас не понял, повторите выбор:',
    'input_err': 'Ошибка ввода данных\nПовторите попытку',
    'file_err': 'Пожалуйста, пришлите файл с расширением .txt',
    'answer_text': 'Я помогу тебе построить график📈\nВыбери команду или пришли txt файл:\n\n/start - Запуск бота\n/plot - Построить график\n/file - Формат данных в файле',
    'file_form': 'Необходимый формат данных в файле:\n\nДля линейного графика пожалуйста, используйте формат:\n\nкоордината_X1 координата_Y1\nкоордината_X2 координата_Y2\n\nДля столбчатой диаграммы пожалуйста, используйте формат:\n\nстолбец_1 значение_1\nстолбец_2 значение_2\n\nДля круговой диаграммы пожалуйста, используйте формат:\n\nвеличина_1 значение_1\nвеличина_2 значение_2'
}

colors = {'🟥': 'red',
          '🟧': 'orange',
          '🟨': 'yellow',
          '🟩': 'green',
          '🟦': 'blue',
          '🟪': 'purple',
          '⬛️': 'black',
          '🟫': 'brown'
          }

user_data = {}

panel = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
button1 = types.KeyboardButton(bot_text['lin_p'])
button2 = types.KeyboardButton(bot_text['bar_p'])
button3 = types.KeyboardButton(bot_text['cir_p'])
panel.add(button1, button2, button3)

color_panel = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
color_buttons = [types.KeyboardButton(color) for color in colors]
color_panel.add(*color_buttons)

axis_panel = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
button4 = types.KeyboardButton(bot_text['axis_yes'])
button5 = types.KeyboardButton(bot_text['axis_no'])
axis_panel.add(button4, button5)

t_panel = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
button6 = types.KeyboardButton(bot_text['read'])
t_panel.add(button6)

close_panel = types.ReplyKeyboardRemove()


@Bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name
    bot_hello = f'Привет, <b>{user_name}</b>, я помогу тебе построить график! 📈' \
                f'\nВыбери команду или пришли txt файл:\n\n/start - Запуск бота\n/plot - Построить график\n/file - Формат данных в файле'
    Bot.send_message(message.chat.id, bot_hello, parse_mode='html')


@Bot.message_handler(commands=['plot'])
def command_plot(message):
    user_data[message.chat.id] = dict()
    Bot.send_message(message.chat.id, bot_text['menu'], reply_markup=panel)
    Bot.register_next_step_handler(message, choice)


@Bot.message_handler(commands=['file'])
def file_form(message):
    Bot.send_message(message.chat.id, bot_text['file_form'])


@Bot.message_handler(content_types=['document'])
def document(message):
    if message.document.mime_type == 'text/plain' and message.document.file_name.endswith('.txt'):
        user_data[message.chat.id] = dict()

        file_info = Bot.get_file(message.document.file_id)
        file = Bot.download_file(file_info.file_path)
        text_file = file.decode('utf-8')
        user_data[message.chat.id]['text_f'] = text_file

        Bot.send_message(message.chat.id, bot_text['menu'], reply_markup=panel)
        Bot.register_next_step_handler(message, choice)
    else:
        Bot.send_message(message.chat.id, bot_text['file_err'])


@Bot.message_handler(content_types=['sticker'])
def user_text(message):
    Bot.send_message(message.chat.id, bot_text['answer_text'])


@Bot.message_handler(content_types=['text'])
def user_text(message):
    Bot.send_message(message.chat.id, bot_text['answer_text'])


def choice(message):
    if message.text == bot_text['lin_p']:
        user_data[message.chat.id]['plot'] = 'lin_plot'
        Bot.send_message(message.chat.id, bot_text['color_lin'], reply_markup=color_panel)
        Bot.register_next_step_handler(message, color_choice)
    elif message.text == bot_text['bar_p']:
        user_data[message.chat.id]['plot'] = 'bar_plot'
        Bot.send_message(message.chat.id, bot_text['color_bar'], reply_markup=color_panel)
        Bot.register_next_step_handler(message, color_choice)
    elif message.text == bot_text['cir_p']:
        if 'text_f' not in user_data[message.chat.id]:
            Bot.send_message(message.chat.id, bot_text['cir_input'], reply_markup=close_panel)
            Bot.register_next_step_handler(message, circle_plot_data)
        else:
            Bot.send_message(message.chat.id, bot_text['read_f'], reply_markup=t_panel)
            Bot.register_next_step_handler(message, circle_plot_data)
    else:
        Bot.send_message(message.chat.id, bot_text['err_choice'], reply_markup=panel)
        Bot.register_next_step_handler(message, choice)


def color_choice(message):
    if message.text in colors.keys():
        user_data[message.chat.id]['color'] = colors[message.text]
        Bot.send_message(message.chat.id, bot_text['axis_choice'], reply_markup=axis_panel)
        Bot.register_next_step_handler(message, axis_choice)
    else:
        Bot.send_message(message.chat.id, bot_text['err_choice'], reply_markup=color_panel)
        Bot.register_next_step_handler(message, color_choice)


def axis_choice(message):
    if message.text == bot_text['axis_yes']:
        Bot.send_message(message.chat.id, bot_text['axis_input'], reply_markup=close_panel)
        Bot.register_next_step_handler(message, input_axis)
    elif message.text == bot_text['axis_no']:
        user_data[message.chat.id]['X_axis'] = 'Ось X'
        user_data[message.chat.id]['Y_axis'] = 'Ось Y'
        if user_data[message.chat.id]['plot'] == 'lin_plot' and 'text_f' not in user_data[message.chat.id]:
            Bot.send_message(message.chat.id, bot_text['lin_input'], reply_markup=close_panel)
            Bot.register_next_step_handler(message, linear_plot_data)
        elif user_data[message.chat.id]['plot'] == 'bar_plot' and 'text_f' not in user_data[message.chat.id]:
            Bot.send_message(message.chat.id, bot_text['bar_input'], reply_markup=close_panel)
            Bot.register_next_step_handler(message, bar_plot_data)
        elif user_data[message.chat.id]['plot'] == 'lin_plot' and 'text_f' in user_data[message.chat.id]:
            Bot.send_message(message.chat.id, bot_text['read_f'], reply_markup=t_panel)
            Bot.register_next_step_handler(message, linear_plot_data)
        elif user_data[message.chat.id]['plot'] == 'bar_plot' and 'text_f' in user_data[message.chat.id]:
            Bot.send_message(message.chat.id, bot_text['read_f'], reply_markup=t_panel)
            Bot.register_next_step_handler(message, bar_plot_data)
    else:
        Bot.send_message(message.chat.id, bot_text['err_choice'], reply_markup=axis_panel)
        Bot.register_next_step_handler(message, axis_choice)


def input_axis(message):
    text = message.text
    try:
        x, y = text.split('\n')
        user_data[message.chat.id]['X_axis'] = x
        user_data[message.chat.id]['Y_axis'] = y
        if user_data[message.chat.id]['plot'] == 'lin_plot' and 'text_f' not in user_data[message.chat.id]:
            Bot.send_message(message.chat.id, bot_text['lin_input'], reply_markup=close_panel)
            Bot.register_next_step_handler(message, linear_plot_data)
        elif user_data[message.chat.id]['plot'] == 'bar_plot' and 'text_f' not in user_data[message.chat.id]:
            Bot.send_message(message.chat.id, bot_text['bar_input'], reply_markup=close_panel)
            Bot.register_next_step_handler(message, bar_plot_data)
        elif user_data[message.chat.id]['plot'] == 'lin_plot' and 'text_f' in user_data[message.chat.id]:
            Bot.send_message(message.chat.id, bot_text['read_f'], reply_markup=t_panel)
            Bot.register_next_step_handler(message, linear_plot_data)
        elif user_data[message.chat.id]['plot'] == 'bar_plot' and 'text_f' in user_data[message.chat.id]:
            Bot.send_message(message.chat.id, bot_text['read_f'], reply_markup=t_panel)
            Bot.register_next_step_handler(message, bar_plot_data)
    except ValueError:
        Bot.send_message(message.chat.id, bot_text['input_err'])


def linear_plot_data(message):
    if 'text_f' in user_data[message.chat.id]:
        text = user_data[message.chat.id]['text_f']
        Bot.send_message(message.chat.id, bot_text['read_data'], reply_markup=close_panel)
    else:
        text = message.text
    text = text.replace(',', '.')
    try:
        lines = text.split('\n')
        X = list()
        Y = list()
        for line in lines:
            x, y = list(map(float, line.split()))
            X.append(x)
            Y.append(y)
        linear_plot(message, X, Y, user_data[message.chat.id]['color'], user_data[message.chat.id]['X_axis'],
                    user_data[message.chat.id]['Y_axis'])
    except ValueError:
        Bot.send_message(message.chat.id, bot_text['input_err'])


def linear_plot(message, X, Y, color, xlabel, ylabel):
    plt.plot(X, Y, color=color, marker='o', markersize=5)
    plt.grid()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig('linearPlot.png')
    ph = open('linearPlot.png', 'rb')
    Bot.send_message(message.chat.id, 'График построен:')
    Bot.send_photo(message.chat.id, ph)
    plt.clf()
    ph.close()


def bar_plot_data(message):
    if 'text_f' in user_data[message.chat.id]:
        text = user_data[message.chat.id]['text_f']
        Bot.send_message(message.chat.id, bot_text['read_data'], reply_markup=close_panel)
    else:
        text = message.text
    text = text.replace(',', '.')
    try:
        lines = text.split('\n')
        X = list()
        Y = list()
        for line in lines:
            x, y = list(line.split())
            X.append(x)
            y = float(y)
            Y.append(y)
        bar_plot(message, X, Y, user_data[message.chat.id]['color'], user_data[message.chat.id]['X_axis'],
                 user_data[message.chat.id]['Y_axis'])
    except ValueError:
        Bot.send_message(message.chat.id, bot_text['input_err'])


def bar_plot(message, X, Y, color, xlabel, ylabel):
    plt.bar(X, Y, color=color, width=0.3, align='center', edgecolor='black', zorder=2)
    plt.grid()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig('barPlot.png')
    plot = open('barPlot.png', 'rb')
    Bot.send_message(message.chat.id, 'Диаграмма построена:')
    Bot.send_photo(message.chat.id, plot)
    plt.clf()
    plot.close()


def circle_plot_data(message):
    if 'text_f' in user_data[message.chat.id]:
        text = user_data[message.chat.id]['text_f']
        Bot.send_message(message.chat.id, bot_text['read_data'], reply_markup=close_panel)
    else:
        text = message.text
    text = text.replace(',', '.')
    try:
        lines = text.split('\n')
        X = list()
        Y = list()
        for line in lines:
            x, y = list(line.split())
            X.append(x)
            y = float(y)
            Y.append(y)
        circle_plot(message, X, Y)
    except ValueError:
        Bot.send_message(message.chat.id, bot_text['input_err'])


def circle_plot(message, X, Y):
    plt.pie(Y, labels=X, autopct='%1.1f%%', radius=1.4)
    plt.savefig('circlePlot.png')
    plot = open('circlePlot.png', 'rb')
    Bot.send_message(message.chat.id, 'Диаграмма построена:')
    Bot.send_photo(message.chat.id, plot)
    plt.clf()
    plot.close()


Bot.polling(non_stop=True)
