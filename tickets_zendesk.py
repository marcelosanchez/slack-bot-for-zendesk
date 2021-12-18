import datetime
# Import the Zenpy Class
import os
import json

from zenpy import Zenpy
from zenpy.lib.api_objects import Comment


class Ticket:
    ESTADO_OPEN    = "open"
    ESTADO_PENDING = "pending"
    ESTADO_CLOSED  = "closed"

    CANAL_WEB   = 'web'
    CANAL_EMAIL = 'email'

    def __init__(self, ticket_dict):
        self.id             = ticket_dict['id']
        self.fecha_creacion = ticket_dict['created_at']
        self.descripcion    = ticket_dict['description']
        self.estado         = ticket_dict['status']
        self.canal          = ticket_dict['via']['channel']
        self.estado         = ticket_dict['status']

    @classmethod
    def obtener_credenciales(cls):
        creds = {}
        with open('creds_zendesk.json') as data_file:
            data = json.load(data_file)
        creds = {
            'email': data['email'],
            'password': data['password'],
            'subdomain': data['subdomain']
        }
        return creds

    @classmethod
    def obtener_nuevos_tickets(cls):
        zenpy_client = Zenpy(**Ticket.obtener_credenciales())

        estados = [cls.ESTADO_OPEN]
        tickets = zenpy_client.search(type='ticket', status=estados)

        tickets_list = []
        for ticket in tickets:
            tickets_list.append(Ticket(ticket.to_dict()))
        print(str(len(tickets_list)) + " tickets nuevos!")
        return tickets_list

    def ticket_as_msg(self):
        texto = ":tique: *Ticket #" + str(self.id) + "*\n\n"
        texto += "Descripcion: \n"
        texto += "\n>" + str(self.descripcion)
        return texto

    def gestionar_ticket(self):
        zenpy_client = Zenpy(**Ticket.obtener_credenciales())
        ticket = zenpy_client.tickets(id=self.id)
        ticket.comment = Comment(body="Se cambió el estado del ticket, es necesario responderlo, lo más pronto posible.", public=False)
        ticket.status = 'pending'
        zenpy_client.tickets.update(ticket)

    def get_canal_display(self):
        if self.canal == Ticket.CANAL_EMAIL:
            return ":email: Email"
        elif self.canal == Ticket.CANAL_WEB:
            return ":computer: Web widget "
        else:
            return "Desconocido :alien:"

    def get_estado_display(self):
        if self.estado == Ticket.ESTADO_OPEN:
            return ":red_circle: Abierto"
        elif self.estado == Ticket.ESTADO_PENDING:
            return ":large_blue_circle: Pendiente"
        elif self.estado == Ticket.ESTADO_CLOSED:
            return ":alien: Cerrado"
        else:
            return ":white_circle: Desconocido"

    def get_fecha_display(self):
        return ":date: " + self.fecha_creacion

    def get_sitio_display(self):
        return "comextweb_logo: Comextweb - web_app"

    def get_descripcion_display(self):
        print(self.descripcion.splitlines(True))
        descripcion_mkd = self.descripcion
        # descripcion_mkd = descripcion_mkd.replace("\n", "\n\n>")
        # return '\n>' + descripcion_mkd
        return descripcion_mkd

    def dict_to_json_block(self):
        json_block = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":ticket: Ticket # " + str(self.id),
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Descipcion:*\n" + self.get_descripcion_display()
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Estado:*\n" + self.get_estado_display()
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Fecha de creacion:*\n" + self.get_fecha_display()
                    }
                ]
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Sitio:*\n:" + self.get_sitio_display()
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Canal:*\n" + self.get_canal_display()
                    }
                ]
            },
            # {
            #     "type": "section",
            #     "text": {
            #         "type": "mrkdwn",
            #         "text": "<https://www.google.com|Ir al enlace>"
            #     }
            # }
        ]
        return json_block
