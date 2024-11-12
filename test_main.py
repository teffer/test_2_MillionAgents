import requests
BASE_URL = "http://127.0.0.1:8000"

def shorten_url(original_url):
    response = requests.post(f"{BASE_URL}/shorten", json={"original_url": original_url})
    if response.status_code == 200:
        return response.json().get("short_url")
    else:
        print("Ошибка при создании короткой ссылки:", response.text)
        return None

def test_redirect(short_url):
    response = requests.get(f"{BASE_URL}/{short_url}")
    if response.status_code == 200:
        print(f"Перенаправлен на адресс: {response.url}")
    else:
        print(f"Ошибка при редиректе с короткой ссылки {short_url}: {response.status_code}")

if __name__ == "__main__":
    original_url = "https://www.google.com"
    print(f"Оригинальная ссылка: {original_url}")
    short_url = shorten_url(original_url)
    if short_url:
        print(f"Короткая ссылка: {short_url}")
        test_redirect(short_url)