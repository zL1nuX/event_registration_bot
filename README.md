# Телеграм-бот: Регистрация на мероприятия
[Полный отчет Google Docs](https://docs.google.com/document/d/1UQLBwBm9AHppeYlkQdm6kTh2bAcnRaMa/edit?usp=sharing&ouid=111124886044646232411&rtpof=true&sd=true)

# Паспорт проекта
## Цель
Создание Telegram-бота для регистрации участников мероприятия с возможностью уточнения дополнительной информации о нем и функцией прохождения теста на проверку знаний.
## Задачи
1. Создание стартового интерфейса (приветствие пользователя, «кнопки», отвечающие за функции бота).
2. Реализация функции регистрации команд: сбор информации с пользователя (название команды, количество человек в команде, ФИО участников, номер и почта капитана, учебное заведение).
3. Реализация автоматического переноса полученной информации в базу данных.
4. Реализация функции уточнения времени и места проведения мероприятия по запросу пользователя (вывод информации пользователю в удобном формате).
5. Реализация функции получения регламента проведения мероприятия по запросу пользователя.
6. Реализация функции прохождения теста на проверку знаний с получением вопросов и вариантов ответов (включая номер правильного) из базы данных.
7. Отладка бота, косметические правки (красивые кнопки, удобная навигация)
## План

| Запланировано | Отчет |
|----------|----------|
| Составить техзадание вместе с заказчиком | Обсудили, составили ТЗ, разделив требуемые функции по пунктам, определились с базой данных (вместо нее было решено использовать Google Sheets)   |
| Определиться с библиотекой python для написания бота    | Была выбрана библиотека pyTelegramBotAPI, у меня уже имеется работы с ней    |
| Написать код интерфейса (приветствие, кнопки) и протестировать запуск бота | Выполнено, были поставлены «кнопки-заглушки» с именами будущих функций, бот умеет приветствовать пользователя   |
| Придумать, как переносить информацию из бота в Google sheets | Найдено официальное API Google Sheets и документация к нему |
| Реализовать функцию регистрации команд, вызываемую одной из кнопок и последующий перенос данных в требуемую Google-таблицу | Выполнено, бот получает данные от пользователя, которые успешно появляются в таблице с помощью взаимодействия с Google Sheets API |
| Реализовать функцию вывода времени, места, и регламента проведения | Выполнено, время и место проведения отправляются в виде сообщения от бота, данные берутся из файла config.py. Отдельно отправляется файл регламента, находящийся в папке с ботом |
| Реализовать отправку изображения с картой места проведения | Дополнительно вместе с местом проведения отправляется изображение с фрагментом Яндекс.Карт с меткой в указанном месте, реализовано с помощью библиотеки yandex-geocoder и Yandex.Maps Static API |
| Добавить тест на проверку знаний | Реализовано с помощью Google Sheets API, вопросы берутся из таблицы, после прохождения теста бот присылает результат, полученный пользователем |
| Косметические улучшения | Изменены размеры кнопок, перенос строк в длинных вопросах теста, добавлена удобная навигация: кнопка «Домой» и кнопка «Назад» |
| Тестирование продукта, передача заказчику, исправление возможных ошибок | Бот работает исправно, были исправлены некоторые ошибки с запуском на другом компьютере, заказчик остался доволен, проект запущен для использования реальными пользователями |


## Requirements and used sources
Использовались документации библиотек yandex-geocoder, Gspread, pyTelegramBotAPI, а также документации API: Yandex.Maps StaticAPI и Google Sheets API.
Также использовал информацию из статей с habr.com, некоторые ошибки исправлял с помощью ответов на Stack Overflow.
