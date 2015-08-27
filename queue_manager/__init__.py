import copy
import logging

from metahosting.common.config_manager import get_configuration
from queue_manager.rabbit import BlockingPikaManager


manager = dict()


def set_manager(queues=None):
    config = get_configuration('messaging')
    if 'host' in config and 'port' in config \
            and 'user' in config and 'port' in config:
        global manager
        manager[queues] = BlockingPikaManager(host=config['host'],
                                              port=int(config['port']),
                                              user=config['user'],
                                              password=config['pass'],
                                              queue=queues)
    else:
        logging.error('Configuration parameters for messaging missing')


def get_manager(queue=None):
    global manager
    if not manager or queue not in manager:
        set_manager(queues=queue)
    return manager[queue]


def send_message(routing_key, subject, message):
    msg = copy.copy(message)
    msg['subject'] = subject
    get_manager(queue=routing_key).publish(routing_key, msg)


def get_message_subject(message):
    if 'subject' not in message:
        return None
    return message.pop('subject')


def subscribe(routing_key, callback):
    get_manager(queue=routing_key).subscribe(routing_key, callback)
