from django import forms

from .models import Community, Blue, Red, Ranking

from django.core.exceptions import ValidationError

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
        fields = ('name', 'community')
        # exclude = ('Pairing',)


class RankingBlueForm(forms.ModelForm):
    class Meta:
        model = Ranking
        fields = ('blue_to_red_score',)

class RankingRedForm(forms.ModelForm):
    class Meta:
        model = Ranking
        fields = ('red_to_blue_score',)


    # blue_to_red_score = forms.IntegerField()
    # blue = forms.IntegerField(widget=forms.HiddenInput())
    # red = forms.IntegerField(widget=forms.HiddenInput())
    # TODO tal vez poner el clean
# class BlueForm(forms.Form):
#
#     # class Meta:
#     #     model = Blue
#     #     fields = ('name','community')
#     name = forms.CharField()
#     community = forms.CharField()
#
#     def clean_blue(self):
#         name_data = self.cleaned_data['name']
#         community_data = self.cleaned_data['community']
#
#         blues = Blue.objects.filter(community = community)
#         print('this is blues')
#         print(blues)
#         #Check date is not in past.
#         if blues.count >= community_data.number_couples:
#             raise ValidationError(_('There is no more space for blue in this community'))
#
#         # Remember to always return the cleaned data.
#         return name_data, community_data


# class AddBlue(forms.Form):
    # renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")
