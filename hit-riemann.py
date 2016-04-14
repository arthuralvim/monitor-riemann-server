# -*- coding: utf-8 -*-

from bernhard import Client as RiemannClient
from decouple import config
import collections
import datetime
import logging
import random
import string

LEVELS = {'DEBUG': logging.DEBUG,
          'INFO': logging.INFO,
          'WARNING': logging.WARNING,
          'ERROR': logging.ERROR,
          'CRITICAL': logging.CRITICAL}

LOG_LEVEL = config('LOG_LEVEL', default='DEBUG')
LOG_FILENAME = config('LOG_FILENAME', default='hit-riemann.log')
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(LEVELS.get(LOG_LEVEL, logging.NOTSET))


def lucky(threshold=0.5):
    return random.random() > threshold


fields = ['service', 'state', 'host', 'metric', 'description', 'tags']
Event = collections.namedtuple('Event', fields)


class GenerateRandom(object):

    def choose_one(self, choices):
        return random.sample(choices, 1)[0]

    def choose_sample(self, choices, size):
        return random.sample(choices, size)

    def number(self, mini=1, maxi=100):
        return random.randint(mini, maxi)

    def string(size):
        return ''.join([random.choice(string.letters) for i in xrange(size)])

    def alphanumeric(size):
        return ''.join([random.choice(string.letters + string.digits)
                       for i in xrange(size)])

    def datetime(span=0):
        return (datetime.date.today() +
                datetime.timedelta(days=span)).isoformat()


class EventRandom(GenerateRandom):

    event_states = ['critical', 'ok', 'warning']
    event_tags = ['web', 'worker', 'db', 'spider']

    def service(self, service_type='mservice', seq=1):
        return '{0}-{1}'.format(service_type, str(seq))

    def state(self, state='critical'):
        return self.choose_one(self.event_states)

    def host(self, host_type='www', seq=1):
        return '{0}-{1}'.format(host_type, str(seq))

    def metric(self):
        return self.number()

    def description(self, metric=None):
        if metric is None:
            metric = self.metric()
        return "{0} problems occurred.".format(metric)

    def tags(self, size=2):
        return self.choose_sample(self.event_tags, size)

    def event(self, nr_services=1, nr_hosts=1):
        metric = self.metric()
        return Event(self.service(seq=self.number(maxi=nr_services)),
                     self.state(),
                     self.host(seq=self.number(maxi=nr_hosts)),
                     metric,
                     self.description(metric),
                     self.tags())


class RiemannPayload(object):

    HOST = config('RIEMANN_HOST', default='33.33.33.30')
    PORT = config('RIEMANN_PORT', default=5555, cast=int)

    @property
    def client(self):
        if not hasattr(self, '_client'):
            self._client = RiemannClient(self.HOST, self.PORT)
        return self._client

    def get_random_payload(self):
        return EventRandom().event()

    def loop(self, verbose=1):
        while True:
            if lucky():
                event = self.get_random_payload()
                if verbose != 1:
                    logger.debug(event)
                    print event
                else:
                    print event
                self.client.send(event._asdict())

if __name__ == '__main__':
    rie = RiemannPayload()
    rie.loop(2)
