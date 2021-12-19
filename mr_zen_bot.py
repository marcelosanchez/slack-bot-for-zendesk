import os
import asyncio
from datetime import datetime

from tickets_zendesk import Ticket
from slack_integration import Slack

channel = os.environ['BOT_CHANNEL']


async def tickets_monitor():
    TIEMPO_ESPERA = 60
    while True:
        print("[" + str(datetime.now()) + "] ** Buscando nuevos tickets")
        tickets_notificados = 0
        tickets_list = Ticket.obtener_nuevos_tickets()
        slack = Slack()
        for ticket in tickets_list:
            ticket_id = ticket.id
            if not ticket.fue_notificado():  # Bug notificacion estado pendiente
                slack.send_messange_to_slack_channel(channel_name=channel, message=ticket.ticket_as_msg(), json_block_msg=ticket.dict_to_json_block())
                ticket.gestionar_ticket()
                print("[Ticket # " + str(ticket_id) + "] Notificado en el canal #" + str(channel))
                tickets_notificados += 1
        print(str(tickets_notificados) + " tickets notificados!")
        print("[" + str(datetime.now()) + "] ** Fin de la busqueda")
        await asyncio.sleep(TIEMPO_ESPERA)  # Tiempo de espera

loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(tickets_monitor())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Finalizando Loop")
    loop.close()
