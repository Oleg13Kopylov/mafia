# Приложение для игры в мафию

Сетевой вариант игры "Мафия". Взаимодействие между клиентом и сервером обеспечивается с помощью gRPC.
В одном сеансе игры – 4 игрока: мафия, комиссар, два мирных жителя.

**Условия для победы мирных жителей: мафия была убита.**

**Условия для победы мафии: игроков-мафий не меньше, чем игроков, 
которые не являются мафией.**


## Как запускать
Открыть пять окон в терминале. В одном окне нужно запустить сервер,
в остальных четырех – клиентов. Как это сделать – описано в разделе _Команды для запуска_.

### Замечание
Если запускаете с macbook, то следует оставить python3, как в командах ниже. 
Иначе надо заменить python3 на python.

### Команды для запуска
1.  ```cd kopylov-mafia```
2. ```python3 -m pip install --upgrade pip && virtualenv venv```
3Запуск сервера: ```(venv) kopylov-mafia %python -m pip install --upgrade pip && python3 
-m pip install grpcio && python3 server.py```
или запуск клиента: ```(venv) kopylov-mafia %python -m pip install --upgrade pip && python3 
-m pip install grpcio && python3 client.py```