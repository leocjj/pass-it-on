"""
General results:
    * Process Pool Executor works WELL for intensive IO tasks.
    * Thread Pool Executor works GREAT for intensive IO tasks.
    * Asyncio functions work EXCELLENT for intensive IO tasks.
    * Elapsed times:
        Dict comprehension calling a function: 40.3
        Process Pool Executor calling a function: 12.6
        Thread Pool Executor calling a function: 7.2
"""

from time import monotonic
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import asyncio
import aiohttp
import urllib.request

URLS = [
    "http://www.eltiempo.com/",
    "http://www.elpais.com.co/",
    "http://www.bbc.co.uk/",
    "https://www.elmundo.es/",
    "https://es.euronews.com/noticias/internacional",
    "https://www.elespectador.com/",
    "https://www.semana.com/",
    "https://cnnespanol.cnn.com/",
    "https://www.larepublica.co/",
    "https://www.harvard.edu/",
    "https://www.yale.edu/",
    "https://www.utp.edu.co/",
    "http://www.mit.edu/",
    "https://www.stanford.edu/",
    "https://home.www.upenn.edu/",
    "https://duke.edu/",
    "https://www.cornell.edu/",
    "https://www.northwestern.edu/",
    "https://www.jhu.edu/",
    "https://wustl.edu/",
    "http://www.emory.edu/",
    "https://www.nd.edu/",
    "https://www.virginia.edu/",
    "https://www.vanderbilt.edu/",
    "https://www.cmu.edu/",
    "https://www.georgetown.edu/",
    "https://docs.python.org/3/library/asyncio.html",
    "https://docs.python.org/3/library/concurrent.futures.html",
    "https://docs.python.org/3/library/multiprocessing.html",
    "https://docs.python.org/3/library/threading.html",
    "https://docs.python.org/3/library/queue.html",
    "https://docs.python.org/3/library/subprocess.html",
    "https://docs.python.org/3/library/socket.html",
    "https://docs.python.org/3/library/select.html",
    "https://docs.python.org/3/library/ssl.html",
    "https://docs.python.org/3/library/urllib.html",
    "https://docs.python.org/3/library/http.html",
    "https://docs.python.org/3/library/ftplib.html",
    "https://docs.python.org/3/library/poplib.html",
    "https://docs.python.org/3/library/imaplib.html",
]


# Retrieve a single page and report the URL and contents
def load_url(url):
    # print(f"\tLoading {url}")
    with urllib.request.urlopen(url, timeout=60) as conn:
        return conn.read()


def load_one_by_one():
    elapsed = monotonic()
    result1 = {url: load_url(url) for url in URLS}
    print(f"\nLoading one by one spent: {(monotonic() - elapsed):.2f}\n")
    return result1


def load_with_process_pool():
    elapsed = monotonic()
    with ProcessPoolExecutor() as executor:
        result2 = {}
        for url, load in zip(URLS, executor.map(load_url, URLS)):
            result2[url] = load
    print(f"\nProcess Pool Executor spent: {(monotonic() - elapsed):.2f}\n")
    return result2


def load_with_thread_pool():
    elapsed = monotonic()
    with ThreadPoolExecutor() as executor:
        result3 = {}
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(load_url, url): url for url in URLS}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result3[url] = future.result()
            except Exception as exc:
                print(f"{url} generated an exception: {exc}")
    print(f"\nThread Pool Executor spent: {(monotonic() - elapsed):.2f}\n")
    return result3


async def async_load_url(url, session):
    # print(f"\tLoading {url}")
    async with session.get(url) as response:
        return await response.read()


async def load_with_asyncio():
    elapsed = monotonic()
    async with aiohttp.ClientSession() as session:
        tasks = [async_load_url(url, session) for url in URLS]
        result4 = await asyncio.gather(*tasks)
    print(f"\nAsyncio spent: {(monotonic() - elapsed):.2f}\n")
    return dict(zip(URLS, result4))


if __name__ == "__main__":
    print(f"\nLoading {len(URLS)} URLs...")
    load_one_by_one()
    load_with_process_pool()
    load_with_thread_pool()
    asyncio.run(load_with_asyncio())
    print("Done!")
