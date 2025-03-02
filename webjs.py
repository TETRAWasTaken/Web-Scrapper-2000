from httpcore import TimeoutException
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
import json
data = []
url = "https://www.myscheme.gov.in/search"
nextselector = "#__next > div > main > div.grid.grid-cols-4.gap-4.container.mx-auto.relative.px-4 > div.sm\:col-span-3.col-span-4.items-center.justify-center > div.mt-2 > div.w-full.overflow\:hidden > div > ul > svg.ml-2.text-darkblue-900.dark\:text-white.cursor-pointer"
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url)

    n=0

    while True:
        n=n+1
        print(f"scraping page {n}")
        try:
            page.wait_for_selector("body")
        except TimeoutException:
            print("Timed out waiting for page to load")
            break

        html = page.content()
        pattern = r'<div class="mx-auto rounded-xl shadow-md overflow-hidden w-full group hover:shadow-lg bg-white dark:bg-dark dark:shadow-xl dark:hover:shadow-2xl">.*?>.*?</div></div></div></div></div></div>'

        a = re.findall(pattern, html)
        len(a)

        for i in a:
            x = re.findall(r'<span>(.*?)</span>', i, re.DOTALL)
            x.insert(1, re.findall(r'<h2 class="mt-3.*?>(.*?)</h2>', i)[0])
            data.append(x)


        try:
            next_button = page.query_selector(nextselector)
            if next_button:
                next_button.click()
            else:
                print("No more pages")
                break
        except Exception as e:
            print(e)

    browser.close()

with open("data.json", "w", encoding="utf8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Done")