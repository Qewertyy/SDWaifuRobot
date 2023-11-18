# Copyright 2023 Qewertyy, MIT License
import asyncio
from lexica import AsyncClient

async def ImageGeneration(model,prompt):
    try:
        client = AsyncClient()
        output = await client.generate(model,prompt,"")
        if output['code'] != 1:
            return 2
        elif output['code'] == 69:
            return output['code']
        task_id, request_id = output['task_id'],output['request_id']
        await asyncio.sleep(20)
        tries = 0
        image_url = None
        resp = await client.getImages(task_id,request_id)
        while True:
            if resp['code'] == 2:
                image_url = resp['img_urls']
                break
            if tries > 15:
                break
            await asyncio.sleep(5)
            resp = await client.getImages(task_id,request_id)
            tries += 1
            continue
        return image_url
    except Exception as e:
        raise Exception(f"Failed to generate the image: {e}")
    finally:
        await client.close()

async def UpscaleImages(image: bytes) -> str:
    """
    Upscales an image and return with upscaled image path.
    """
    try:
        client = AsyncClient()
        content = await client.upscale(image)
        await client.close()
        upscaled_file_path = "upscaled.png"
        with open(upscaled_file_path, "wb") as output_file:
            output_file.write(content)
        return upscaled_file_path
    except Exception as e:
        raise Exception(f"Failed to upscale the image: {e}")

async def gpt(prompt) -> str:
    try:
        client = AsyncClient()
        output = await client.gpt(prompt)
        await client.close()
        return output['content']
    except Exception as E:
        raise Exception(f"API error: {E}")

async def bard(prompt) -> str:
    try:
        client = AsyncClient()
        output = await client.bard(prompt)
        await client.close()
        return output['content'],output['images']
    except Exception as E:
        raise Exception(f"API error: {E}")