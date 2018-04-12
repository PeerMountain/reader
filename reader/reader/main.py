import os

from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher

from himalaya_models import Message, Persona
from settings import PORT, ENVIRONMENT 


@dispatcher.add_method
def message(hash=None, persona_sender=None, created_at=None) -> dict:
    """messages

    Retrieves a message or list of messages from HBase
    according to the given filters.

    :param hash: Hash of the message
    :param persona_sender: Reader of the messages
    :param created_at: Date the messages were created
    :rtype: dict
    """

    message = message_list = None

    if hash:
        message = Message.get(hash=hash)

    if persona_sender:
        message_list = Message.filter(persona_sender=persona_sender)

    if created_at:
        message_list = Message.filter(created_at=created_at)

    if not (message or message_list):
        raise Exception('Message not found')

    response = {
        'response': (
            message.to_dict() if message
            else [message.to_dict() for message in message_list]
        ),
        'status': 200,
    }

    return response


@dispatcher.add_method
def persona(address=None, nickname=None) -> dict:
    """persona

    Retrieves a persona's data from HBase
    according to the given filters

    :param address: ASCII representation of the user's address
    :param nickname: Nickname given to the persona
    :rtype: dict
    """
    _persona = Persona.get(address=address) or Persona.get(nickname=nickname)
    if not _persona:
        raise Exception("Persona not found")
    return {
        'response': _persona.to_dict(),
        'status': 200,
    }


    return {
        'response': _container.to_dict(),
        'status': 200,
    }


@Request.application
def application(request):
    """application

    Main app function.

    :param request: werkzeug.Request
    """
    response = JSONRPCResponseManager.handle(request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    run_simple('0.0.0.0', PORT, application)
