#!/usr/bin/env python

import logging
import signal

from datetime import datetime
from time import sleep, ctime

from metahosting.common import argument_parsing, config_manager, logging_setup


class Updater(object):
    def __init__(self, config):
        persistence_class = \
            config_manager.get_backend_class(config['persistence'])
        messaging_class = \
            config_manager.get_backend_class(config['messaging'])

        self.messaging = messaging_class(config=config['messaging'],
                                         queue='status')
        self.datapoints = persistence_class(config=config['persistence'])
        self.running = False

    def start(self):
        self.running = True
        logging.info('Starting status updater %s', ctime())
        self.messaging.subscribe('status', self.store_datapoint)
        while self.running:
            logging.info('Heartbeat status updater %s', ctime())
            sleep(15)

    def stop(self, signal, stack):
        logging.info('Stopping status updater with signal %s', signal)
        self.running = False

    def store_datapoint(self, item):
        timestamp = item.pop('ts')
        item['ts'] = datetime.fromtimestamp(timestamp)
        logging.debug(item)
        self.datapoints.insert(item)

    def cleanup_old_entries(self, days=14):
        old = datetime.datetime.now() - datetime.timedelta(days=days)
        self.datapoints.delete_many({"ts": {"$lt": old}})


def run():
    arguments = argument_parsing()
    logging_setup(arguments=arguments)

    if arguments.config:
        config_manager._CONFIG_FILE = arguments.config
    if arguments.envfile:
        config_manager._VARIABLES_FILE = arguments.envfile

    config = dict()
    config['persistence'] = config_manager.get_configuration('persistence')
    config['messaging'] = config_manager.get_configuration('messaging')

    updater = Updater(config=config)

    signal.signal(signal.SIGTERM, updater.stop)
    signal.signal(signal.SIGHUP, updater.stop)
    signal.signal(signal.SIGINT, updater.stop)
    updater.start()

if __name__ == "__main__":
    run()
