import asyncio
import time


from services.parse_pegas_cls import ParsePegas

start_time = time.time()

if __name__ == '__main__':

    parse_pegas = ParsePegas()
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # Necessary for Windows users
    loop = asyncio.get_event_loop()
    loop.run_until_complete(parse_pegas.parse_pegas())
    end_time = time.time() - start_time
    print(f"\nExecution time: {end_time} seconds")
