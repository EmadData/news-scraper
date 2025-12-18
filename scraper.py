import requests as rq
import pandas as pd
from bs4 import BeautifulSoup

my_list = []
seen = set()

def get_news(url, category):
    response = rq.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.find_all("article")

    for item in items:
        title_tag = item.find("h4")
        time_tag = item.find("time")

        if title_tag is None or time_tag is None:
            continue

        title = title_tag.text.strip()
        time_text = time_tag.text.strip()

        if len(title) > 10:
            length = "بلند"
        elif len(title) > 3:
            length = "کوتاه"
        else:
            continue

        if "1404" in time_text:
            continue

        if title in seen:
            continue

        seen.add(title)
        my_list.append({
            "خبر": title,
            "دسته": category,
            "اندازه": length,
            "زمان": time_text,
            "منبع": "تسنیم"
        })

sources = [
    ("https://www.tasnimnews.com/fa/service/1/%D8%B3%DB%8C%D8%A7%D8%B3%DB%8C", "سیاسی"),
    ("https://www.tasnimnews.com/fa/service/3/%D9%88%D8%B1%D8%B2%D8%B4%DB%8C", "ورزشی"),
    ("https://www.tasnimnews.com/fa/service/8/%D8%A8%DB%8C%D9%86-%D8%A7%D9%84%D9%85%D9%84%D9%84", "بین‌المللی"),
    ("https://www.tasnimnews.com/fa/service/1486/%D9%81%D8%B6%D8%A7-%D9%88-%D9%86%D8%AC%D9%88%D9%85", "نجوم"),
]

for url, category in sources:
    get_news(url, category)

df = pd.DataFrame(my_list)
df.to_csv("titles.csv", index=False, encoding="utf-8-sig")

print(df.head())
print(df["دسته"].value_counts())
print("Total news:", len(df))
