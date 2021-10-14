import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)
spam_chats = []

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply(
    "__**Olá eu sou 𖤘 ⃝𝑴 ᩠𝒆 ᩠𝒏 ᩠𝒕 ᩠𝒊 ᩠𝒐 ᩠𝒏 ⿻ꦿꪳ։ 𝑨 ᩠𝒍 ᩠𝒍৴ํฺ͘.•🛸 ݈݇─𖤘 ⃝**, Eu sou um chamador de todos os membros, infernizar pouquin 👻\nClique no **/help** para mais informações ademir__\n\n Chegue no meu canal aí brodi ➜ [@GR4V3_S4D_CRAZZY](https://t.me/GR4V3_S4D_CRAZZY)",
    link_preview=False,
    buttons=(
      [
        Button.url('🤺 Canal', 'https://t.me/RabiscoS_MeuS_77'),
        Button.url('⚙️ Musics', 'https://t.me/GR4V3_S4D_CRAZZY')
      ]
    )
  )

@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**⚙️ Menu de comandos do 𖤘 ⃝𝑴 ᩠𝒆 ᩠𝒏 ᩠𝒕 ᩠𝒊 ᩠𝒐 ᩠𝒏 ⿻ꦿꪳ։ 𝑨 ᩠𝒍 ᩠𝒍৴ํฺ͘.•🛸 ݈݇─𖤘 ⃝**\n\nComando: /mentionall\n__Você usa o comando + texto para mencionar o pessoal ou então não precisa mandar algo só por o comando.__\n`Examplo: /mentionall Boa noite é o caralho!`\n__Bem simples, mas você também consegue chamar marcando em uma mensagem. __.\n\nEnfim, bot criado pelo [•𝘊𝘳𝘪𝘢𝘥𝘰𝘳•](https://t.me/xPV_D4_M34_S4Y0R1_D3M0N_CR4ZZYx)"
  await event.reply(
    helptext,
    link_preview=False,
    buttons=(
      [
        Button.url('🤺 Canal', 'https://t.me/RabiscoS_MeuS_77'),
        Button.url('⚙️ Musics', 'https://t.me/GR4V3_S4D_CRAZZY')
      ]
    )
  )
  
@client.on(events.NewMessage(pattern="^/mentionall ?(.*)"))
async def mentionall(event):
  chat_id = event.chat_id
  if event.is_private:
    return await event.respond("__O comando só pode ser usado em grupos ou canais, ademiro!__")
  
  is_admin = False
  try:
    partici_ = await client(GetParticipantRequest(
      event.chat_id,
      event.sender_id
    ))
  except UserNotParticipantError:
    is_admin = False
  else:
    if (
      isinstance(
        partici_.participant,
        (
          ChannelParticipantAdmin,
          ChannelParticipantCreator
        )
      )
    ):
      is_admin = True
  if not is_admin:
    return await event.respond("__Apenas administradores pode usar o bot!__")
  
  if event.pattern_match.group(1) and event.is_reply:
    return await event.respond("__Me envie um argumento!__")
  elif event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.is_reply:
    mode = "text_on_reply"
    msg = await event.get_reply_message()
    if msg == None:
        return await event.respond("__Não posso mencionar uma mensagem antiga para os membros! (Mande a mensagem antes de eu ser adicionado)__")
  else:
    return await event.respond("__Marque a vossa mensagem, para que eu retribua a mensagem para todos!__")
  
  spam_chats.append(chat_id)
  usrnum = 0
  usrtxt = ''
  async for usr in client.iter_participants(chat_id):
    if not chat_id in spam_chats:
      break
    usrnum += 1
    usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
    if usrnum == 5:
      if mode == "text_on_cmd":
        txt = f"{usrtxt}\n\n{msg}"
        await client.send_message(chat_id, txt)
      elif mode == "text_on_reply":
        await msg.reply(usrtxt)
      await asyncio.sleep(2)
      usrnum = 0
      usrtxt = ''
  try:
    spam_chats.remove(chat_id)
  except:
    pass

@client.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
  if not event.chat_id in spam_chats:
    return await event.respond('__Não há processo em andamento...__')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.respond('__Parei.__')

print(">> BOT STARTED <<")
client.run_until_disconnected()
