import collections
import optparse
import os

import unicodecsv as csv

from django.core.management import BaseCommand
from django.db import connection

from projections.models import Batting, Pitching


Types = {
    'batting': Batting,
    'pitching': Pitching,
}


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        optparse.make_option('-t', dest='type'),
        optparse.make_option('-s', dest='steamer'),
        optparse.make_option('-z', dest='zips'), )

    def handle(self, **opts):
        if not opts['type'] in Types:
            exit(u'Error: -t must be one of {%s}' % ', '.join(Types))

        self.cursor = connection.cursor()
        self.players = collections.defaultdict(list)

        Model = Types[opts['type']]
        method = getattr(self, opts['type'])

        # wipe what we have
        Model.objects.filter().delete()

        # coalesce projections by player
        reader = csv.DictReader(open(opts['zips'], 'rb'))

        for row in reader:
            method(row)

        # wrap up
        connection.commit()

    def batting(self, row):
        self.cursor.execute("""
insert into projections_batting (
        playerid, name, pos, is_kept,
        g, pa, ab, h, hr,
        r, rbi, bb, so, hbp,
        sb, cs, avg, obp, slg,
        tb, woba
) values (
        %(playerid)s, %(Name)s, null, 'f',
        %(G)s, %(PA)s, %(AB)s,
        %(H)s, %(HR)s, %(R)s, %(RBI)s, %(BB)s,
        %(SO)s, %(HBP)s, %(SB)s, %(CS)s, %(AVG)s,
        %(OBP)s, %(SLG)s,
        (
            %(H)s::numeric
            + (%(2B)s::numeric * 2)
            + (%(3B)s::numeric * 3)
            + (%(HR)s::numeric * 4)
        ),
        %(wOBA)s
)
""", row)

    def pitching(self, row):
        self.cursor.execute("""
insert into projections_pitching (
        playerid, name, pos, is_kept,
        w, l, era, sv, bs,
        ip, h, er, hra, so,
        bb, whip, k9, bb9,

        -- non-native fields
        qs, hd, cg, sh
) values (
        %(playerid)s, %(Name)s, null, 'f',
        %(W)s, %(L)s, %(ERA)s, null, null,
        %(IP)s, %(H)s, %(ER)s, %(HR)s, %(SO)s,
        %(BB)s, %(WHIP)s, %(K/9)s, %(BB/9)s,

    -- quality starts via https://bit.ly/1kztmPq
    case
      when %(GS)s::numeric > 0
        then (((%(IP)s::numeric / %(GS)s::numeric) / 6.15) - (.11 * %(ERA)s::numeric)) * %(GS)s::numeric
      else 0
    end,

    null, null, null
)
        """, row)
