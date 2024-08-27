import telebot
from telebot import types

# Замените 'YOUR_TOKEN' на ваш реальный токен бота
bot = telebot.TeleBot('5820184297:AAEEpjyCO8N5iJV1L8TWJtCSlo37yZxx_QM')

# Отключаем вебхук, если он активен
bot.remove_webhook()

# Ваш chat_id, который нужно заменить на актуальный после получения
ADMIN_CHAT_ID = '424796989'

# Словарь с джерками и их ценами
jerks = {
    "куриные с паприкой": 130,
    "куриные с бастурмой": 130,
    "куриные карри": 130,
    "куриные чили": 130,
    "куриные с травами": 130,
    "куриные со смесью перцев": 130,
    "куриные 'под шашлык'": 130,
    "говядина с паприкой": 150,
    "говядина с бастурмой": 150,
    "говядина карри": 150,
    "говядина чили": 150,
    "говядина с травами": 150,
    "говядина со смесью перцев": 150,
    "говядина 'под шашлык'": 150,
    "свиные с паприкой": 150,
    "свиные с бастурмой": 150,
    "свиные карри": 150,
    "свиные чили": 150,
    "фирменные свиные": 200,
    "свиные со смесью перцев": 150,
    "свиные 'под шашлык'": 150,
    "кабаносы свиные": 250
}

# Значки для каждого вида
icons = {
    "куриные": "🐔",
    "говядина": "🐄",
    "свиные": "🐖",
    "кабаносы": "🐗"
}

# Корзина
cart = {}

# Состояния пользователя
USER_STATE = {}

# Функция для создания клавиатуры с джерками и корзиной
def create_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    items = []
    for jerk, price in jerks.items():
        icon = icons.get(get_meat_type(jerk), "")
        item = types.KeyboardButton(f"{icon} {jerk} ({price} грн.)")
        items.append(item)
    markup.add(*items)
    markup.add(types.KeyboardButton("Корзина"))
    return markup

# Функция для определения типа мяса по названию
def get_meat_type(jerk_name):
    if "куриные" in jerk_name:
        return "куриные"
    elif "говядина" in jerk_name:
        return "говядина"
    elif "свиные" in jerk_name or "кабаносы" in jerk_name:
        return "свиные"
    else:
        return "кабаносы"

# Функция для создания клавиатуры редактирования корзины
def create_cart_editing_menu():
    markup = types.InlineKeyboardMarkup()
    for jerk, quantity in cart.items():
        markup.add(
            types.InlineKeyboardButton(f"➕ {jerk}", callback_data=f'inc_{jerk}'),
            types.InlineKeyboardButton(f"➖ {jerk}", callback_data=f'dec_{jerk}'),
            types.InlineKeyboardButton(f"❌ {jerk}", callback_data=f'del_{jerk}')
        )
    markup.add(types.InlineKeyboardButton("Подтвердить заказ", callback_data='confirm_order'))
    return markup

# Функция для отображения корзины
def show_cart(message):
    text = "Ваша корзина:\n"
    total = 0
    for jerk, quantity in cart.items():
        price = jerks[jerk]
        text += f"- {jerk} x {quantity} = {price * quantity} грн.\n"
        total += price * quantity
    text += f"Итого: {total} грн."
    bot.send_message(message.chat.id, text, reply_markup=create_cart_editing_menu())

# Функция для сбора данных о доставке
def get_delivery_info(message):
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Введите ваши данные для доставки:\nНомер телефона:\nФИО:\nАдрес Новой Почты:\nКомментарий (опционально):", reply_markup=markup)
    USER_STATE[message.chat.id] = 'waiting_for_delivery_info'

# Функция для отправки данных заказа админу
def send_order_to_admin(order_text, chat_link):
    bot.send_message(ADMIN_CHAT_ID, f"{order_text}\n\nПользователь: {chat_link}")

# Функция для создания кнопки "Старт"
def create_start_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton("Старт")
    markup.add(start_button)
    return markup

