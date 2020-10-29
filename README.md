# bitly-links
Скрипт позволяет посредством [API сервиса bit-ly](https://bitly.com/) формировать короткую ссылку и получать
статистику переходов по ней.

## Установка:
1. Скопируйте файл.
2. Сгенерируйте токен [bit.ly](https://bitly.com/a/oauth_apps).
3. В папке, где расположен скрипт создайте файл **.env** и поместите в него сгенерированный
токен, добавив в файл следующую строку:
    >**TOKEN = ваш_токен**
4. Выполните команду, чтобы установить необходимые для работы скрипта библиотеки
    >**pip install -r requirements.txt**  
Скрипт готов к использованию!

## Использование:
1. Запустите скрипт выполнив в командной строке.
    >**$ python bitly-links.py**
2. Введите URL статистику переходов по которому хотите отслеживать. Например:
    >**https://google.com**
3. Получите короткую ссылку формата:
    >**https://bitly.com/1111**
4. Разместите короткую ссылку.
5. Чтобы получить статистику переходов по короткой ссылке, запустите скрипт и введите ссылку формата
    >**https://bitly.com/1111>**
