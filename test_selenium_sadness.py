import asyncio
import os
from inspect import signature

import pytest

import selenium_sadness

base_dir = os.getenv("CHROME_BINARY_PATH", "/usr/bin")

test_cases = [
    (f"https://quotes.toscrape.com/page/{i}/", base_dir, i) for i in range(2, 10)
]


def async_run_pytest(async_pytest):
    def wrapper(*args, **kwargs):
        return asyncio.run(async_pytest(*args, **kwargs))

    wrapper.__signature__ = signature(async_pytest)
    return wrapper


@pytest.mark.parametrize("url,chrome_path,page_num", test_cases)
@async_run_pytest
async def test_selenium_sadness(url: str, chrome_path: str, page_num: int):
    c = selenium_sadness.Crawller(url=url, base_dir=chrome_path, office_id=page_num)
    result = await c.fetch_data()
    assert result
