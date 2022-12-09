import pytest
from faker import Faker
import random
import requests
import json
from datetime import datetime

fake = Faker()

email = 'svnandr@yandex.ru'
password = 'Aaaa1111'


@pytest.fixture
def pet_info():
    name = fake.first_name()
    animal_type = 'вот такая'
    age = str(random.randint(1, 50))
    data = {'name': name, 'animal_type': animal_type, 'age': age}
    return data


@pytest.fixture
def get_api_key():
    header = {'email': email, 'password': password}
    resp = requests.get(url='https://petfriends.skillfactory.ru' + '/api/key', headers=header)
    try:
        result = resp.json()
    except json.decoder.JSONDecodeError:
        result = resp.text
    return result


@pytest.fixture(autouse=True)
def t_control(request):
    a = str(f'\n Запускаю тест {request.function.__name__}')
    start_time = datetime.now()
    yield
    b = str(f'\n Тест {request.function.__name__} выполнен')
    end_time = datetime.now()
    c = str(f'\n Тест длился  {end_time - start_time}')
    with open('log.txt', 'a', encoding='utf8') as file:
        file.write(a + b + c)
