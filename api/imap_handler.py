from imap_tools import MailBox, AND
import httpx
import re

address = "crm@apexdiabetes.ru"
password = "1Mcl552smPjUsPXu"
server = "mail.netangels.ru"
#email - UF_CRM_1723114805999
#name - UF_CRM_1723114789182
#phone - UF_CRM_1723114796732
api = "https://b24-d1uwq7.bitrix24.ru/rest/1/2ylw0cg8hm7u5ef4/"
block_id_values = {'rec1158004176': 'UC_JJAT3O', 'rec1151357361': 'STORE' , '#rec1206105936': 'WEB' , '#rec860376858': 'UC_LC50KQ' }
#block_id_values = {'rec1158004176': '572', 'rec1151357361': '31' , '#rec1206105936': '15' , '#rec860376858': '574' }

# Get date, subject and body len of all emails from INBOX folder
async def imap_handler():
    with MailBox(server).login(address, password) as mailbox:
        for f in mailbox.folder.list():
            print(f)
        uids = []
        for msg in mailbox.fetch():
            try:
              print(msg.date, msg.subject, len(msg.text or msg.html))
              #print(msg.html)
              html = str(msg.html)
              print(len(html))
              print("Name" in html)
              name = re.findall("Name:(.*)<br>", html)
              name = "" if not name else name[0]
              phone = re.findall("Phone:(.*)<br>", html)
              phone = "" if not phone else phone[0]
              email = re.findall("Email:(.*)<br>", html)
              if len(email) < 1:
                 email = re.findall("Textarea:(.*)<br>", html)
                 email = "" if not email else email[0]
              else:
                 email = email[0]
              print(name, phone, email)
              block_ID = re.findall("Block ID:([^\\s]*)<br>", html)
              block_ID = "" if not block_ID else block_id_values[block_ID[0]]
              
              comments = re.findall("Input:(.*)<br>", html)
              comments = "" if not comments else comments[0]
              input_2 = re.findall("Input_2:(.*)<br>", html)
              if len(input_2) > 0:
                comments += ("\n" + input_2[0])
              #+ "\n" + re.findall("Input_2:(.*)<br>", html)
              print(name, phone, email, comments)
              mailbox.move(msg.uid, "INBOX.Trash")
              await create_deal(name, phone, email, comments)
            except Exception as e:
              print(e)

async def create_deal(name, phone, email, comments):
    async with httpx.AsyncClient() as client:
        data = {"fields": {"TITLE": name, "CATEGORY_ID": 12, "UF_CRM_1723114789182": name, "UF_CRM_1723114805999": email, "UF_CRM_1723114796732": phone, "COMMENTS": comments, "ASSIGNED_BY_ID": 1, "SOURCE_ID": block_ID  }}
        response = await client.post(f"{api}crm.deal.add", json=data)
        print(response.json())

async def get_data(text):
    print("#")
