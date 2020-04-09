# FIFO = # First In - First Out (Primer en Entrar - Primero en Salir)
# Debo eliminar siempre el primero de la lista

# LIFO = # Last In - First Out (Ultimo en Entrar - Primero en Salir)
# Debo eliminar siempre el ultimo de la lista
from twilio.rest import Client


class Queue:

    def __init__(self):
        self.account_sid = 'AC0a1b31ffe7b3be4b6cbd1d2502a43eac'
        self.auth_token = '985da92d6240de8b8c1904cc42a00800'
        self.client = Client(self.account_sid, self.auth_token)
        self._queue = []
        # depending on the _mode, the queue has to behave like a FIFO or LIFO
        self._mode = 'FIFO'

    def enqueue(self, item):
        self._queue.append(item)

        message = self.client.messages.create(
            to="+" + str(item["telefono"]),
            from_="+56937830831",
            body="Bienvenido " + item["nombre"] + " " + item["apellido"] + ", hay cola de " + str(self.size()-1)+" personas frente a ti.")

        return True

    def dequeue(self):
        
        if self._mode == "FIFO":

            message = self.client.messages.create(
                to="+" + str(self._queue[0]["telefono"]),
                from_="+56937830831",
                body=self._queue[0]["nombre"] + " " + self._queue[0]["apellido"] + ", Tu Numero ha llegado te antederemos inmediatamente")
            self._queue.pop(0)
            return True

        if self._mode == "LIFO":

            message = self.client.messages.create(
                to="+" + str(self._queue[0]["telefono"]),
                from_="+56937830831",
                body=self._queue[0]["nombre"] + " " + self._queue[str(self.size()-1)]["apellido"] + ", Tu Numero ha llegado te antederemos inmediatamente")
            self._queue.pop()
            return True
            
        else:
            return False

    def get_queue(self):
        return self._queue

    def size(self):
        return len(self._queue)


'''
message = client.messages.create(
         body="Join Earth's mightiest heroes. Like Kevin Bacon.",
         to='+15558675310'
     )

print(message)


{
  "account_sid": "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "api_version": "2010-04-01",
  "body": "Join Earth's mightiest heroes. Like Kevin Bacon.",
  "date_created": "Thu, 30 Jul 2015 20:12:31 +0000",
  "date_sent": "Thu, 30 Jul 2015 20:12:33 +0000",
  "date_updated": "Thu, 30 Jul 2015 20:12:33 +0000",
  "direction": "outbound-api",
  "error_code": null,
  "error_message": null,
  "from": "+14155552345",
  "messaging_service_sid": "MGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "num_media": "0",
  "num_segments": "1",
  "price": null,
  "price_unit": null,
  "sid": "MMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "status": "sent",
  "subresource_uris": {
    "media": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Messages/SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Media.json"
  },
  "to": "+15558675310",
  "uri": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Messages/SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.json"
}

'''
