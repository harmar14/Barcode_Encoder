# -*- coding: cp1251 -*-

from sys import argv

def check_sequence(sequence):
    length = len(sequence)
    # ���������, ��� ������� ������������������ �� ������.
    if (length == 0):
        return False
    else:
        # ���������, ��� ��� ������� ������� ������������������ ���������.
        for symbol in sequence:
            ascii_code = ord(symbol)
            if (ascii_code < 32 or ascii_code > 126):
                return False
        return True

def add_checksum(data):
    # ������� ��������� ����������� � ��������� ���-�����.
    for idx in range(len(data)):
        symbol = ord(data[idx])
        if (symbol < 127):
            symbol -= 32
        else:
            symbol -= 100
        if (idx == 0):
            checksum = symbol
        checksum = (checksum + idx * symbol) % 103
    # ������ ������������� ���-�����.
    if (checksum < 95):
        checksum += 32
    else:
        checksum += 100
    # ���������� � ��������� ���-�����.
    data += chr(checksum)
    return data

def code_128_encoder(sequence):
    # ��������� ����� ������� ������������������.
    length = len(sequence)
    # ������������� ���� ������������� ������� B ��� �����������.
    table_b = True
    # ������������� ��������� ������.
    idx = 0
    # ��������� ���������, ���� �� ���������� ������������������ ��������.
    while (idx < length):
        # ��������� ���� ������������� ������� B.
        if (table_b):
            # ���������, ��������� �� � ������ ��� � ����� ������������������, ���� ���.
            if (idx == 0 or (idx + 3) == (length - 1)):
                mini = 4 # ���������� ��������� �������� = 4.
            else:
                mini = 6
            mini -= 1
            # ���������, ��� ����� ����������� ��������� <mini> �������� (�� ������� �� ������� ������������������).
            if ((idx + mini) <= length - 1):
                # ���������� �������.
                while not (mini < 0):
                    # ������� 0-9 ����� ���� 48-57. ���� ��������� �� �����, ���������.
                    if (ord(sequence[idx + mini]) < 48 or ord(sequence[idx + mini]) > 57):
                        break
                    mini -= 1
            # ���� mini < 0, ��������� � ������� C.
            if (mini < 0):
                # ���� ��������� �� ��������� �������, ����� ��������� ������ �� ������� C, ����� - ���������� � ���������� ��� C.
                if (idx == 0):
                    result = chr(205)
                else:
                    result += chr(199)
                table_b = False
            else:
                # ���� ��������� �� ��������� �������, ����� ��������� ������ �� ������� B.
                if (idx == 0):
                    result = chr(204)
        # ���������, ������� �� �� � ������� C.
        if not (table_b):
            # � Code128C ���������� ��������� �������� �������, ������� mini = 2.
            mini = 2
            mini -= 1
            # ���������, ��� �� ������� �� ������� ������������������.
            if (idx + mini < length):
                # ���������� �������.
                while not (mini < 0):
                    # ������� 0-9 ����� ���� 48-57. ���� ��������� �� �����, ���������.
                    if (ord(sequence[idx + mini]) < 48 or ord(sequence[idx + mini]) > 57):
                        break
                    mini -= 1
            # ���� mini < 0, ������ ��� ������� - �����. ������������ �� ������.
            if (mini < 0):
                pair = int(sequence[idx:(idx + 2)])
                if (pair < 95):
                    pair += 32
                else:
                    pair += 100
                result += chr(pair)
                idx += 2
            else:
                # ��� ������� - �� ��� �����, ������������ � ������� B.
                result += chr(200) # 200 - ��� B.
                table_b = True
        # ��������� ���� � ������, ���������� �� �� ������� B.
        if (table_b):
            # ���������� � ��������� ������ �������� ������������������ � ������� ��������.
            result += sequence[idx]
            idx += 1
    
    # �������� ���������� ���-����� � ���������� �� � ����������.
    result = add_checksum(result)
    # ��������� �������������� ������.
    result += chr(206)
    
    return result

def code_128(sequence):
    # ��������� �������� ������� ������������������.
    check = check_sequence(sequence)
    if not (check):
        return "Error: Invalid sequence provided."
    return code_128_encoder(sequence)

if __name__ == '__main__':
    _, dataToEncode = argv
    print(code_128(dataToEncode))