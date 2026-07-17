import requests
from bs4 import BeautifulSoup
import os
import shutil

# خواندن لینک‌ها از سکرت گیتهاب
raw_urls = os.getenv("TARGET_URLS", "")
URLS = [url.strip() for url in raw_urls.split(",") if url.strip()]

def scrape():
    # پاکسازی پوشه قدیمی
    if os.path.exists('output'):
        shutil.rmtree('output')
    os.makedirs('output')

    if not URLS:
        print("هیچ لینکی در سکرت TARGET_URLS پیدا نشد.")
        return

    for i, url in enumerate(URLS):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, timeout=20, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            # حذف کدهای اسکریپت و استایل
            for s in soup(["script", "style"]):
                s.extract()
            
            text = soup.get_text(separator='\n')
            clean_text = '\n'.join(line.strip() for line in text.splitlines() if line.strip())

            # ذخیره با پسوند .data
            file_name = f"output/page_{i+1}.data"
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(clean_text)
            print(f"استخراج موفق: {url}")
            
        except Exception as e:
            print(f"خطا در استخراج {url}: {e}")

if __name__ == "__main__":
    scrape()
