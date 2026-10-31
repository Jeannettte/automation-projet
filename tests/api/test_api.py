import pytest
from selenium.webdriver.common.by import By

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

from config import settings


CREDENTIAL={
        "userName": settings.USENAME,
        "password": settings.PASSWORD,
        "userID": settings.USERID
    }

@pytest.mark.api
def test_api_01_statut_on():
    PATH="/BookStore/v1/Books"
    session = requests.Session()
    response = session.get(f"{settings.BASE_URL}{PATH}")


    assert response.status_code == 200


@pytest.mark.api
def test_api_02_connection_user():
    

    PATH="/Account/v1/GenerateToken"
    PATH2 = "/Account/v1/Authorized"

    session = requests.Session()

    print(CREDENTIAL)

    response = session.post(f"{settings.BASE_URL}{PATH}", json={
        "userName": CREDENTIAL["userName"],
        "password": CREDENTIAL["password"]
    })

    assert response.status_code == 200

    response = session.post(f"{settings.BASE_URL}{PATH2}", json={
        "userName": CREDENTIAL["userName"],
        "password": CREDENTIAL["password"]
    })
    assert response.status_code == 200


@pytest.mark.api
def test_api_03_invalid_credential():
    PATH="/Account/v1/Authorized"

    session = requests.Session()


    response = session.post(f"{settings.BASE_URL}{PATH}", json={
            "userName": CREDENTIAL["userName"],
            "password": "INVALID"
        })

    assert response.status_code == 404


@pytest.mark.api
def test_api_04_get_specific_book():
    PATH="/BookStore/v1/Book"

    ISBN="9781449325862"

    session = requests.Session()
    
    response = session.get(f"{settings.BASE_URL}{PATH}?ISBN={ISBN}", )

    assert response.status_code == 200
    assert response.json()['isbn'] == ISBN
    assert response.json()['title'] == "Git Pocket Guide"
    
    