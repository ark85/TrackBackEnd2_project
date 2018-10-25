from django import forms


class QuestionViewsForm(forms.Form):

    sort = forms.ChoiceField(choices=(
        ('name', 'Name asc'),
        ('-name', 'Name desc'),
        ('id', 'Id'),
        ('author', 'Author')
    ), required=False)
    search = forms.CharField(required=False)