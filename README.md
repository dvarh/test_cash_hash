# Тестовое задание

Написать сервис на python2.7
Сервис имеет один endpoint:

```GET /from_cache?key="some key"
```


который возвращает значение получаемое от стороннего сервиса :

Значение нужно закешировать и вернуть пользователю. 
При этом клиент ждет ответа не более 1 сек (после этого он отвалится по таймауту),
но может перезапрашивать значение несколько раз. Так как сервис довольно медленный, 
и может отвечать с ошибками (error - это ошибка которую не нужно кешировать),
желательно свести количество обращений к нему к минимуму. 
Значение из кеша должно быть не старше 24 часов. 
Сервис не должен пятисотить или падать.

## Installation

1. `git clone https://github.com/dvarh/test_cash_hash.git`

2. `cd test_cash_hash`

3. `pip install -r requirements.txt`

4. `python manage.py runserver`

5. http://127.0.0.1:8000 /from_cache?key="some key"

## License

MIT