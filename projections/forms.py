import itertools

from django import forms

from projections.models import Player, Batting, Pitching


class LeagueOverviewForm(forms.Form):
    min_ip = forms.IntegerField(
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control input-sm',
            'min': 0,
            'step': 5,
        }))
    min_pa = forms.IntegerField(
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control input-sm',
            'min': 0,
            'step': 5,
        }))
    use_pts = forms.BooleanField(required=False)

    def __init__(self, *a, **kw):
        super(LeagueOverviewForm, self).__init__(*a, **kw)

        # add a boolean field for each model stat field
        inherited_fields = set([f.name for f in Player._meta.local_fields])
        inherited_fields.add('id')
        self.batting_fields = set([f.name for f in Batting._meta.fields]) - inherited_fields
        self.pitching_fields = set([f.name for f in Pitching._meta.fields]) - inherited_fields

        for field_name in itertools.chain(self.batting_fields,
                                          self.pitching_fields):
            # add option field
            self.fields[field_name] = forms.BooleanField(required=False)

            self.fields[field_name + '_pts'] = forms.IntegerField(
                initial=0,
                max_value=100,
                min_value=-100,
                widget=forms.NumberInput(attrs={
                    'class': 'form-control input-sm',
                    'style': 'width: 60px',
                }))
