
async def Notifall(msg: dict, users):
    for ws in users:
        try:
            await ws.send_json(msg)
        except:
            pass