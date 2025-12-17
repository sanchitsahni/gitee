import aiohttp
from config import config
from mythic_container.logging import logger

async def send_to_mythic(message):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            config["mythic_address"],
            headers={"Mythic": "gitee"},
            data=message,
        ) as response:
            if response.status == 200:
                return await response.text()
            else:
                logger.info(f"Failed to send message to Mythic. Status code: {response.status}")
                logger.info(f"Response: {await response.text()}")
                return None