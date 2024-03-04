# Copyright 2024 Qewertyy, MIT License

from typing import Optional
import asyncio,base64,mimetypes,os
from lexica import AsyncClient
from lexica.constants import languageModels

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
        print(f"Failed to generate the image:",e)
    finally:
        await client.close()

async def UpscaleImages(image:bytes=None,image_url:str=None,format="url") -> dict:
    """
    Upscales an image and return with upscaled image path.
    """
    if not image and not image_url:
        raise Exception("Image or image_url is required")
    client = AsyncClient()
    content = await client.upscale(image,image_url,format)
    await client.close()
    return content['url']

async def ChatCompletion(prompt,model)  :
    modelInfo = getattr(languageModels,model)
    client = AsyncClient()
    output = await client.ChatCompletion(prompt,modelInfo)
    await client.close()
    if output['code'] == 0:
        return "I can't answer that."
    if model == "bard":
        return output['content'], output['images']
    return output['content']

async def geminiVision(prompt,model,images):
    imageInfo = []
    for image in images:
        with open(image,"rb") as imageFile:
            data = base64.b64encode(imageFile.read()).decode("utf-8")
            mime_type,_= mimetypes.guess_type(image)
            imageInfo.append({
                "data": data,
                "mime_type": mime_type
            })
        os.remove(image)
    payload = {
        "images":imageInfo
    }
    modelInfo = getattr(languageModels,model)
    client = AsyncClient()
    output = await client.ChatCompletion(prompt,modelInfo,json=payload)
    return output['content']['parts'][0]['text']

async def ReverseImageSearch(img_url,search_engine) -> dict:
    client = AsyncClient()
    output = await client.ImageReverse(img_url,search_engine)
    await client.close()
    return output

async def SearchImages(query,search_engine) -> dict:
    client = AsyncClient()
    output = await client.SearchImages(query,0,search_engine)
    await client.close()
    return output

async def DownloadMedia(platform,url) -> dict:
    client = AsyncClient()
    output = await client.MediaDownloaders(platform,url)
    await client.close()
    return output