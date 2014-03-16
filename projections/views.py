from django.shortcuts import render


def list_players(request):
    """Show a table of all players
    """

    return render(request, 'player_list.html')
