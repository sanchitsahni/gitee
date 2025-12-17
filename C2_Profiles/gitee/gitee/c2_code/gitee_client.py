import aiohttp
import base64
from config import config
from mythic_container.logging import logger

BASE = "https://gitee.com/api/v5"


async def delete_comment(comment_id):
    url = f"{BASE}/repos/{config['owner']}/{config['repo']}/issues/comments/{comment_id}?access_token={config.get('gitee_token','') }"

    async with aiohttp.ClientSession() as session:
        async with session.delete(url) as response:
            if response.status in (200, 204):
                logger.info(f"Comment {comment_id} successfully deleted.")
            else:
                logger.info(
                    f"Failed to delete comment {comment_id}. Status code: {response.status}"
                )
                logger.info(f"Response: {await response.text()}")


async def post_comment(msg):
    url = f"{BASE}/repos/{config['owner']}/{config['repo']}/issues/{config['server_issue']}/comments?access_token={config.get('gitee_token','') }"
    payload = {"body": msg}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            if response.status in (200, 201):
                logger.info("Comment successfully created.")
                return await response.json()
            else:
                logger.info(f"Failed to create comment. Status code: {response.status}")
                logger.info(f"Response: {await response.text()}")
                return None


async def read_file(branch):
    url = f"{BASE}/repos/{config['owner']}/{config['repo']}/contents/server.txt?ref={branch}&access_token={config.get('gitee_token','') }"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                r = await response.json()
                return base64.b64decode(r["content"]).decode('utf-8')
            else:
                print("Failed to retrieve file")
                return None


async def push(branch, msg):
    url = f"{BASE}/repos/{config['owner']}/{config['repo']}/contents/client.txt?access_token={config.get('gitee_token','') }"
    content = base64.b64encode(msg.encode()).decode()
    payload = {
        "message": "SERVER",
        "content": content,
        "branch": branch
    }
    async with aiohttp.ClientSession() as session:
        async with session.put(url, json=payload) as response:
            response.raise_for_status()
