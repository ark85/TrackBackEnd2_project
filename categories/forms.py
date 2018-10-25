from django import forms
from categories.models import Category


class CategoryViewsForm(forms.Form):

    sort = forms.ChoiceField(choices=(
        ('name', 'Name asc'),
        ('-name', 'Name desc'),
        ('id', 'Id')
    ), required=False)
    search = forms.CharField(required=False)


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = 'name',