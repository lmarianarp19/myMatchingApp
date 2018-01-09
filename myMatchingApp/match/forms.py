from django import forms

from .models import Community, Man, Woman

# from django.forms import inlineformset_factory


class CommunityForm(forms.ModelForm):

    class Meta:
        model = Community
        fields = ('name', 'number_couples')
        # unique_together = ('name', 'community')

class WomanForm(forms.ModelForm):

    class Meta:
        model = Woman
        fields = ('name', 'community')
        # exclude = ('Pairing',)

# WomanFormSet = inlineformset_factory(Community, Woman, form=WomanForm, extra=1)


class ManForm(forms.ModelForm):

    class Meta:
        model = Man
        fields = ('name','community')
