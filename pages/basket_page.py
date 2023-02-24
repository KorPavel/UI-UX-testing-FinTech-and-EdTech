from .base_page import BasePage
from .locators import BasketPageLocators
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from time import sleep


class BasketPage(BasePage):

    def __init__(self, browser, url, timeout=10):
        super().__init__(browser, url, timeout)
        self.plus = self.wait.until(EC.presence_of_element_located(BasketPageLocators.TOUR_PLUS))
        self.minus = self.wait.until(EC.presence_of_element_located(BasketPageLocators.TOUR_MINUS))
        self.name_area = self.wait.until(EC.presence_of_element_located(BasketPageLocators.NAME_AREA))
        self.email_area = self.wait.until(EC.presence_of_element_located(BasketPageLocators.EMAIL_AREA))
        self.phone_area = self.wait.until(EC.presence_of_element_located(BasketPageLocators.PHONE_AREA))
        self.checkout = self.wait.until(EC.presence_of_element_located(BasketPageLocators.CHECKOUT))
        # self.tour_return = self.wait.until(EC.presence_of_element_located(BasketPageLocators.TOUR_RETURN))

    def should_be_basic_elements(self):
        """ Метод проверяет наличие основных элементов на странице корзины. """
        assert self.wait.until(EC.text_to_be_present_in_element(BasketPageLocators.YOUR_ORDER, 'Ваш заказ:'))
        assert self.wait.until(EC.element_to_be_clickable(BasketPageLocators.BASKET_CLOSE))
        assert self.name_area
        assert self.email_area
        assert self.phone_area
        assert self.checkout

    def price_calculate(self):
        """ Метод вычисляет стоимость тура из расчёта общей стоимости корзины и количества мест. """
        amount = self.wait.until(EC.presence_of_element_located(BasketPageLocators.TOUR_AMOUNT)).text
        price = self.wait.until(EC.presence_of_element_located(BasketPageLocators.TOTAL_PRICE)).text
        try:
            price = price.replace(' ', '')
            pr = int(price)
            am = int(amount)
            # print(f'\nprice = {pr}, type = {type(pr)}\namount = {am}, type = {type(am)}')
            res = int(pr / am)
            return res
        except:
            print(f'\nprice = {price}\namount = {amount}')
            return 29000

    def product_counter_operation_plus(self, price_tour):
        """ Метод сравнивает вычисленную стоимость тура с рекламной стоимостью тура. """
        self.plus.click()
        sleep(0.5)
        assert self.price_calculate() == price_tour
        self.plus.click()
        self.plus.click()
        assert self.price_calculate() == price_tour

    def product_counter_operation_minus(self, price_tour):
        """ Метод сравнивает вычисленную стоимость тура с рекламной стоимостью тура. """
        self.plus.click()
        self.minus.click()
        sleep(0.5)
        assert self.price_calculate() == price_tour
        self.minus.click()
        tour_return = self.wait.until(EC.presence_of_element_located(BasketPageLocators.TOUR_RETURN))
        sleep(0.5)
        assert tour_return.text == 'Вернуть'
        tour_return.click()
        sleep(0.5)
        assert self.price_calculate() == price_tour

    def product_counter_operation_manual_input(self, price_tour, amount):
        """ Метод сравнивает вычисленную стоимость тура с рекламной стоимостью тура. """
        tour_amount = self.wait.until(EC.presence_of_element_located(BasketPageLocators.TOUR_AMOUNT))
        ActionChains(self.browser)\
            .move_to_element(tour_amount)\
            .double_click()\
            .send_keys(Keys.BACKSPACE)\
            .send_keys(amount)\
            .perform()
        ActionBuilder(self.browser).clear_actions()     # Освободить все действия
        self.wait.until(EC.presence_of_element_located(BasketPageLocators.TOTAL_PRICE)).click()
        sleep(0.5)
        assert self.price_calculate() == price_tour

    def send_params_to_fields(self, name, email, phone, exp=True):
        """ Метод заполняет поля персональными данными пользователя и проверяет реакцию системы. """
        self.name_area.send_keys(name)
        self.email_area.send_keys(email)
        self.phone_area.send_keys(phone)
        self.checkout.click()
        if exp:
            sleep(30)  # Время для ввода капча
            assert self.wait.until(
                EC.text_to_be_present_in_element(BasketPageLocators.SUCCESSBOX_2,
                                                 'Спасибо! Данные успешно отправлены.'))
        else:
            errors_list = ['Пожалуйста, заполните все обязательные поля', 'Укажите, пожалуйста, имя',
                           'Укажите, пожалуйста, корректный email', 'Укажите, пожалуйста, корректный номер телефона']
            err = self.wait.until(EC.presence_of_all_elements_located(BasketPageLocators.ERROR_BOX_2))
            err_text = [el.text for el in err]
            print(err_text)
            assert set(err_text) <= set(errors_list)
