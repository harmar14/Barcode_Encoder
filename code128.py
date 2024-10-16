# -*- coding: cp1251 -*-

from sys import argv

def check_sequence(sequence):
    length = len(sequence)
    # Проверяем, что входная последовательность не пустая.
    if (length == 0):
        return False
    else:
        # Проверяем, что все символы входной последовательности допустимы.
        for symbol in sequence:
            ascii_code = ord(symbol)
            if (ascii_code < 32 or ascii_code > 126):
                return False
        return True

def add_checksum(data):
    # Обходим результат кодирования и вычисляем чек-сумму.
    for idx in range(len(data)):
        symbol = ord(data[idx])
        if (symbol < 127):
            symbol -= 32
        else:
            symbol -= 100
        if (idx == 0):
            checksum = symbol
        checksum = (checksum + idx * symbol) % 103
    # Делаем постобработку чек-суммы.
    if (checksum < 95):
        checksum += 32
    else:
        checksum += 100
    # Дописываем в результат чек-сумму.
    data += chr(checksum)
    return data

def code_128_encoder(sequence):
    # Посчитаем длину входной последовательности.
    length = len(sequence)
    # Устанавливаем флаг использования таблицы B для кодирования.
    table_b = True
    # Устанавливаем начальный индекс.
    idx = 0
    # Выполняем обработку, пока не закончится последовательность символов.
    while (idx < length):
        # Проверяем флаг использования таблицы B.
        if (table_b):
            # Проверяем, находимся мы в начале или в конце последовательности, либо нет.
            if (idx == 0 or (idx + 3) == (length - 1)):
                mini = 4 # Количество следующих символов = 4.
            else:
                mini = 6
            mini -= 1
            # Проверяем, что можем рассмотреть следующие <mini> символов (не выходим за пределы последовательности).
            if ((idx + mini) <= length - 1):
                # Перебираем символы.
                while not (mini < 0):
                    # Символы 0-9 имеют коды 48-57. Если встречаем не число, прерываем.
                    if (ord(sequence[idx + mini]) < 48 or ord(sequence[idx + mini]) > 57):
                        break
                    mini -= 1
            # Если mini < 0, переходим к таблице C.
            if (mini < 0):
                # Если находимся на начальной позиции, берем стартовый символ по таблице C, иначе - прибавляем к результату код C.
                if (idx == 0):
                    result = chr(205)
                else:
                    result += chr(199)
                table_b = False
            else:
                # Если находимся на начальной позиции, берем стартовый символ по таблице B.
                if (idx == 0):
                    result = chr(204)
        # Проверяем, перешли ли мы к таблице C.
        if not (table_b):
            # В Code128C происходит обработка символов попарно, поэтому mini = 2.
            mini = 2
            mini -= 1
            # Проверяем, что не выходим за пределы последовательности.
            if (idx + mini < length):
                # Перебираем символы.
                while not (mini < 0):
                    # Символы 0-9 имеют коды 48-57. Если встречаем не число, прерываем.
                    if (ord(sequence[idx + mini]) < 48 or ord(sequence[idx + mini]) > 57):
                        break
                    mini -= 1
            # Если mini < 0, значит два символа - цифры. Обрабатываем их вместе.
            if (mini < 0):
                pair = int(sequence[idx:(idx + 2)])
                if (pair < 95):
                    pair += 32
                else:
                    pair += 100
                result += chr(pair)
                idx += 2
            else:
                # Два символа - не две цифры, возвращаемся к таблице B.
                result += chr(200) # 200 - код B.
                table_b = True
        # Проверяем флаг и узнаем, используем ли мы таблицу B.
        if (table_b):
            # Дописываем в результат символ исходной последовательности с текущим индексом.
            result += sequence[idx]
            idx += 1
    
    # Вызываем вычисление чек-суммы и добавление ее к результату.
    result = add_checksum(result)
    # Добавляем заключительный символ.
    result += chr(206)
    
    # Постобработка на случай, если в результате есть пробелы.
    result.replace(' ', chr(194))
    
    return result

def code_128(sequence):
    # Выполняем проверку входной последовательности.
    check = check_sequence(sequence)
    if not (check):
        return "Error: Invalid sequence provided."
    return code_128_encoder(sequence)

if __name__ == '__main__':
    _, data = argv
    print(code_128(data))
