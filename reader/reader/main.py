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

    if not message_list and not message:
        response = {
            'response': None,
            'status': 404,
        }
    else:
        response = {
            'response': (
                message.to_dict() if message
                else [message.to_dict() for message in message_list]
            ),
            'status': 200,
        }

    return response


@dispatcher.add_method
def persona(address=None, nickname=None, pubkey=None) -> dict:
    """persona

    Retrieves a persona's data from HBase
    according to the given filters

    :param address: ASCII representation of the user's address
    :param nickname: Nickname given to the persona
    :param pubkey: ASCII represnetation of the user's pubkey
    :rtype: dict
    """
    _persona = None

    if address:
        _persona = Persona.get(address=address)
    if nickname:
        _persona = Persona.get(nickname=nickname)
    if pubkey:
        _persona = Persona.get(pubkey=pubkey)

    if not _persona:
        response = {
            'response': None,
            'status': 404,
        }
    else:
        response = {
            'response': _persona.to_dict(),
            'status': 200,
        }

    return response


@Request.application
def application(request):
    """application

    Main app function.

    :param request: werkzeug.Request
    """

    response = JSONRPCResponseManager.handle(request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    run_parameters = {
        'hostname': '0.0.0.0',
        'port': PORT,
        'application': application,
        'use_reloader': True if ENVIRONMENT == 'DEVELOPMENT' else False
    }

    run_simple(**run_parameters)
