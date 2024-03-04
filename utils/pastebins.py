# Copyright 2024 Qewertyy, MIT License

import httpx

NEKOBIN = "https://nekobin.com/api/documents"
async def nekobin(data,extension=None):
    """
    To Paste the given message/text/code to nekobin
    """
    try:
        async with httpx.AsyncClient() as req:
            res = req.post(
                url=NEKOBIN,
                json={
                    "content":data,
                    "title": "data",
                    "author": "SDWaifuRobot"
                })
    except Exception as e:
        return {"error": str(e)}
    if res.ok:
        resp = res.json()
        purl = (
            f"nekobin.com/{resp['result']['key']}.{extension}"
            if extension
            else f"nekobin.com/{resp['result']['key']}"
        )
        return purl
    return {"error": "Unable to reach nekobin."}