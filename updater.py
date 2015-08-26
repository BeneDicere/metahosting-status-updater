#!/usr/bin/env python

from datetime import datetime
from metahosting.common import argument_parsing, logging_setup
from metahosting.common.config_manager \
    import get_backend_class, get_configuration
from queue_manager import subscribe
from time import sleep, ctime

import argparse
import logging
import signal

class Updater(object):
    def __init__(self, config):
        persistence_class = get_backend_class(config)
        self.datapoints = persistence_class(config=config)
        self.running = False

    def start(self):
        self.running = True
        logging.info('Starting status updater %s', ctime())
        subscribe('status', self.store_datapoint)
        while self.running:
            logging.info('Heartbeat status updater %s', ctime())
            sleep(15)

    def stop(self, signal, stack):
        logging.info('Stopping status updater with signal %s', signal)
        self.running = False

    def store_datapoint(self, item):
        timestamp = item.pop('ts')
        item['date'] = datetime.fromtimestamp(timestamp)
        logging.debug(item)
        self.datapoints.insert(item)

    def cleanup_old_entries(self, days=14):
        old = datetime.datetime.now() - datetime.timedelta(days=days)
        self.datapoints.delete_many({"date": {"$lt": old}})


def run():
    arguments = argument_parsing()
    logging_setup(arguments=arguments)
    config = get_configuration('persistence')
    updater = Updater(config=config)

    signal.signal(signal.SIGTERM, updater.stop)
    signal.signal(signal.SIGHUP, updater.stop)
    signal.signal(signal.SIGINT, updater.stop)
    updater.start()

if __name__ == "__main__":
    run()
