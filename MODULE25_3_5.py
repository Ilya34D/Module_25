import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
    # получение объекта веб-драйвера для нужного браузера в полноэкранном режиме
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--kiosk')
    pytest.driver = webdriver.Chrome('c:/path/to/chromedriver.exe')
    pytest.driver.maximize_window()
    # Переходим на страницу авторизации
    pytest.driver.get('https://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()


def test_show_my_pets():
    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys('ilya-dolgov34@yandex.ru')
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys('r5e7eumh')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    pytest.driver.implicitly_wait(3)
    # переходим на страницу мои питомцы
    btn_my_pets = pytest.driver.find_element_by_link_text('Мои питомцы')
    btn_my_pets.click()
    # Проверяем, что мы оказались на главной странице 'Мои питомцы'
    assert pytest.driver.find_element_by_tag_name('h2').text == "Ilya.D34"

    element = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".\\.col-sm-4.left")))

    # Сохраняем в переменную ststistic элементы статистики
    statistic = pytest.driver.find_elements_by_css_selector(".\\.col-sm-4.left")

    element = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))

    # Сохраняем в переменную pets элементы карточек питомцев
    pets = pytest.driver.find_elements_by_css_selector('.table.table-hover tbody tr')

    # Получаем количество питомцев из данных статистики
    number = statistic[0].text.split('\n')
    number = number[1].split(' ')
    number = int(number[1])

    # Получаем количество карточек питомцев
    number_of_pets = len(pets)

    # ожидание появления данных на странице
    element = WebDriverWait(pytest.driver, 15).until(
       EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover img")))
    # Сохраняем в переменную images элементы с атрибутом img
    images = pytest.driver.find_elements_by_css_selector('.table.table-hover img')

    # Выбираем данные питомцев
    # ожидание появления данных на странице
    element = WebDriverWait(pytest.driver, 15).until(EC.presence_of_element_located(
       (By.XPATH, '//tbody/tr/td[1]')))
    pet_names = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table[1]/thead[1]/tr[1]/th[2]')  # имена
    pet_species = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table[1]/thead[1]/tr[1]/th[3]')  # порода
    pet_ages = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table[1]/thead[1]/tr[1]/th[4]')  # возраст
    print('\n')
    # print(len(pet_names))
    pet_count = len(pet_names)  # количество питомцев на странице
    print('Всего на странице питомцев: ', pet_count)
    # находим все имена
    names = []
    for l in pet_names:
       names.append(l.text)
    # print(pnames)
    # проверки на дублирование имён и питомцев
    for i in range(pet_count - 1):
       # одинаковые имена
       try:
          assert names.count(pet_names[i].text) <= 1
       except:
          print('Имя  "', pet_names[i].text, '"  среди моих питомцев встречается', names.count(pet_names[i].text),
                'раз/a')
          # удаляем уже проверенные совпадающие имена
          names = list(filter(lambda x: x != pet_names[i].text, names))
       for j in range(i + 1, pet_count):
          # print(i, j)
          if pet_names[i].text == pet_names[j].text:
             if pet_species[i].text == pet_species[j].text:
                # одинаковые питомцы
                try:
                   assert pet_ages[i].text != pet_ages[j].text
                except:
                   print("Есть дубликаты питомцев с номерами: ", i + 1, j + 1)

    # Проверяем, что количество карточек питомцев совпадает со статистикой
    assert number == number_of_pets

    # проверка на пустые поля
    img_no_photo = 0
    pet_no_name = 0
    pet_no_species = 0
    pet_no_ages = 0
    for i in range(pet_count):
       try:  # фото
          assert images[i].get_attribute('src') != ''
       except:
          img_no_photo += 1
       try:  # имя
          assert pet_names[i].text != ''
       except:
          pet_no_name += 1
       try:  # порода
          assert pet_species[i].text != ''
       except:
          pet_no_species += 1
       try:  # возраст
          assert pet_ages[i].text != ''
       except:
          pet_no_ages += 1

    # Проверяем, что на странице со списком моих питомцев хотя бы у половины питомцев есть фото
    if img_no_photo > round(pet_count / 2):
       photo_text = 'больше половины'
    else:
       photo_text = 'меньше половины'
    # Вывод результатов
    print('Моих питомцев без фото', photo_text, '-', img_no_photo, 'из', pet_count)
    print('Моих питомцев без имени: ', pet_no_name)
    print('Моих питомцев без породы: ', pet_no_species)
    print('Моих питомцев без возраста: ', pet_no_ages)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   pass
