from string import ascii_letters, digits

# получаем символы русского алфавита
rus_alphabet = ''.join([chr(i) for i in range(1040, 1104)])


# проверка - больше 30 и меньше 2 символов, название не может быть полностью числом,
# могут быть только русские и английские символы
def valid_name(name):
    try:
        assert int(name.strip())
        return False
    except:
        if 2 < len(name) < 30:
            for l in name:
                if not l in ascii_letters + digits + rus_alphabet + ' ':
                    return False
            return True
        else:
            return False


# проверка на количество участников и что введено было число
def check_team_count(count, m1, m2):
    try:
        if m1 <= int(count.strip()) <= m2:
            return True
        else:
            return False
    except:
        return False


# проверяем номер на правильность
def check_number(number):
    try:
        assert int(number.strip())
        if number.strip()[0] == '7' and len(number.strip()) == 11:
            return True
        else:
            return False
    except:
        return False




