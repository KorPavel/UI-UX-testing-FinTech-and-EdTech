import pytest
from pages.main_page import MainPage
from pages.basket_page import BasketPage
from settings import valid_guest_data, various_mail, get_nums, get_specsymbols, letters_ru, letters_en, letters_cn


class TestMainPage:
    """ Тест-кейсы для ГЛАВНОЙ СТРАНИЦЫ сайта. """

    @pytest.mark.positive
    def test_guest_should_see_basic_elements(self, browser):
        """ Тест-кейс гость проверяет наличие основных элементов на главной странице. """
        page = MainPage(browser)
        page.open()
        page.should_be_name_of_tour()
        elements_tour_info = ['40000 рублей', '15 дней', 'Средний', '92 километра', 'Хайкинг, пересечение рек',
                              'Кутаиси / Батуми', 'Цена тура 40000 рублей', 'Дополнительные расходы']
        page.should_be_basic_content(elements_tour_info)
        page.checking_buy_button_click()
        page.check_social_link()

    @pytest.mark.positive
    @pytest.mark.xfail(reason='БАГ!!! Ссылки на соцсети не работают.')
    def test_get_in_touch_with_us(self, browser):
        page = MainPage(browser)
        page.open()
        page.check_sociallinks_item()

    @pytest.mark.positive
    def test_checking_drop_down_menu_logo_and_button(self, browser):
        """ Проверка логотипа и кнопки "Забронировать тур" в раскрывающемся меню. """
        page = MainPage(browser)
        page.open()
        page.check_logo()
        page.check_menu_button()

    @pytest.mark.positive
    @pytest.mark.xfail(reason='БАГИ!!! Из 5 кнопок, рабочая только одна - "КОНТАКТЫ"')
    def test_checking_drop_down_menu_items(self, browser):
        """ Проверка действия ссылок пунктов в раскрывающемся меню. """
        page = MainPage(browser)
        page.open()
        page.check_menu_elements()

    @pytest.mark.manual(reason='Требуется участие человека для ввода капча')
    @pytest.mark.positive
    def test_book_a_tour_good(self, browser):
        """ Позитивный тест-кейс. Пользователь заполняет поля формы "Забронировать тур"
        Ваша почта и Ваше имя валидными значениями """
        page = MainPage(browser)
        page.open()
        page.send_params_to_fields(valid_guest_data['email'], valid_guest_data['first_name'])

    @pytest.mark.xfail(reason='4 из 16 некорректных email система принимает')
    @pytest.mark.negative
    @pytest.mark.parametrize('email', various_mail, ids='{}'.format)
    def test_book_a_tour_email_bad(self, browser, email):
        """ Негативный тест-кейс. Пользователь заполняет поле Ваша почта формы "Забронировать тур"
        некорректными значениями. """
        page = MainPage(browser)
        page.open()
        page.send_params_to_fields(email, '', False)

    @pytest.mark.negative
    @pytest.mark.parametrize('name', ['', get_nums(8), get_specsymbols(8)], ids='{}'.format)
    def test_book_a_tour_name_bad(self, browser, name):
        """ Негативный тест-кейс. Пользователь заполняет поле Ваше имя формы "Забронировать тур"
        некорректными значениями. """
        page = MainPage(browser)
        page.open()
        page.send_params_to_fields('', name, False)

    @pytest.mark.positive
    def test_check_first_day_photo_forward(self, browser):
        """ Проверка смены фотографий из блока первого дня при нажатии на клавишу ВПРАВО,
        и проверка, что количество уникальных фотографий соответствует количеству точек. """
        page = MainPage(browser)
        page.open()
        page.check_forward_button_on_first_day_photos()

    @pytest.mark.positive
    def test_check_first_day_photo_backward(self, browser):
        """ Проверка смены фотографий из блока первого дня при нажатии на клавишу ВЛЕВО. """
        page = MainPage(browser)
        page.open()
        page.check_backward_button_on_first_day_photos()

    @pytest.mark.positive
    def test_check_second_day_photo_forward(self, browser):
        """ Проверка смены фотографий из блока второго дня при нажатии на клавишу ВПРАВО,
        и проверка, что количество уникальных фотографий соответствует количеству точек. """
        page = MainPage(browser)
        page.open()
        page.check_forward_button_on_second_day_photos()

    @pytest.mark.positive
    def test_check_second_day_photo_backward(self, browser):
        """ Проверка смены фотографий из блока второго дня при нажатии на клавишу ВЛЕВО. """
        page = MainPage(browser)
        page.open()
        page.check_backward_button_on_second_day_photos()

    @pytest.mark.proba
    def test_check_block_photos(self, browser):
        """ Проверка уникальности фотографий в блоке на главной странице и соответствие их в зумном просмотре. """
        page = MainPage(browser)
        page.open()
        photos_list = page.check_block_photos()
        zoom_list = page.check_zoom_photos()
        assert photos_list == zoom_list, 'Списки фотографий не совпадают'


