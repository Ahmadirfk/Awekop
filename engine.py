import requests
from bs4 import BeautifulSoup as Parser
import pyzipper
import os

def fetch_info():
    # دریافت لیست آدرس‌ها از گاوصندوق گیت‌هاب
    raw_data = os.getenv('DATA_SRC', '')
    targets = [t.strip() for t in raw_data.split(',') if t.strip()]
    
    if not os.path.exists('vault'):
        os.makedirs('vault')
    
    for i, url in enumerate(targets):
        try:
            # دریافت محتوا با هویت مرورگر
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
            soup = Parser(res.text, 'html.parser')
            
            # ذخیره با فرمت غیرحساس .dat
            with open(f'vault/file_{i}.dat', 'w', encoding='utf-8') as f:
                f.write(f"Source: {url}\n\n{soup.get_text()}")
        except:
            continue

def create_pack():
    # دریافت رمز عبور از گاوصندوق
    password = os.getenv('Z_PW', 'pass123').encode()
    
    with pyzipper.AESZipFile('sync_pack.zip', 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zf:
        zf.setpassword(password)
        for root, _, files in os.walk('vault'):
            for f in files:
                zf.write(os.path.join(root, f), f)

def upload():
    tk = os.getenv('B_TK')
    cid = os.getenv('B_CID')
    url = f"https://tapi.bale.ai/bot{tk}/sendDocument"
    
    with open('sync_pack.zip', 'rb') as f:
        requests.post(url, files={'document': f}, data={'chat_id': cid})

if __name__ == "__main__":
    fetch_info()
    create_pack()
    upload()
