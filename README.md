# media-content-recommendation-system

Система подразумевает три вида пользователей: авторизированный 
пользователь, неавторизированный пользователь и администратор.
Администратор обладает правами на изменение, прочтение, добавление 
или удаление данных из базы данных.
Неавторизированный пользователь обладает возможностью получить 
рекомендацию в одной из трех сфер (кино, сериалы, игры).
Авторизированный пользователь помимо возможностей 
неавторизированного пользователя, имеет возможность добавлять контент в 
медиатеку тем самым управлять результатом рекомендации (добавленный в 
медиатеку контент не будет показываться в рекомендациях), а также загружать 
собственные наборы данных для получения рекомендации.
В качестве функциональных требований выступают:
• Получить рекомендацию фильма;
o На входе: название фильма;
o На выходе: список рекомендаций.
• Получить рекомендацию сериала;
o На входе: название сериала;
o На выходе: список рекомендаций.
• Получить рекомендацию игры;
o На входе: название игры;
o На выходе: список рекомендаций.
• Регистрация;
o На входе: данные для регистрации;
o На выходе: создается запись пользователя в БД.
• Авторизация;
o На входе: данные для авторизации;
o На выходе: пользователь авторизируется под своим 
аккаунтом.
• Выйти из учетной записи;
o На входе: данные авторизированного аккаунта;
o На выходе: пользователь выходит из своей учетной записи.
• Добавить в медиатеку;
o На входе: название контента;
o На выходе: в медиатеку добавляется контент.
• Загрузить данные;
o На входе: файл с данными;
o На выходе: файл попадает в список данных пользователя.
• Получить рекомендацию по загруженным данным.
o На входе: выбранный файл с данными;
o На выходе: пользователь получает рекомендацию
_____________________________________________________