# Обработчик команд
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Очищаем корзину и состояние пользователя при запуске
    cart.clear()
    USER_STATE[message.chat.id] = 'idle'
    bot.reply_to(message, "Добро пожаловать в наш магазин джерков!\n\nВот что мы предлагаем:\n\n🐔 Куриные джерки:\n- с паприкой: 130 грн.\n- с бастурмой: 130 грн.\n- карри: 130 грн.\n- чили: 130 грн.\n- с травами: 130 грн.\n- со смесью перцев: 130 грн.\n- 'под шашлык': 130 грн.\n\n🐄 Говядина:\n- с паприкой: 150 грн.\n- с бастурмой: 150 грн.\n- карри: 150 грн.\n- чили: 150 грн.\n- с травами: 150 грн.\n- со смесью перцев: 150 грн.\n- 'под шашлык': 150 грн.\n\n🐖 Свиные джерки:\n- с паприкой: 150 грн.\n- с бастурмой: 150 грн.\n- карри: 150 грн.\n- чили: 150 грн.\n- фирменные: 200 грн.\n- со смесью перцев: 150 грн.\n- 'под шашлык': 150 грн.\n\n🐗 Кабаносы свиные: 250 грн.\n\nВыберите джерк из меню ниже:", reply_markup=create_menu())

# Обработчик сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text

    if text == "Корзина":
        show_cart(message)
        return

    if text == "Старт":
        cart.clear()
        USER_STATE[message.chat.id] = 'idle'
        bot.send_message(message.chat.id, "Вы начали новый заказ. Пожалуйста, выберите джерк из меню ниже:", reply_markup=create_menu())
        return

    if message.chat.id in USER_STATE and USER_STATE[message.chat.id] == 'waiting_for_delivery_info':
        # Обработка реквизитов доставки
        delivery_info = text
        chat_link = f"https://t.me/{message.chat.username}" if message.chat.username else f"https://t.me/c/{message.chat.id}"
        order_text = f"Новый заказ от пользователя {message.chat.id}:\n\nДанные для доставки:\n{delivery_info}\n\nСостав заказа:\n"
        for jerk, quantity in cart.items():
            price = jerks[jerk]
            order_text += f"- {jerk} x {quantity} = {price * quantity} грн.\n"
        send_order_to_admin(order_text, chat_link)
        bot.send_message(message.chat.id, "Спасибо! Ваш заказ был отправлен. Мы свяжемся с вами для подтверждения.", reply_markup=create_start_button())
        USER_STATE[message.chat.id] = 'idle'
        return

    try:
        parts = text.split(' (')
        if len(parts) > 1:
            selected_jerk = parts[0].split(' ', 1)[1]  # Извлекаем название джерка без значка и цены
        else:
            selected_jerk = text.split(' ', 1)[1]  # Если не нашли цену, пробуем без нее
    except IndexError:
        bot.send_message(message.chat.id, "Не удалось распознать ваш выбор. Пожалуйста, выберите джерк из меню.")
        return

    if selected_jerk in jerks:
        if selected_jerk not in cart:
            cart[selected_jerk] = 1
        else:
            cart[selected_jerk] += 1
        bot.send_message(message.chat.id, f"Джерк '{selected_jerk}' добавлен в корзину.", reply_markup=create_menu())
    else:
        bot.send_message(message.chat.id, "Не удалось распознать ваш выбор. Пожалуйста, выберите джерк из меню.")

# Обработчик кнопок редактирования корзины
@bot.callback_query_handler(lambda call: call.data.startswith(('inc_', 'dec_', 'del_', 'confirm_order')))
def callback_edit_cart(call):
    if call.data.startswith('inc_'):
        jerk = call.data[4:]
        if jerk in cart:
            cart[jerk] += 1
    elif call.data.startswith('dec_'):
        jerk = call.data[4:]
        if cart[jerk] > 1:
            cart[jerk] -= 1
        else:
            del cart[jerk]
    elif call.data.startswith('del_'):
        jerk = call.data[4:]
        if jerk in cart:
            del cart[jerk]
    elif call.data == 'confirm_order':
        bot.send_message(call.message.chat.id, "Пожалуйста, введите ваши данные для доставки:", reply_markup=types.ReplyKeyboardRemove())
        USER_STATE[call.message.chat.id] = 'waiting_for_delivery_info'
        return

    # Проверка, изменилось ли сообщение
    cart_text = "Ваша корзина обновлена:\n"
    total = 0
    for jerk, quantity in cart.items():
        price = jerks[jerk]
        cart_text += f"- {jerk} x {quantity} = {price * quantity} грн.\n"
        total += price * quantity
    cart_text += f"Итого: {total} грн."

    if call.message.text != cart_text or call.message.reply_markup != create_cart_editing_menu():
        bot.edit_message_text(cart_text, call.message.chat.id, call.message.message_id, reply_markup=create_cart_editing_menu())

# Запуск бота
bot.polling()
