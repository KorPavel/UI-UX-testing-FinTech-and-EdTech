from .base_page import BasePage
from .locators import MainPageLocators
from selenium.webdriver.support import expected_conditions as EC
from settings import MAIN_URL
from time import sleep
from pprint import pprint


class MainPage(BasePage):

    def click_on_buy(self):
        """ Метод для перехода на страницу корзины, при этом запомнив рекламную цену продукта. """
        buy_button = self.wait.until(EC.presence_of_element_located(MainPageLocators.BUY_BUTTON))
        self.browser.execute_script("return arguments[0].scrollIntoView(false);", buy_button)
        sleep(0.5)
        new_price = self.wait.until(EC.presence_of_element_located(MainPageLocators.NEW_PRICE))
        price_tour = int(new_price.text)
        # print(f'\nprice_tour = {price_tour}, type = {type(price_tour)}')
        buy_button.click()
        return price_tour

    def should_be_name_of_tour(self):
        """ Метод проверяет название тура. """
        assert self.wait.until(
            EC.text_to_be_present_in_element(MainPageLocators.NAME_TOUR,
                                             'ЗАХВАТЫВАЮЩИЙ ТУР ПО ГРУЗИИ'))

    def should_be_basic_content(self, elements: list):
        """ Метод проверяет наличие основных элементов главной страницы. """
        tour_info = self.wait.until(EC.presence_of_all_elements_located(MainPageLocators.TOUR_INFO))
        self.checking_the_selected_elements_in_the_main_content(tour_info, elements)

    def check_social_link(self):
        """ Метод проверяет возможность авторизации пользователя через социальные сети ВКонтакте и Твиттер. """
        vk_link = self.wait.until(EC.presence_of_element_located(MainPageLocators.VK_LINK))
        twitter_link = self.wait.until(EC.presence_of_element_located(MainPageLocators.TWITTER_LINK))
        self.browser.execute_script("return arguments[0].scrollIntoView(true);", vk_link)
        assert 'vk.com' in vk_link.get_attribute('href')
        assert 'twitter.com' in twitter_link.get_attribute('href')
        assert self.wait.until(EC.element_to_be_clickable(MainPageLocators.VK_LINK))
        assert self.wait.until(EC.element_to_be_clickable(MainPageLocators.TWITTER_LINK))

    def check_sociallinks_item(self):
        """ Метод проверяет возможность связи с менеджерами сайта через
        ярлыки соцсетей: Твиттер, ВКонтакте, Телеграм. """
        links = self.wait.until(EC.presence_of_element_located(MainPageLocators.SOCIALLINKS))
        self.browser.execute_script("return arguments[0].scrollIntoView(true);", links)
        sociallinks = self.wait.until(EC.presence_of_all_elements_located(MainPageLocators.SOCIALLINKS))
        assert 'twitter.com' in sociallinks[0].get_attribute('href')
        assert 'vk.com' in sociallinks[1].get_attribute('href')
        assert 'telegram.com' in sociallinks[2].get_attribute('href')

    def scroll_to_block_photos(self):
        """ Метод скроллит страницу сайта до блока фотографий. """
        bp = self.wait.until(EC.presence_of_element_located(MainPageLocators.BLOCK_PHOTOS))
        self.browser.execute_script("return arguments[0].scrollIntoView(false);", bp)

    def scroll_to_bron(self):
        """ Метод скроллит страницу сайта до блока бронирования тура. """
        bron_tour = self.wait.until(EC.presence_of_element_located(MainPageLocators.BRON_TOUR))
        self.browser.execute_script("return arguments[0].scrollIntoView(true);", bron_tour)

    def scroll_to_first_day_photos(self):
        """ Метод скроллит страницу сайта до блока фотографий первого дня тура. """
        points = self.wait.until(EC.presence_of_element_located(MainPageLocators.POINTS1))
        self.browser.execute_script("return arguments[0].scrollIntoView(true);", points)

    def scroll_to_second_day_photos(self):
        """ Метод скроллит страницу сайта до блока фотографий второго дня тура. """
        points = self.wait.until(EC.presence_of_element_located(MainPageLocators.POINTS2))
        self.browser.execute_script("return arguments[0].scrollIntoView(true);", points)

    def checking_buy_button_click(self):
        """ Метод проверяет кликабельность кнопки КУПИТЬ. """
        assert self.wait.until(EC.text_to_be_present_in_element(MainPageLocators.BUY_BUTTON, 'КУПИТЬ'))
        assert self.wait.until(EC.element_to_be_clickable(MainPageLocators.BUY_BUTTON))

    def send_params_to_fields(self, email, name, exp=True):
        """ Метод заполняет поля EMAIL и ИМЯ пользователя в форме бронирования тура,
        нажимает на кнопку ОТПРАВИТЬ и проверяет реакцию от сервера. """
        self.scroll_to_bron()
        email_area = self.wait.until(EC.presence_of_element_located(MainPageLocators.EMAIL_AREA_1))
        email_area.send_keys(email)
        user_name = self.wait.until(EC.presence_of_element_located(MainPageLocators.USER_NAME_AREA_1))
        user_name.send_keys(name)
        # tour_name = self.wait.until(EC.presence_of_element_located(MainPageLocators.TOUR_NAME_AREA_1))
        # tour_name.send_keys(tour)
        send_button = self.wait.until(EC.presence_of_element_located(MainPageLocators.SEND_BUTTON_1))
        send_button.click()
        if exp:
            sleep(30)   # Время для ввода капча
            assert self.wait.until(
                EC.text_to_be_present_in_element(MainPageLocators.SUCCESSBOX_1,
                                                 'Спасибо! Данные успешно отправлены.'))
        else:
            errors_list = ['Ни одно поле не заполнено', 'Укажите, пожалуйста, корректный email',
                           'Укажите, пожалуйста, имя', 'None of the fields are filled in', 'Please put a name']
            err = self.wait.until(EC.presence_of_all_elements_located(MainPageLocators.ERROR_BOX_1))
            err_text = [el.text for el in err]
            print(err_text)
            assert set(err_text) <= set(errors_list)

    def check_logo(self):
        """ Метод проверяет кликабельность логотипа и возможность перехода на соответствующую страницу. """
        original_window = self.browser.current_window_handle
        self.scroll_to_bron()
        logo = self.wait.until(EC.presence_of_element_located(MainPageLocators.LOGO_MENU))
        assert self.wait.until(EC.element_to_be_clickable(MainPageLocators.LOGO_MENU))
        transit_url = logo.get_attribute('href')
        logo.click()
        self.switch_to_new_window(original_window, transit_url)

    def check_menu_elements(self):
        """ Метод проверяет возможность перехода по ссылкам выпадающего меню. """
        self.scroll_to_bron()
        menu = self.wait.until(EC.presence_of_all_elements_located(MainPageLocators.SELF_MENU))
        for elem in menu:
            assert elem.get_attribute('href') != f'{MAIN_URL}#', \
                f'Элемент с названием "{elem.text}" не переходит по ссылке'

    def check_menu_button(self):
        """ Метод проверяет кнопку "Забронировать тур" в выпадающем меню. """
        self.scroll_to_bron()
        button = self.wait.until(EC.presence_of_element_located(MainPageLocators.BUTTON_MENU))
        assert button.text == 'Забронировать тур'
        assert self.wait.until(EC.element_to_be_clickable(MainPageLocators.BUTTON_MENU))
        assert button.get_attribute('href') == f'{MAIN_URL}#form'

    def check_forward_button_on_first_day_photos(self):
        """ Метод проверяет смену фотографий при нажатии кнопки '>' (СЛЕДУЮЩАЯ)
        в блоке фотографий первого дня тура. """
        self.scroll_to_first_day_photos()

        forward = self.wait.until(EC.presence_of_all_elements_located(MainPageLocators.SLDS_RIGHT))
        tochki = self.wait.until(EC.presence_of_all_elements_located(MainPageLocators.POINTS1))
        photo = self.wait.until(EC.presence_of_all_elements_located(MainPageLocators.FIRST_DAY_PHOTO))
        print()
        dct = {}
        for i in range(7):

            assert 'bullet_active' in tochki[i % len(tochki)].get_attribute('class')
            dct.setdefault(tochki[i % len(tochki)].get_attribute('data-slide-bullet-for'),
                           photo[i % len(tochki)].get_attribute('content'))
            sleep(1)
            forward[0].click()
        assert len(set(dct.values())) == len(tochki), \
            'Количество уникальных фотографий не соответствует количеству точек'
        pprint(dct)

    def check_backward_button_on_first_day_photos(self):
        """ Метод проверяет смену фотографий при нажатии кнопки '<' (ПРЕДЫДУЩАЯ)
        в блоке фотографий первого дня тура. """
        self.scroll_to_first_day_photos()

        backward = self.wait.until(EC.presence_of_all_elements_located(MainPageLocators.SLDS_LEFT))
        tochki = self.wait.until(EC.presence_of_all_elements_located(MainPageLocators.POINTS1))
        for i in range(len(tochki)):
            assert 'bullet_active' in tochki[-(i % len(tochki))].get_attribute('class')
            sleep(1)
            backward[0].click()

    def check_forward_button_on_second_day_photos(self):
        """ Метод проверяет смену фотографий при нажатии кнопки '>' (СЛЕДУЮЩАЯ)
        в блоке фотографий второго дня тура. """
        self.scroll_to_second_day_photos()

        forward = self.wait.until(EC.presence_of_all_elements_located(MainPageLocators.SLDS_RIGHT))
        tochki = self.wait.until(EC.presence_of_all_elements_located(MainPageLocators.POINTS2))
        photo = self.wait.until(EC.presence_of_all_elements_located(MainPageLocators.SECOND_DAY_PHOTO))
        print()
        dct = {}
        for i in range(5):

            assert 'bullet_active' in tochki[i % len(tochki)].get_attribute('class')
            dct.setdefault(tochki[i % len(tochki)].get_attribute('data-slide-bullet-for'),
                           photo[i % len(tochki)].get_attribute('content'))
            sleep(1)
            forward[1].click()
        assert len(set(dct.values())) == len(tochki), \
            'Количество уникальных фотографий не соответствует количеству точек'
        pprint(dct)

    def check_backward_button_on_second_day_photos(self):
        """ Метод проверяет смену фотографий при нажатии кнопки '<' (ПРЕДЫДУЩАЯ)
        в блоке фотографий второго дня тура. """
        self.scroll_to_second_day_photos()

        backward = self.wait.until(EC.presence_of_all_elements_located(MainPageLocators.SLDS_LEFT))
        tochki = self.wait.until(EC.presence_of_all_elements_located(MainPageLocators.POINTS2))
        for i in range(len(tochki)):
            assert 'bullet_active' in tochki[-(i % len(tochki))].get_attribute('class')
            sleep(1)
            backward[1].click()

    def check_block_photos(self):
        """ Метод проверяет кликабельность фотографий в основном блоке фотографий и считает
        количество уникальных фотографий. """
        self.scroll_to_block_photos()

        sp = []
        for i in range(1, 9):
            how, what = MainPageLocators.PHOTOS_A
            what = what.replace('$', str(i))
            new_locator = (how, what)
            pict = self.wait.until(EC.presence_of_element_located(new_locator))
            sp.append(pict.get_attribute('data-original'))
            assert self.wait.until(EC.element_to_be_clickable(pict))

        assert len(set(sp)) == 8
        # pprint(sp)
        return set(sp)

    def check_zoom_photos(self):
        """ Метод переходит в зумовый режим просмотра фотографий, перелистывает их по порядку
        кнопкой '>' и считает количество уникальных фотографий"""
        dct = {}
        # self.scroll_to_block_photos()
        block_photos = self.wait.until(EC.presence_of_all_elements_located(MainPageLocators.BLOCK_PHOTOS))
        sleep(0.3)
        block_photos[0].click()
        next_photo = self.wait.until(EC.presence_of_element_located(MainPageLocators.NEXT))
        for i in range(8):
            curr_photo = self.wait.until(EC.presence_of_element_located(MainPageLocators.CURR_PHOTO))
            dct.setdefault(i, curr_photo.get_attribute('data-original'))
            next_photo.click()
            sleep(0.3)
        assert len(set(dct.values())) == 8
        # print()
        # pprint(dct)
        return set(dct.values())

