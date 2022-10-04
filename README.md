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
-Получить рекомендацию фильма;
> На входе: название фильма;
> На выходе: список рекомендаций.
- Получить рекомендацию сериала;
> На входе: название сериала;
> На выходе: список рекомендаций.
- Получить рекомендацию игры;
> На входе: название игры;
> На выходе: список рекомендаций.
- Регистрация;
> На входе: данные для регистрации;
> На выходе: создается запись пользователя в БД.
- Авторизация;
> На входе: данные для авторизации;
> На выходе: пользователь авторизируется под своим 
аккаунтом.
- Выйти из учетной записи;
> На входе: данные авторизированного аккаунта;
> На выходе: пользователь выходит из своей учетной записи.
- Добавить в медиатеку;
> На входе: название контента;
> На выходе: в медиатеку добавляется контент.
- Загрузить данные;
> На входе: файл с данными;
> На выходе: файл попадает в список данных пользователя.
- Получить рекомендацию по загруженным данным.
> На входе: выбранный файл с данными;
> На выходе: пользователь получает рекомендацию.
