from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def download_ibrx50_data():
    """
    Realiza o download dos dados do IBrX-50 do site da B3.
    """
    chrome_options = webdriver.ChromeOptions()
    download_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'results'))
    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': download_dir,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True
    })
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--disable-popup-blocking')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        url = 'https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBXL?language=pt-br'
        driver.get(url)
        
        try:
            accept_cookies = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))
            )
            accept_cookies.click()
            print('Cookies aceitos com sucesso!')
        except Exception as e:
            print('Não foi possível encontrar o botão de cookies ou já foi aceito anteriormente')
        
        print('Procurando o dropdown...')
        dropdown = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'selectPage'))
        )
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'selectPage'))
        )
        
        print('Selecionando 120 itens por página...')
        select = Select(dropdown)
        try:
            select.select_by_visible_text('120')
        except:
            try:
                driver.execute_script("arguments[0].value = '120'; arguments[0].dispatchEvent(new Event('change'))", dropdown)
            except:
                print('Não foi possível selecionar o valor usando métodos convencionais')
                options = driver.find_elements(By.TAG_NAME, 'option')
                for option in options:
                    if option.get_attribute('value') == '120':
                        option.click()
                        break
        print('Valor selecionado com sucesso!')
        time.sleep(3)
        
        time.sleep(2)
        
        print('Procurando botão de download...')
        try:
            download_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'btn-download'))
            )
        except:
            try:
                download_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Download')]" ))
                )
            except:
                try:
                    download_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.LINK_TEXT, "Download"))
                    )
                except Exception as e:
                    print(f'Não foi possível encontrar o botão de download: {str(e)}')
                    print('\nHTML da página:')
                    print(driver.page_source)
                    raise e
        
        print('Botão de download encontrado, tentando clicar...')
        driver.execute_script("arguments[0].click();", download_button)
        
        time.sleep(5)
        
        print('Download concluído com sucesso!')
        
    except Exception as e:
        print(f'Erro durante o processo: {str(e)}')
        
    finally:
        driver.quit()