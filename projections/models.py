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

    @classmethod
    def get_field_sort_dir(cls, field_name):
        try:
            return cls._meta.get_field_by_name(field_name)[0].sort_dir
        except IndexError:
            raise IndexError('This field could not be found')
        except:
            raise


class WeightedValueField(models.FloatField):
    def __init__(self, sort_dir=1, *a, **kw):
        self.sort_dir = sort_dir
        kw.update(blank=True, null=True)
        super(WeightedValueField, self).__init__(*a, **kw)


class Batting(Player):
    g = WeightedValueField(sort_dir=1, verbose_name='Games')
    pa = WeightedValueField(sort_dir=1)
    ab = WeightedValueField(sort_dir=1)
    h = WeightedValueField(sort_dir=1)
    hr = WeightedValueField(sort_dir=1)
    r = WeightedValueField(sort_dir=1)
    rbi = WeightedValueField(sort_dir=1)
    bb = WeightedValueField(sort_dir=1)
    so = WeightedValueField(sort_dir=-1)
    hbp = WeightedValueField(sort_dir=1)
    sb = WeightedValueField(sort_dir=1)
    cs = WeightedValueField(sort_dir=-1)
    avg = WeightedValueField(sort_dir=1)
    obp = WeightedValueField(sort_dir=1)
    slg = WeightedValueField(sort_dir=1)
    tb = WeightedValueField(sort_dir=1)

    class Meta:
        verbose_name = 'Batter'


class Pitching(Player):
    w = WeightedValueField(sort_dir=1)
    l = WeightedValueField(sort_dir=-1)
    era = WeightedValueField(sort_dir=-1)
    sv = WeightedValueField(sort_dir=1)
    bs = WeightedValueField(sort_dir=-1)
    ip = WeightedValueField(sort_dir=1)
    h = WeightedValueField(sort_dir=1)
    er = WeightedValueField(sort_dir=-1)
    hra = WeightedValueField(sort_dir=-1)
    so = WeightedValueField(sort_dir=1)
    bb = WeightedValueField(sort_dir=-1)
    whip = WeightedValueField(sort_dir=-1)
    k9 = WeightedValueField(sort_dir=1)
    bb9 = WeightedValueField(sort_dir=-1)

    # non-native fields
    qs = WeightedValueField(sort_dir=1)
    hd = WeightedValueField(sort_dir=1)
    cg = WeightedValueField(sort_dir=1)
    sh = WeightedValueField(sort_dir=1)

    class Meta:
        verbose_name = 'Pitcher'
