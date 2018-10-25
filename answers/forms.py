from django import forms

class AnswerViewsForm(forms.Form):

    sort = forms.ChoiceField(choices=(
        ('content', 'Content asc'),
        ('-content', 'Content desc'),
        ('id', 'Id'),
        ('author', 'Author')
    ), required=False)
    search = forms.CharField(required=False)