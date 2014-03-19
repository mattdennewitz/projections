"""Imports position data from CBS
"""

from __future__ import unicode_literals
import optparse
import os

import unicodecsv as csv

from django.core.management import BaseCommand
from django.db import connection

from projections.models import Batting, Pitching


TABLES = {
    'pitching': Pitching._meta.db_table,
    'batting': Batting._meta.db_table,
}


realpath = lambda p: os.path.realpath(os.path.expanduser(p))


def get_file(option, cmd_arg, value, parser):
    path = realpath(value)

    if not os.path.isfile(path):
        raise optparse.OptionError('%s is not a file' % value,
                                   option)

    parser.values.input = open(path, 'rb')


def get_player_data(value):
    """Decomposes player CBS-formatted names fields to
    <first last>, team, and position.
    """

    bits = value.split()
    team, pos = bits.pop(), bits.pop()

    # recombine name
    name_bits = map(lambda v: v.strip(), ' '.join(bits).split(','))
    last, first = name_bits
    name = first + ' ' + last

    return name, team, pos


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        optparse.make_option('-i', type='string',
                             action='callback',
                             callback=get_file),
        optparse.make_option('-t', dest='type', choices=TABLES.keys()),
    )

    def handle(self, **opts):
        self.cursor = connection.cursor()
        self.type_ = opts['type']

        data = csv.DictReader(opts['input'])
        sync_method = getattr(self, opts['type'])

        for row in data:
            name, team, pos = get_player_data(row['Player'])

            q = 'select count(*) from {table} where name = %s'.format(
                table = TABLES[opts['type']])

            self.cursor.execute(q, (name, ))
            count = self.cursor.fetchone()[0]

            if count > 1:
                print(name, team, pos, count)
                continue

            # sync cbs data with player
            sync_method(name, pos, team, row)

        # all done
        connection.commit()

    def batting(self, name, pos, team, row):
        q = 'update {table} set pos = %(pos)s where name = %(name)s'.format(
            table = TABLES[self.type_])
        self.cursor.execute(q, {'pos': pos, 'name': name})

    def pitching(self, name, pos, team, row):
        q = """
update {table}
set
        pos = %(pos)s,
        sv = %(sv)s,
        bs = %(bs)s,
        hd = %(hd)s,
        cg = %(cg)s,
        sh = %(sh)s
where name = %(name)s
"""
        q = q.format(table = TABLES[self.type_])

        self.cursor.execute(q, {
            'pos': pos,
            'sv': row['S'],
            'bs': row['BS'],
            'hd': row['HD'],
            'cg': row['CG'],
            'sh': row['SO'],
            'name': name,
        })
