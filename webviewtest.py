import webview
import requests
from DestroyPrettyPage import DestroyPrettyPage

def show_window(html: str):
    webview.create_window('Attached', html)
    webview.start()

def get_html(url: str) -> str:
    response = requests.get(url)
    return response.text

def test_class():
    dpp = DestroyPrettyPage('https://www.javatpoint.com/ionic')
    print(dpp.content)
    show_window(dpp.content)

def main():
    test_class()
    # show_window(get_html('https://www.google.com'))
    
if __name__ == '__main__':
    main()