import asyncio
import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()


class Crawller(object):
    def __init__(self, url: str, base_dir: str, office_id: int):
        self.url = url
        self.office_id = office_id
        self.base_dir = base_dir
        chrome_prefs = {
            "profile.default_content_settings.popups": 0,
            "download.default_directory": f"{self.base_dir}/chromedriver",
        }

        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("prefs", chrome_prefs)
        self.chrome_options.add_argument(
            f"--user-data-dir={self.base_dir}/Chrome_{str(self.office_id)}\\"
        )
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--headless")

    async def fetch_data(self):
        start_time = time.time()
        # cant print or i/o block
        # print(f"start of fetch_data:\ngonna go to url: {self.url}")
        chrome_service = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=chrome_service, options=self.chrome_options)
        # print(f"brower initialized with options for {self.url}: {browser}")
        browser.get(self.url)
        if self.office_id == 2:
            await asyncio.sleep(5)
        elif self.office_id == 4:
            await asyncio.sleep(10)

        await asyncio.sleep(0.001)
        # print(
        #    f"length of content from browser.get: {len(browser.page_source)}\nend of {self.url} fetch_data"
        # )
        end_time = time.time()
        run_time = end_time - start_time
        return {self.url: {"length": len(browser.page_source), "run_time": run_time}}


async def main():
    number_of_offices = 10
    base_dir = os.getenv("CHROME_BINARY_PATH", "/usr/bin")
    print(f"starting test with {number_of_offices} offices\n")
    print(f"using base dir: {base_dir}\n")
    crawllers = [
        Crawller(
            url=f"https://quotes.toscrape.com/page/{i}/",
            base_dir=base_dir,
            office_id=i,
        ).fetch_data()
        for i in range(2, number_of_offices)
    ]
    results = await asyncio.gather(*crawllers)
    print(f"results from the experiment:\n{results}")
    page_2_run_time = [
        result["https://quotes.toscrape.com/page/2/"]["run_time"]
        for result in results
        if "https://quotes.toscrape.com/page/2/" in result
    ][0]
    page_3_run_time = [
        result["https://quotes.toscrape.com/page/3/"]["run_time"]
        for result in results
        if "https://quotes.toscrape.com/page/3/" in result
    ][0]
    assert page_2_run_time > page_3_run_time
    for result in results:
        assert list(result.values())[0]["length"] > 0


if __name__ == "__main__":
    asyncio.run(main())
