# Audio_telegram_bot
Данный бот представляет собой библиотеку песен отправленных в бота. В нем есть возможность получать топ песен исполнителя, песни из альбома или все имеющиеся песни.

Управлять ботом можно как из меню так и отправив имя исполнителя боту. Если исполнитель присутствует в списке, то бот отправит меню исполнителя.

Для получения информации об исполнителе, альбоме и песне используется API last.fm. Соответственно чтобы бот работал необходимо ввести ключ полученный на сайте https://www.last.fm/api.

Для добавления песен в бота, рекомендую создать отдельный приватный канал и загружать всю музыку туда. Если вы решите загружать песни напрямую в бот, то вы не сможете использовать их потом в другом боте, даже зная идентификатор. В этом случае, при отправке песни, телеграм будет ругаться и пропускать этот файл.

Создавая этого бота я начинал изучать Python, поэтому даже я могу найти в этом коде много косяков или пользоваться другим функционалом языка для достижения тех же целей.

Постепенно постараюсь добавлять описание и комментарии в коде.

Скриншоты бота:

Главное меню:

![alt text](https://github.com/baddll/Audio_telegram_bot/blob/master/screenshorts/%D0%98%D1%81%D0%BF%D0%BE%D0%BB%D0%BD%D0%B8%D1%82%D0%B5%D0%BB%D0%B8.PNG)

Меню исполнителя:

![alt text](https://github.com/baddll/Audio_telegram_bot/blob/master/screenshorts/%D0%9C%D0%B5%D0%BD%D1%8E%20%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D0%BD%D0%B8%D1%82%D0%B5%D0%BB%D1%8F.PNG)

Меню выбора альбома:

![alt text](https://github.com/baddll/Audio_telegram_bot/blob/master/screenshorts/%D0%90%D0%BB%D1%8C%D0%B1%D0%BE%D0%BC%D1%8B%20%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D0%BD%D0%B8%D1%82%D0%B5%D0%BB%D1%8F.PNG)

После выбора альбома:

![alt text](https://github.com/baddll/Audio_telegram_bot/blob/master/screenshorts/%D0%9F%D0%B5%D1%81%D0%BD%D0%B8%20%D0%B8%D0%B7%20%D0%B0%D0%BB%D1%8C%D0%B1%D0%BE%D0%BC%D0%B0%201.PNG)

![alt text](https://github.com/baddll/Audio_telegram_bot/blob/master/screenshorts/%D0%9F%D0%B5%D1%81%D0%BD%D0%B8%20%D0%B8%D0%B7%20%D0%B0%D0%BB%D1%8C%D0%B1%D0%BE%D0%BC%D0%B0%202.PNG)

Меню топ-песен:

![alt text](https://github.com/baddll/Audio_telegram_bot/blob/master/screenshorts/%D0%A2%D0%BE%D0%BF.PNG?raw=true)
