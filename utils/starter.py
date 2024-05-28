from utils.blum import BlumBot
from asyncio import sleep
from random import randint, uniform
from data import config
from utils.core import logger
import datetime
# import pandas as pd
from utils.telegram import Accounts
import asyncio
from itertools import zip_longest
from utils.core import get_all_lines
from aiocfscrape import CloudflareScraper
from fake_useragent import UserAgent
import aiohttp




async def start(thread: int, account: str, proxy: [str, None]):
    async with CloudflareScraper(headers={'User-Agent': UserAgent(os='android').random}, timeout=aiohttp.ClientTimeout(total=60)) as session:
        blum = BlumBot(account=account, thread=thread, session=session, proxy=proxy)
        max_try = 5
    
        await sleep(uniform(*config.DELAYS['ACCOUNT']))
        await blum.login()
    
        while True:
            try:
                msg = await blum.claim_daily_reward()
                if isinstance(msg, bool) and msg:
                    logger.success(f"Thread {thread} | Claimed daily reward!")
    
                timestamp, start_time, end_time, play_passes = await blum.balance()
    
                if play_passes and play_passes > 0:
                    await blum.play_game(play_passes)
                
                await sleep(uniform(3, 10))

                # try:
                #     tasks = await blum.get_tasks()
                #     for task in tasks:
                #         if task.get('status') == 'CLAIMED' or task.get('title') in config.BLACKLIST_TASKS:
                #             continue
        
                #         if task.get('status') == "NOT_STARTED":
                #             await blum.start_complete_task(task)
                #             await sleep(uniform(10, 15))
                #         elif task.get('status') == 'STARTED':
                #             await sleep(uniform(10, 15))
        
                #         if await blum.claim_task(task):
                #             logger.success(f"Thread {thread} | Completed task «{task.get('title')}»")
                #         else:
                #             logger.error(f"Thread {thread} | Failed complete task «{task.get('title')}»")
                # except Exception as e:
                #     logger.error(f"Thread {thread} | Error in task management: {e}")
    
                timestamp, start_time, end_time, play_passes = await blum.balance()

                try:
                    if start_time is None and end_time is None and max_try>0:
                        await blum.start()
                        logger.info(f"Thread {thread} | Start farming!")
                        max_try-=1
        
                    elif start_time is not None and end_time is not None and timestamp is not None and timestamp >= end_time and max_try>0:
                        await blum.refresh()
                        timestamp, balance = await blum.claim()
                        logger.success(f"Thread {thread} | Claimed reward! Balance: {balance}")
                        max_try-=1
        
                    elif end_time is not None and timestamp is not None:
                        sleep_duration = end_time - timestamp
                        logger.info(f"Thread {thread} | Sleep {sleep_duration} seconds!")
                        max_try+=5
                        await sleep(sleep_duration)
                    
                    elif max_try==0:
                        break
                        
                except Exception as e:
                    logger.error(f"Thread {thread} | Error in farming management: {e}")
    
                await sleep(10)
            except Exception as e:
                logger.error(f"Thread {thread} | Error: {e}")



async def stats():
    logger.success("Analytics disabled")
    # accounts = await Accounts().get_accounts()
    # proxys = get_all_lines("data/proxy.txt")

    # tasks = []
    # for thread, (account, proxy) in enumerate(zip_longest(accounts, proxys)):
    #     if not account: break
    #     tasks.append(asyncio.create_task(BlumBot(account=account, thread=thread, proxy=proxy).stats()))

    # data = await asyncio.gather(*tasks)

    # path = f"statistics/statistics_{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"
    # columns = ['Phone number', 'Name', 'Points', 'Play passes', 'Referrals', 'Limit invites', 'Referral link']
    
    # df = pd.DataFrame(data, columns=columns)
    # df['Name'] = df['Name'].astype(str)
    # df.to_csv(path, index=False, encoding='utf-8-sig')

    # logger.success(f"Saved statistics to {path}")