class TestBasket:
    """ Тест-кейсы для страницы КОРЗИНА ТОВАРОВ. """

    def go_to_buy(self, browser):
        """ Переход на страницу КОРЗИНА. Функция берёт с главной страницы
        актуальную цену товара и передаёт её в корзину для сравнения. """
        page = MainPage(browser)
        page.open()
        self.price_tour = page.click_on_buy()

    @pytest.mark.positive
    def test_should_be_basic_elements_in_basket(self, browser):
        """ Проверка основных элементов на странице КОРЗИНА. """
        self.go_to_buy(browser)
        basket = BasketPage(browser, browser.current_url)
        basket.should_be_basic_elements()

    @pytest.mark.positive
    def test_product_counter_operation_plus(self, browser):
        """ Проверка действия кнопки "+" (увеличить количество товара). """
        self.go_to_buy(browser)
        basket = BasketPage(browser, browser.current_url)
        basket.product_counter_operation_plus(self.price_tour)

    @pytest.mark.positive
    def test_product_counter_operation_minus(self, browser):
        """ Проверка действия кнопки "-" (уменьшить количество товара). """
        self.go_to_buy(browser)
        basket = BasketPage(browser, browser.current_url)
        basket.product_counter_operation_minus(self.price_tour)

    @pytest.mark.positive
    @pytest.mark.parametrize('num', [2, 5, 10])
    def test_product_counter_operation_manual_input(self, browser, num):
        """ Проверка ввода количества товара вручную. """
        self.go_to_buy(browser)
        basket = BasketPage(browser, browser.current_url)
        basket.product_counter_operation_manual_input(self.price_tour, get_nums(num))

    @pytest.mark.positive
    @pytest.mark.manual(reason='Требуется участие человека для ввода капча')
    def test_buy_a_tour_good(self, browser):
        """ Позитивный тест-кейс. Пользователь заполняет поля формы "Покупка тура" валидными значениями. """
        self.go_to_buy(browser)
        basket = BasketPage(browser, browser.current_url)
        basket.send_params_to_fields(valid_guest_data['first_name'],
                                     valid_guest_data['email'],
                                     valid_guest_data['phone'])

    @pytest.mark.negative
    @pytest.mark.parametrize('name', ['', 14, '$', '58'], ids='{}'.format)
    def test_buy_a_tour_name_bad(self, browser, name):
        """ Негативный тест-кейс. Пользователь заполняет поле для ввода ИМЕНИ формы "Покупка тура"
        некорректными значениями, остальные поля - корректные значения. """
        self.go_to_buy(browser)
        basket = BasketPage(browser, browser.current_url)
        basket.send_params_to_fields(name, valid_guest_data['email'], valid_guest_data['phone'], False)

    @pytest.mark.negative
    @pytest.mark.xfail(reason='4 из 16 некорректных email система принимает')
    @pytest.mark.parametrize('email', various_mail, ids='{}'.format)
    def test_buy_a_tour_email_bad(self, browser, email):
        """ Негативный тест-кейс. Пользователь заполняет поле для ввода EMAIL формы "Покупка тура"
        некорректными значениями, остальные поля - корректные значения. """
        self.go_to_buy(browser)
        basket = BasketPage(browser, browser.current_url)
        basket.send_params_to_fields(valid_guest_data['first_name'], email, valid_guest_data['phone'], False)

    @pytest.mark.negative
    @pytest.mark.parametrize('phone', ['', letters_ru(10), letters_en(10), letters_cn(10), get_specsymbols(10)],
                             ids='{}'.format)
    def test_buy_a_tour_phone_bad(self, browser, phone):
        """ Негативный тест-кейс. Пользователь заполняет поле для ввода НОМЕРА ТЕЛЕФОНА формы "Покупка тура"
        некорректными значениями, остальные поля - корректные значения. """
        self.go_to_buy(browser)
        basket = BasketPage(browser, browser.current_url)
        basket.send_params_to_fields(valid_guest_data['first_name'], valid_guest_data['email'], phone, False)

