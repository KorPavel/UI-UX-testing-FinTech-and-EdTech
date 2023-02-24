from random import choice, randint
from string import punctuation, ascii_lowercase
from faker import Faker


__all__ = ['get_nums', 'letters_ru', 'letters_en', 'letters_cn', 'get_specsymbols',
           'valid_guest_data', 'various_mail', 'various_phone', 'MAIN_URL']

faker = Faker('ru_RU')
faker_pwd = Faker()

MAIN_URL = 'https://testinglove.ru/test'


def get_nums(count: int) -> str:
    """ Функция возвращает строку цифр длиной count символов """
    return ''.join([str(choice(range(10))) for _ in range(count)])


def letters_ru(count: int) -> str:
    """ Функция возвращает строку кириллицы длиной count символов """
    return ''.join(chr(randint(ord('а'), ord('я'))) for _ in range(count))


def letters_en(count: int) -> str:
    """ Функция возвращает строку латиницы длиной count символов """
    return ''.join(choice(ascii_lowercase) for _ in range(count))


def letters_cn(count: int) -> str:
    """ Функция возвращает строку китайских иероглифов длиной count символов """
    text_cn = '这些软软的法式包子多吃点喝点茶从架子上拿一个带钉子的馅饼好好享受你的饭吧别谢我'
    return ''.join(choice(text_cn) for _ in range(count))


def get_specsymbols(count: int) -> str:
    """ Функция возвращает строку спецсимволов длиной count знаков """
    return ''.join(choice(punctuation) for _ in range(count))


valid_guest_data = {'first_name': faker.first_name_male(),
                    'last_name': faker.last_name_male(),
                    'login': f'rtkid_{get_nums(13)}',
                    'email': faker.free_email(),
                    'phone': '+79' + get_nums(9),
                    'ls': get_nums(12),
                    'password': 'tEst1Ng%sIte_Rt',
                    'password_confirm': 'tEst1Ng%sIte_Rt'}


various_mail = ['',
                f'{letters_ru(10)}@email.com',
                f'email@{letters_ru(5)}.com',
                f'email@email.{letters_ru(3)}',
                f'{get_specsymbols(10)}@email.com',
                f'email@{get_specsymbols(5)}.com',
                f'email@email.{get_specsymbols(3)}',
                f'{letters_cn(10)}@email.com',
                f'email@{letters_cn(5)}.com',
                f'email@email.{letters_cn(3)}'
                ' @email.com',
                'email@ .com',
                'email@email com',
                'email@email. com',
                'email@e mail.com',
                'e mail@email.com',
                'email@email.c om']

various_phone = [letters_ru(11),
                 letters_en(11),
                 letters_cn(11),
                 get_specsymbols(11),
                 f'+7{letters_ru(10)}',
                 f'+7{letters_en(10)}',
                 f'+7{get_specsymbols(10)}',
                 f'+375{letters_ru(9)}',
                 f'+375{letters_en(9)}',
                 f'+375{get_specsymbols(9)}']



