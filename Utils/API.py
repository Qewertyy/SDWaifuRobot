# Copyright 2023 Qewertyy, MIT License
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

async def UpscaleImages(image: bytes) -> str:
    """
    Upscales an image and return with upscaled image path.
    """
    client = AsyncClient()
    content = await client.upscale(image)
    await client.close()
    upscaled_file_path = "upscaled.png"
    with open(upscaled_file_path, "wb") as output_file:
        output_file.write(content)
    return upscaled_file_path

async def ChatCompletion(prompt,model) -> tuple | str :
    modelInfo = getattr(languageModels,model)
    client = AsyncClient()
    output = await client.ChatCompletion(prompt,modelInfo)
    await client.close()
    if model == "bard":
        return output['content'], output['images']
    return output['content']

async def geminiVision(prompt,model,images) -> tuple | str :
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