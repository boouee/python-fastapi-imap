import httpx

api = "https://b24-d1uwq7.bitrix24.ru/rest/1/2ylw0cg8hm7u5ef4/"

async def new_comment_handler(comment):
  async with httpx.AsyncClient() as client:
    company = await get_company_id(client, comment)
    title = await get_company_name(client, company)
    await send_notification(client, company, title)

async def get_company_id(client, comment):
  response = await client.get(f"{api}crm.timeline.comment.get?id={comment}")
  response = response.json()
  return response["result"]["ENTITY_ID"]

async def send_notification(client, company, title):
  data = {"USER_ID": 1, "MESSAGE": f"Новый комментарий на [URL=https://b24-d1uwq7.bitrix24.ru/crm/company/details/{company}/]{title}[/URL]"}
  response = await client.post(f"{api}im.notify.system.add", json=data)
  response = response.json()
  return response["result"]["ENTITY_ID"]

async def get_company_name(client, company):
  response = await client.get(f"{api}crm.company.get?id={company}")
  response = response.json()
  return response["result"]["TITLE"]
