# -*- coding: utf-8 -*-

from bernhard import Client as RiemannClient
from decouple import config
import datetime
import random
import string
import collections


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

    def tags(self, size=1):
        return self.choose_sample(self.event_tags, 3)

    def event(self):
        return Event(self.service(seq=self.number(maxi=4)),
                     self.state(),
                     self.host(seq=self.number(maxi=10)),
                     self.metric(),
                     self.description(),
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

    def loop(self, verbose=False):
        while True:
            if lucky():
                event = self.get_random_payload()
                if verbose:
                    print event
                self.client.send(event._asdict())

if __name__ == '__main__':
    rie = RiemannPayload()
    rie.loop(True)
