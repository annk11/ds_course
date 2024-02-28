riddle = []
riddle1 = ['Какая версия языка сейчас актуальна?', 'Python3']
riddle2 = ['Какая кодировка используется в строках?', 'UTF8']
riddle3 = ['Сколько значений есть у bool?', '2']
riddle4 = ['В условии If может быть выражение, которое возвращает True/False?', 'Да']
riddle5 = ['Что такое bytes?', 'Тип данных']
riddle6 = ['Что такое while?', 'Цикл']
riddle7 = ['Можно ли складывать строки?', 'Да']
riddle8 = ['Можно ли вычитать строки?', 'Нет']
riddle9 = ['Нужно ли ставить пробелы после условия?', 'Да']
riddle10 = ['Соединение двух строк в единую строку - это ...?', 'Конкатинация']
riddle.append(riddle1)
riddle.append(riddle2)
riddle.append(riddle3)
riddle.append(riddle4)
riddle.append(riddle5)
riddle.append(riddle6)
riddle.append(riddle7)
riddle.append(riddle8)
riddle.append(riddle9)
riddle.append(riddle10)

great_ans = 0

for i in riddle:
    user_answer = input(f'Введите ответ на вопрос: {i[0]} - ')
    if user_answer.lower() == i[1].lower():
        print('Ответ "{0}" верен!'.format(user_answer))
        great_ans = great_ans + 1
    else:
        print('Неверный ответ!')
print('Количество верных ответов:', great_ans, 'из 10')