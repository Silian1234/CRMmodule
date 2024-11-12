from django import forms
from django.contrib.auth.models import Group
from .models import Event, CustomUser

class EventAdminForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        leaders_group = Group.objects.get(name="leader")
        self.fields['leader'].queryset = CustomUser.objects.filter(groups=leaders_group)

        curators_group = Group.objects.get(name="curator")
        self.fields['curator'].queryset = CustomUser.objects.filter(groups=curators_group)