import os
import asyncio

from tickets_zendesk import Ticket
from slack_integration import Slack

channel = os.environ['BOT_CHANNEL']


async def tickets_monitor():
    while True:
        print("** Buscando nuevos tickets")
        tickets_list = Ticket.obtener_nuevos_tickets()
        slack = Slack()
        for ticket in tickets_list:
            ticket_id = ticket.id
            slack.send_messange_to_slack_channel(channel_name=channel, message=ticket.ticket_as_msg(), json_block_msg=ticket.dict_to_json_block())
            ticket.gestionar_ticket()
            print("[Ticket # " + str(ticket_id) + "] Notificado en el canal #" + str(channel))
        print("** Fin de la busqueda")
        await asyncio.sleep(60)  # 60

loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(tickets_monitor())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Finalizando Loop")
    loop.close()
