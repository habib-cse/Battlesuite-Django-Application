from django import forms

class TournamentForm(forms.Form):
    name = forms.CharField(label="Tournament Name", max_length=100)
    game_name = forms.CharField(label="Game Name", max_length=100)
    platform = forms.CharField(label="Platform", max_length=100)
    player_amount = forms.ChoiceField(choices=["1 VS 1", "2 VS 2", "3 VS 3", "4 VS 4", "5 VS 5"], widget=forms.RadioSelect)
    number_of_teams = forms.ChoiceField(choices=["2 Teams", "4 Teams", "8 Teams"], widget=forms.RadioSelect)
    game_length = forms.ChoiceField(choices=["40 min", "60 min", "80 min"], widget=forms.RadioSelect)
    date = forms.DateTimeField()
    description = forms.CharField(label="Tournament Description", max_length=5000)