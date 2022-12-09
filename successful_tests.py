import os
import pytest
from api import PetFriends
from test_config import pet_info, get_api_key, t_control, email, password


pet_friends = PetFriends()


def test_get_key(email=email, password=password):
    """Проверка получения ключа API"""
    status, result = pet_friends.get_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_list(get_api_key, filter='my_pets'):
    """Проверка получения списка питомцев с фильтром 'мои питомцы'"""
    status, result = pet_friends.get_list_pets(get_api_key, filter)
    print(result)
    assert status == 200
    assert len(result['pets']) > 0
    assert len('my_pets') > 0


def test_post_new_pet(get_api_key, pet_info, pet_photo='images/huski1.jpg'):
    """Проверка возможности добавить нового питомца"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pet_friends.post_new_pet(get_api_key, pet_info['name'], pet_info['animal_type'],
                                              pet_info['age'], pet_photo)
    print(result)
    assert status is 200
    assert result['name'] == pet_info['name']


def test_delete_pet(get_api_key):
    """Проверка удаления существующего питомца по его id"""
    _, my_pets = pet_friends.get_list_pets(get_api_key, 'my_pets')
    # if len(my_pets['pets']) == 0:
    #     pet_friends.post_new_pet(auth_key, 'Жулька', 'crocodile', '22', 'images/husk2.jpeg')
    #     _, my_pets = pet_friends.get_list_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pet_friends.delete_pet(get_api_key, pet_id)

    _, my_pets_fresh = pet_friends.get_list_pets(get_api_key, 'my_pets')
    print(my_pets_fresh['pets'])
    assert status is 200
    assert pet_id not in my_pets_fresh.values()

# получение id и name моих питомцев
# def test_get_my_list(filter='my_pets'):
#     _, auth_key = pet_friends.get_api_key(email, password)
#     _, my_pets = pet_friends.get_list_pets(auth_key, filter)
#     pets = my_pets.get('pets')
#     for el in pets:
#         print(el['name'], el['id'])


def test_update_info(get_api_key, pet_info):
    """Проверка обновления информации о питомце по его id"""
    _, my_pets = pet_friends.get_list_pets(get_api_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    if len(my_pets['pets']) > 0:
        status1, result = pet_friends.update_info(get_api_key, pet_id, pet_info['name'],
                                                  pet_info['animal_type'], pet_info['age'])

    _, my_pets_fresh = pet_friends.get_list_pets(get_api_key, 'my_pets')
    print(my_pets_fresh)
    assert status1 == 200
    assert pet_info['name'] == my_pets_fresh['pets'][0]['name']


def test_create_new_pet(get_api_key, pet_info):
    status, result = pet_friends.create_new_pet(get_api_key, pet_info['name'],
                                                pet_info['animal_type'], pet_info['age'])
    _, my_pets = pet_friends.get_list_pets(get_api_key, 'my_pets')
    print(my_pets)
    assert status == 200
    assert result['name'] == pet_info['name']


@pytest.mark.xfail
def test_set_photo_pet(get_api_key, pet_photo='images/huski2.jpeg'):
    _, my_pets = pet_friends.get_list_pets(get_api_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pet_friends.set_photo_pet(get_api_key, pet_id, pet_photo)
    _, my_pets_fresh = pet_friends.get_list_pets(get_api_key, 'my_pets')
    assert status == 200
    assert result['pet_photo'] is not None
