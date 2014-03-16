from __future__ import unicode_literals
import collections

from django.db import models


class Player(models.Model):
    playerid = models.CharField(unique=True, max_length=12, blank=True)
    name = models.CharField(max_length=120, blank=True)
    pos = models.CharField(max_length=5, blank=True, null=True)
    is_kept = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name


class Batting(Player):
    g = models.IntegerField(blank=True, null=True)
    pa = models.IntegerField(blank=True, null=True)
    ab = models.IntegerField(blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    hr = models.IntegerField(blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)
    rbi = models.IntegerField(blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    hbp = models.IntegerField(blank=True, null=True)
    sb = models.IntegerField(blank=True, null=True)
    cs = models.IntegerField(blank=True, null=True)
    avg = models.FloatField(blank=True, null=True)
    obp = models.FloatField(blank=True, null=True)
    slg = models.FloatField(blank=True, null=True)
    tb = models.IntegerField(blank=True, null=True)
    woba = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = 'Batter'


class Pitching(Player):
    w = models.IntegerField(blank=True, null=True)
    l = models.IntegerField(blank=True, null=True)
    era = models.FloatField(blank=True, null=True)
    sv = models.IntegerField(blank=True, null=True)
    bs = models.IntegerField(blank=True, null=True)
    ip = models.FloatField(blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    er = models.IntegerField(blank=True, null=True)
    hra = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    whip = models.FloatField(blank=True, null=True)
    k9 = models.FloatField(blank=True, null=True)
    bb9 = models.FloatField(blank=True, null=True)

    # non-native fields
    qs = models.IntegerField(blank=True, null=True)
    hd = models.IntegerField(blank=True, null=True)
    cg = models.IntegerField(blank=True, null=True)
    sh = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Pitcher'
