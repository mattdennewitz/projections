from django.db.models import StdDev, Avg, F
from django.shortcuts import render
from django.template.loader import render_to_string

from projections.forms import LeagueOverviewForm
from projections.models import Batting, Pitching


def list_players(request):
    """Show a table of all players
    """

    form = LeagueOverviewForm(request.GET)

    return render(request, 'index.html', {
        'form': form,
    })


def player_values(request):
    """Generates and executes query using form parameters.
    """

    form = LeagueOverviewForm(request.GET)
    form.is_valid()

    # pick categories selected by the user
    categories = filter(lambda (k, v): v is True, form.cleaned_data.items())
    pitching = [c[0] for c in categories if c[0] in form.pitching_fields]
    batting = [c[0] for c in categories if c[0] in form.batting_fields]

    query = render_to_string('value_query.html', {
        'pitching': pitching,
        'batting': batting,
        'raw': form.cleaned_data,
    })

    raise Exception, query


    if pitching_categories:
        global_stats['pitching'] = Pitching.objects.aggregate(**pitching_agg)

