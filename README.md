# [Тестим](https://telegram-converter.onrender.com)

1) Подумать над двумя результатами (для голоса и для таблички);
2) Внешний вид;
3) Организовать модули:
4) 
OnlineSchoolHelper/
|-- app.py
|-- groups/
|   |-- __init__.py
|   |-- groups.py
|   |-- templates/
|       |-- groups/
|           |-- group_list.html
|           |-- group_view.html
|           |-- group_create.html
|-- students/
|   |-- __init__.py
|   |-- students.py
|   |-- templates/
|       |-- students/
|           |-- student_absent.html
|           |-- student_feedback.html
|           |-- student_result.html
|           |-- student_view.html
|-- feedback/
|   |-- __init__.py
|   |-- feedback.py
|   |-- templates/
|       |-- feedback/
|           |-- feedback.html
|           |-- feedback_result.html
|-- database/
|   |-- __init__.py
|   |-- operations.py
|-- messenger/
|   |-- __init__.py
|   |-- messanger.py
|   |-- templates/
|       |-- messenger/
|           |-- messenger.html
|-- utility.py

Придумать:

I. Логику для заполнения таблицы

1) Автоматический перенос текста в таблицу Excel
- Перенос имен в таблицу
- Перенос обратной связи в таблицу