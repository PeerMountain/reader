import os

from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher
from himalaya_models import Message, Persona


class Container:
    @classmethod
    def get(cls, **kwargs):
        return None


# Port should be 8000 for all internal web services.
PORT = 8000


@dispatcher.add_method
def messages(message_hash=None, reader=None, date=None) -> dict:
    """messages

    Retrieves a message or list of messages from HBase
    according to the given filters.

    :param message_hash: Hash of the message
    :param reader: Reader of the messages
    :param date: Date the messages were created
    :rtype: dict
    """
    message = message_list = None
    if message_hash:
        message = Message.get(message_hash=message_hash)
    elif reader:
        message_list = Message.filter(reader=reader)
    elif date:
        message_list = Message.filter(date=date)
    if not (message or message_list):
        raise Exception("Message not found")
    return {
        'response': (
            message.to_dict() if message
            else [message.to_dict() for message in message_list]
        ),
        'status': 200,
    }


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


@dispatcher.add_method
def container(container_hash) -> dict:
    _container = Container.get(container_hash=container_hash)
    if not _container:
        raise Exception("Container not found")
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
