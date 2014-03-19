from __future__ import unicode_literals

from schematics import models, types
from schematics.exceptions import ConversionError
from schematics.types.serializable import serializable


__all__ = ('BattingSchema', 'BattingContainer',
           'PitchingSchema', 'PitchingContainer', )


class BattingSchema(models.Model):
    PA = types.IntType(required=False)
    AB = types.IntType(required=False)
    H = types.IntType(required=False)
    _2B = types.IntType(required=False, serialized_name='2B')
    _3B = types.IntType(required=False, serialized_name='3B')
    HR = types.IntType(required=False)
    R = types.IntType(required=False)
    RBI = types.IntType(required=False)
    BB = types.IntType(required=False)
    SO = types.IntType(required=False)
    HBP = types.IntType(required=False)
    SB = types.IntType(required=False)
    CS = types.IntType(required=False)
    AVG = types.FloatType(required=False)
    OBP = types.FloatType(required=False)
    SLG = types.FloatType(required=False)

    def import_data(self, data, *a, **kw):
        data.update(_2B = data.pop('2B', None),
                    _3B = data.pop('3B', None))

        super(BattingSchema, self).import_data(data, *a, **kw)

    @serializable
    def TB(self):
        return (
            self.H
            + (self._2B * 2)
            + (self._3B * 3)
            + (self.HR * 4)
        )


class PitchingSchema(models.Model):
    W = types.IntType(required=False)
    L = types.IntType(required=False)
    GS = types.IntType(required=False)
    G = types.IntType(required=False)
    SV = types.IntType(required=False)
    BS = types.IntType(required=False)
    IP = types.FloatType(required=False)
    H = types.IntType(required=False)
    ER = types.IntType(required=False)
    HR = types.IntType(required=False)
    SO = types.IntType(required=False)
    BB = types.IntType(required=False)
    WHIP = types.FloatType(required=False)
    K9 = types.FloatType(required=False, serialized_name='K/9')
    BB9 = types.FloatType(required=False, serialized_name='BB/9')
    QS = types.IntType(required=False)
    HD = types.IntType(required=False)
    CG = types.IntType(required=False)
    SH = types.IntType(required=False)

    def import_data(self, data, *a, **kw):
        data.update(
            K9 = data.pop('K/9', None),
            BB9 = data.pop('BB/9', None)
        )

        super(PitchingSchema, self).import_data(data, *a, **kw)

    @serializable(serialized_name='ERA')
    def era(self):
        return (self.ER / self.IP) * 9.


class Container(models.Model):
    """Abstract container for sets of player projections
    """
    playerid = types.StringType()
    name = types.StringType()
    pos = types.StringType(required=False)
    is_kept = types.BooleanType(default=False)
    batting_projections = types.compound.ListType(
        types.compound.ModelType(BattingSchema),
        default=list())
    pitching_projections = types.compound.ListType(
        types.compound.ModelType(PitchingSchema),
        default=list())

    def import_data(self, data, *a, **kw):
        data.update(name=data.pop('Name'))
        super(Container, self).import_data(data, *a, **kw)
