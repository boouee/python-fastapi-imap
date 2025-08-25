import httpx

async def webhook_handler(request):
  async with httpx.AsyncClient() as client:
    company = await get_company(client, comment)
    await send_notification(client, company)

async def get_company(client, comment):
  response = await client.get(f"{api}crm.timeline.comment.get?id={comment}")
  response = response.json()
  return response["result"]["ENTITY_ID"]

async def send_notification(client, company):
  data = {"USER_ID": 1, "MESSAGE": f"Новый комментарий на {company}"}
  response = await client.post(f"{api}im.notify.system.add", json=data)
  response = response.json()
  return response["result"]["ENTITY_ID"]
