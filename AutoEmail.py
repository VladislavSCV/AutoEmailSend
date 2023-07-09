import telebot
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time
from telebot import types


bot = telebot.TeleBot("6352338175:AAGygUKngPtJMhyWvg9C45nAXSwfkSHLqxs")
emailTEXT = ""
emails = []

userEmail = ""
userPassw = ""


print("Bot start work!!!")


@bot.message_handler(content_types=['text'])
def main(message):
    if message.text == "/command1":
        bot.send_message(message.from_user.id, "Окей, начнем!")
        print(1)
        time.sleep(1)
        bot.send_message(message.from_user.id, "Введите email пользователей через запятую!")
        bot.register_next_step_handler(message, emailUsers)

    elif message.text == "/command5":
        bot.send_message(message.from_user.id, "Хорошо, я рад, что вы решили использовать свой аккаунт!")
        time.sleep(1)
        bot.send_message(message.from_user.id, "Введите свой логин от аккаунта в email")
        bot.register_next_step_handler(message, CustomUserEmailLogin)


    elif message.text == "/start":
        bot.send_message(message.from_user.id, "Hello, World! Я бот для массовой рассылки email! Вы можете ознакомиться с моими функциями в меню.")


    elif message.text == "/command2":
        global emails
        emails = []
        bot.send_message(message.from_user.id, "Список пользователей был стерт.")

    elif message.text == "/command3":
        if emails == []:
            bot.send_message(message.from_user.id, "Список пуст.")
        else:
            for one_email in emails:
                bot.send_message(message.from_user.id, one_email)
            else:
                bot.send_message(message.from_user.id, "Список закончен.")

    elif message.text == "/command4":
        bot.send_message(message.from_user.id, "Привет!\nЯ бот для рассылки сообщений по email. \nЯ могу отправить сообщение с ващего email адреса или могу отправить сообщение с default email адреса! \nТак же вы можете заглянуть в меню. Тут вы найдете все мои функции)")        


def CustomUserEmailLogin(message):
    global userEmail
    bot.send_message(message.from_user.id, "Введите свой пароль от аккаунта в email")
    userEmail += str(message.text)
    print(userEmail)
    bot.register_next_step_handler(message, CustomUserEmailPassword)


def CustomUserEmailPassword(message):
    global userPassw
    bot.send_message(message.from_user.id, "Введите email пользователей через запятую!")
    userPassw += str(message.text)
    print(userPassw)
    bot.register_next_step_handler(message, emailUsers)


def emailUsers(message):
    global emails
    try:
        # Дело в том что когда пользователь доходит до этой функции бот ждет дополнительного ввода
        emails = message.text.split(",")
        bot.send_message(message.from_user.id, "Обработка прошла успешно, введите 'Ок' для продолжения...")
        print(2,"Проблемная область")
        bot.register_next_step_handler(message, confirm)
    except:
        bot.send_message(message.from_user.id, "Произошла какая-то ошибка(")


def confirm(message):
    print(3)
    bot.send_message(message.from_user.id, """Уважаемые пользователи,

Мы хотели бы обратить ваше внимание на важное правило нашей электронной почты: соблюдение этикета и избегание спама. 

Спам может быть определен различными способами, но кратко говоря, это нежелательные, неперсонализированные или массовые сообщения, которые могут нарушать работу и производительность электронной почты.

Пожалуйста, учтите следующие правила:
1. Используйте электронную почту только для личной или деловой переписки, в соответствии с ее назначением.
2. Не отправляйте массовые или нежелательные сообщения получателям, которые не просили их получать.
3. Избегайте перенаправления или копирования сообщений без разрешения отправителя.
4. Будьте внимательны при использовании функции "ответить всем" и убедитесь, что все получатели действительно нуждаются в этой информации.
5. Не рассылайте рекламные или спам-ссылки через электронную почту.\nЕсли вы принимаете согласие, то введите 'Ок'""")
    if message.text == "Ок":
        print(4)
        bot.register_next_step_handler(message, count_message_Email)
    else:
        bot.send_message(message.from_user.id, "Введите 'Ок' для продолжения работы!")



def count_message_Email(message):
    global emailTEXT
    print(5)
    bot.send_message(message.from_user.id, "Введите сообщение!")
    print(6)
    emailTEXT = message.text
    bot.register_next_step_handler(message, sendEmail)


def sendEmail(message):
    try:
        global emails
        messageForUsers = message.text
        print("Готово")
        for email in emails:
            from_email = userEmail or 'vladnety134@gmail.com' 
            to_email = email
            password = userPassw or 'vmdwzvemfpjfqlwm'

            msg = MIMEText(messageForUsers, 'plain', 'utf-8')

            smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_server.starttls()
            smtp_server.login(from_email, password)

            smtp_server.sendmail(from_email, to_email, msg.as_string())
            smtp_server.quit()

        bot.send_message(message.from_user.id, "ГОТОВО! Email сообщения были отправлены.")
    except:
        bot.send_message(message.from_user.id, "Произошла какая то ошибка! Проверьте пожалуйста правильность ввода(")
if __name__ == '__main__':
    bot.polling()