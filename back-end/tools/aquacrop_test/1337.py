import json
import requests
from twilio.rest import Client
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
import time
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service

# # URL for the login endpoint

# def recaptcha_handling(session):

#     chrome_options = Options()
#     chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
#     chrome_options.add_argument('--no-sandbox')  # # Bypass OS security model
#     chrome_options.add_argument('--disable-dev-shm-usage')  # overcome limited resource problems
#     chrome_options.add_argument('start-maximized')  # 
#     chrome_options.add_argument('disable-infobars')
#     chrome_options.add_argument('--disable-extensions')

#     # Set path to chromedriver as needed
#     # driver = webdriver.Chrome(executable_path='/usr/bin/google-chrome', options=chrome_options)
#     service = Service(executable_path='/usr/bin/google-chrome')
#     driver = webdriver.Chrome(service=service)

#     # Rest of your code
#     driver.add_cookie(session.cookies)
#     driver.get('https://admission.1337.ma/fr/candidature/piscine')
#     # driver = webdriver.Chrome()
#     # driver.add_cookie(session.cookies)
#     # driver.get('https://admission.1337.ma/fr/candidature/piscine')

#     # Wait and click the reCAPTCHA checkbox
#     wait = WebDriverWait(driver, 10)
#     frame = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
#     driver.switch_to.frame(frame)

#     checkbox = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "recaptcha-checkbox-border")))
#     checkbox.click()
#     driver.switch_to.default_content()
#     recaptcha_response = driver.find_element(By.ID, 'g-recaptcha-response').get_attribute('value')
#     print("Recaptcha Response Token:", recaptcha_response)

# session = requests.Session()

# url = 'https://admission.1337.ma/api/auth/login'

# # Headers as specified
# headers = {
#     'Accept': 'application/json, text/plain, */*',
#     'Content-Type': 'application/json',
#     'Origin': 'https://admission.1337.ma',
#     'Referer': 'https://admission.1337.ma/fr/users/sign_in',
#     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
#     'Sec-Fetch-Dest': 'empty',
#     'Sec-Fetch-Mode': 'cors',
#     'Sec-Fetch-Site': 'same-origin',
#     'G-Recaptcha-Response': '09APNMo_i962GlZLn99mZDYdxQPaobaVz6VBc9mmaLFfbpScv4oj1qcjiZnmjrjYRtzXhA5GKiBRlvE99DhHh_WcEfDUiICOKI4nl-pQ'
# }

# # Replace these with your actual username and password
# data = {
#     'email': 'Jaafar.chmiaa@gmail.com',
#     'password': 'Romatiamo06@'
# }
# check = True
# piscine_id = 0

# i = 0
# while check:
    
#     if i == 0:
#         response = session.post(url, headers=headers, data=json.dumps(data))
#         i = 1
#     print(f'status : {response.status_code} : {response.json()}')
#     if response.status_code == 201:
#         protected_url = 'https://admission.1337.ma/api/piscines/current'
#         response = session.get(protected_url, headers=headers)
#         if response.status_code == 200:
#             campus = response.json()
#             if len(campus) == 3:
                
#                 for i in range(0, 3):
#                     if campus[i].get('campus').get('slug') == 'Benguerrir':
#                         piscine_id = campus[i].get('id')
#                         break
#                 print(f'got piscine id : {piscine_id}, now i will try to solve recaptcha')
#                 # response = session.post('https://admission.1337.ma/api/users-piscines', headers=headers, data=json.dumps({
#                 #     'piscine_id' : piscine_id,
#                 #     'user_id' : 136576
#                 # }))
#                 # print(response.status_code ,response.text)
#                 recaptcha_handling(session)
                
#             check = False
#             session.close()
#     else :
#         time.sleep(30)


account_sid = 'AC4abc0872dcae8727a05e9fe88899cf4a'
auth_token = '5a6c0a6465f1a4eff9ab2fbd6d3218e3'

client = Client(account_sid, auth_token)

def send_sms(phone_number, message):
    message = client.messages.create(
        body=message,
        from_='+12407433480',  # Twilio phone number
        to=phone_number
    )
    print(f'Message sent with SID: {message.sid}')


session = requests.Session()

url = 'https://admission.1337.ma/api/auth/login'

# Headers as specified
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
    'Origin': 'https://admission.1337.ma',
    'Referer': 'https://admission.1337.ma/fr/users/sign_in',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'G-Recaptcha-Response': '09APNMo_i962GlZLn99mZDYdxQPaobaVz6VBc9mmaLFfbpScv4oj1qcjiZnmjrjYRtzXhA5GKiBRlvE99DhHh_WcEfDUiICOKI4nl-pQ'
}

# Replace these with your actual username and password
data = {
    'email': 'Jaafar.chmiaa@gmail.com',
    'password': 'Romatiamo06@'
}
check = True
piscine_id = 0

i = 0
while check:
    
    try :

        if i == 0:
            session = requests.Session()
            response = session.post(url, headers=headers, data=json.dumps(data))
            i = 1
            print(f'status : {response.status_code} : {response.json()}')
        if i == 1:
            protected_url = 'https://admission.1337.ma/api/piscines/current'
            response = session.get(protected_url, headers=headers)
            if response.status_code == 200:
                campus = response.json()
                if len(campus) != 0:
                    
                    send_sms('+212614009743', 'lpool tlaa7 dkhel ched blasstk')
                    send_sms('+212644422977', 'lpool tlaa7 dkhel ched blasstk')
                    send_sms('+212612970191', 'lpool tlaa7 dkhel ched blasstk')
                    send_sms('+212663115453', 'lpool tlaa7 dkheli chedi blasstk')
                    check = False
                    print('sms was sent, piscine on')

                else : 
                    print('no piscine has been found')
                    time.sleep(1)   
        else :
            session.close()
            i = 0
            time.sleep(10)
    except Exception as e:
        i = 0
        print(f'error : {e}')
        session.close()
        time.sleep(5)