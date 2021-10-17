from selenium import webdriver
import random
import time
from auth_data import login, password
from selenium.webdriver.common.keys import Keys

# Данный скрипт будет проходить аудентификацию на сайте и писать коммент
# Будем запускать каждую минуту


url = "https://vk.com/"

nash_spisok_user_agent = [
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 OPR/80.0.4170.16"
]
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={random.choice(nash_spisok_user_agent)}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.headless = True

def user_agent_usage(url):

    driver = webdriver.Chrome(
        executable_path="./chromedriver.exe",
        options=options
    )
    try:
        # Вызываем метод get и отправляем наш браузер на страницу
        # Поставим задержку что бы страница успела прогрузиться time.sleep(3)
        driver.get(url=url)
        driver.implicitly_wait(5)
        print("Passing authentication...")

        email_input = driver.find_element_by_id("index_email")
        email_input.clear()
        email_input.send_keys(login)
        driver.implicitly_wait(1)
        pass_input = driver.find_element_by_id("index_pass")
        pass_input.clear()
        pass_input.send_keys(password)
        driver.implicitly_wait(1)

        pass_input.send_keys(Keys.ENTER)
        driver.implicitly_wait(5)

        print("Opening My page...")
        login_button = driver.find_element_by_class_name("left_label").click()
        time.sleep(1)

        print("Adding comment...")
        comment_button = driver.find_element_by_class_name("_comment").click()
        time.sleep(1)

        comment = driver.find_elements_by_class_name("submit_post_field")[1].send_keys("COOOL VIDEO ;)" + Keys.ENTER)
        time.sleep(1)
        print("Clothing program...")



    except Exception as _ex:
        print(_ex)

    finally:
        driver.close()
        driver.quit()

user_agent_usage(url)

