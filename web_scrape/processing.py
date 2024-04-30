import multiprocessing
import concurrent.futures
import time

start = time.perf_counter()


def process_urls(seconds):
    print(f"Sleeping for {seconds} seconds")
    time.sleep(seconds)
    return f"Done sleeping --- {seconds}"


if __name__ == "__main__":
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        seconds = [5, 4, 3, 2, 1]
        # execute in a results
        # results = [executor.submit(process_urls, seconds[num]) for num in range(5)]
        # execute with map
        results = executor.map(process_urls, seconds)
        for result in results:
            print(result)
    #     for f in concurrent.futures.as_completed(results):
    #         print(f.result())

    finish = time.perf_counter()

    print(f"finished in {round(finish-start,2)} seconds (s)")
