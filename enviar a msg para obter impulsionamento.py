import asyncio
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
from datetime import datetime, time as dt_time
import pytz

# Chaves da API e hash
api_id = '23086885'
api_hash = 'e5f10927e4b619d2dc707d02c80b4855'

# IDs dos grupos onde você deseja enviar a mensagem
group_ids = [-1001185761601, -1001251469780, -1002163506736, -1001123272694, -1002180118622, -1002182314112, -1001577484978]

# Mensagem a ser enviada para os grupos
group_message = " Vamos se ajudar ? Me manda privado que retribuo na hora \n\n Desafio de futebol desconto Aliexpress\n Oi amigo! Me ajude a obter mais créditos com apenas 1 clique\n https://a.aliexpress.com/_mMGJPRm "

# Mensagem a ser enviada em resposta às mensagens privadas
private_message = ("Pronto te ajudei, ajuda ai entra no nosso grupo de mandar link do joguinho, "
                   "la tem mais 350 pessoas pra vc compartilhar. https://t.me/ofertasgamerjogos")

# Função para enviar a mensagem para os grupos
async def send_message(client, chat_id, text):
    await client.send_message(chat_id, text)

# Função para verificar se está no horário de funcionamento
def is_within_operating_hours():
    tz = pytz.timezone('America/Sao_Paulo')
    now = datetime.now(tz).time()
    start_time = dt_time(8, 0)
    end_time = dt_time(2, 0)
    return (start_time <= now or now < end_time)

# Função principal para enviar a mensagem para todos os grupos
async def main():
    # Inicializa o cliente do Telegram
    client = TelegramClient('session_name', api_id, api_hash)
    
    await client.start()

    # Conjunto para rastrear usuários que já receberam uma resposta
    responded_users = set()

    # Handler para novas mensagens privadas
    @client.on(events.NewMessage(incoming=True))
    async def handle_private_message(event):
        if event.is_private:
            if event.sender_id not in responded_users:
                try:
                    await event.respond(private_message)
                    responded_users.add(event.sender_id)
                    print(f"Respondido para {event.sender_id}")
                except FloodWaitError as e:
                    print(f"Flood wait error: aguarde {e.seconds} segundos")
                    await asyncio.sleep(e.seconds)
                    await event.respond(private_message)
                    responded_users.add(event.sender_id)
                    print(f"Respondido para {event.sender_id} após espera")

    while True:
        if is_within_operating_hours():
            try:
                # Envia a mensagem para cada grupo
                for group_id in group_ids:
                    await send_message(client, group_id, group_message)
                    
                print("Mensagem enviada para todos os grupos.")
                
                # Contagem regressiva de 5 minutos (atualizada a cada minuto)
                for remaining in range(10, 0, -1):  # 5 minutos em minutos
                    print(f'Próxima mensagem em {remaining} minutos', end='\r')
                    await asyncio.sleep(60)  # Espera 1 minuto
            except Exception as e:
                print("Ocorreu um erro:", e)
        else:
            print("Fora do horário de funcionamento. Aguardando para iniciar...")
            await asyncio.sleep(60)  # Verifica novamente em 1 minuto

if __name__ == "__main__":
    asyncio.run(main())
