from __future__ import unicode_literals
import collections
import json
import operator
import optparse
import os
import pprint

import unicodecsv as csv

from django.core.management import BaseCommand
from django.db import connection

from projections.models import Player, Batting, Pitching
from projections.raw import Container, BattingSchema, PitchingSchema


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        optparse.make_option('-c', dest='config'), )

    def handle(self, **opts):
        config = json.load(open(opts['config'], 'r'))

        self.cursor = connection.cursor()

        players = {}

        Batting.objects.filter().delete()
        Pitching.objects.filter().delete()

        # coalesce projections by player
        for system in config['projections']:
            for p_type in system['types']:
                path = system['types'][p_type]['path']
                reader = csv.DictReader(open(path, 'r'))

                for row in reader:
                    # set container for player/type if missing
                    if not row['playerid'] in players:
                        obj = Container()
                        obj.import_data(row, strict=False)
                        players[row['playerid']] = obj

                    # add projection
                    proj_cls = (PitchingSchema if p_type[0] == 'p'
                                else BattingSchema)
                    proj_obj = proj_cls()
                    proj_obj.import_data(row, strict=False)
                    dest = getattr(players[row['playerid']],
                                   p_type + '_projections')
                    proj_obj.validate()
                    dest.append(proj_obj)

                # ensure container is properly constructed
                players[row['playerid']].validate()

        # average out stats
        for player in players:
            for p_type in ('batting', 'pitching'):
                player_data = {
                    'name': players[player].name,
                    'pos': players[player].pos,
                    'is_kept': players[player].is_kept,
                    'playerid': players[player].playerid,
                }

                projs = getattr(players[player], p_type + '_projections')
                if not projs:
                    continue

                stats = collections.defaultdict(list)

                # collect each stat-value
                for proj in projs:
                    data = proj.serialize()
                    for stat in data:
                        stats[stat].append(data[stat])

                # reduce component stat collection into single value
                for stat in stats:
                    values = map(float, filter(lambda v: v is not None,
                                               stats[stat]))
                    if values:
                        value = reduce(operator.add, values) / len(values)
                    else:
                        value = 0.

                    player_data[stat] = value

                # store results for projection type
                try:
                    getattr(self, p_type)(player_data)
                except KeyError:
                    print p_type
                    pprint.pprint(player_data)
                    raise

        # wrap up
        connection.commit()

    def batting(self, row):
        self.cursor.execute("""
insert into projections_batting (
        playerid, name, pos, is_kept,
        pa, ab, h, hr,
        r, rbi, bb, so, hbp,
        sb, cs, avg, obp, slg,
        tb
) values (
        %(playerid)s, %(name)s, null, 'f',
        %(PA)s, %(AB)s,
        %(H)s, %(HR)s, %(R)s, %(RBI)s, %(BB)s,
        %(SO)s, %(HBP)s, %(SB)s, %(CS)s, %(AVG)s,
        %(OBP)s, %(SLG)s, %(TB)s
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
        %(playerid)s, %(name)s, null, 'f',
        %(W)s, %(L)s,
        (%(ER)s / %(IP)s) * 9.0,
        null, null,
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
