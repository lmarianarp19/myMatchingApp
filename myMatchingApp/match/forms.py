from django import forms

from .models import Community, Blue, Red

# from django.forms import inlineformset_factory


class CommunityForm(forms.ModelForm):

    class Meta:
        model = Community
        fields = ('name', 'number_couples')
        # unique_together = ('name', 'community')

class RedForm(forms.ModelForm):

    class Meta:
        model = Red
        fields = ('name', 'community')
        # exclude = ('Pairing',)

# WomanFormSet = inlineformset_factory(Community, Woman, form=WomanForm, extra=1)


class BlueForm(forms.ModelForm):

    class Meta:
        model = Blue
        fields = ('name','community')
