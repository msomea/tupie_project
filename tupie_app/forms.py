from django import forms
from .models import Item, Region, District, Ward, Place, Street

class ItemForm(forms.ModelForm):
    #region = forms.ModelChoiceField(queryset=Region.objects.all(), empty_label='Select Region')
    district = forms.ModelChoiceField(queryset=District.objects.none(), empty_label='Select District')
    ward = forms.ModelChoiceField(queryset=Ward.objects.none(), empty_label='Select Ward')
    place = forms.ModelChoiceField(queryset=Place.objects.none(), empty_label='Select Place')
    
    street = forms.CharField(
        required=False,
        max_length=100,
        label='Street (optional)',
        widget=forms.TextInput(attrs={'placeholder': 'Enter street name if known'})
    )

    class Meta:
        model = Item
        fields = ['title', 'description', 'region', 'district', 'ward', 'place', 'street']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate district queryset based on selected region
        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['district'].queryset = District.objects.filter(region_id=region_id)
            except (ValueError, TypeError):
                self.fields['district'].queryset = District.objects.none()
        elif self.instance.pk and self.instance.region:
            self.fields['district'].queryset = District.objects.filter(region=self.instance.region)
        else:
            self.fields['district'].queryset = District.objects.none()

        # Populate ward queryset based on selected district
        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['ward'].queryset = Ward.objects.filter(district_id=district_id)
            except (ValueError, TypeError):
                self.fields['ward'].queryset = Ward.objects.none()
        elif self.instance.pk and self.instance.district:
            self.fields['ward'].queryset = Ward.objects.filter(district=self.instance.district)
        else:
            self.fields['ward'].queryset = Ward.objects.none()

        # Populate place queryset based on selected ward
        if 'ward' in self.data:
            try:
                ward_id = int(self.data.get('ward'))
                self.fields['place'].queryset = Place.objects.filter(ward_id=ward_id)
            except (ValueError, TypeError):
                self.fields['place'].queryset = Place.objects.none()
        elif self.instance.pk and self.instance.ward:
            self.fields['place'].queryset = Place.objects.filter(ward=self.instance.ward)
        else:
            self.fields['place'].queryset = Place.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        if not all([cleaned_data.get('region'), cleaned_data.get('district'), cleaned_data.get('ward'), cleaned_data.get('place')]):
            raise forms.ValidationError("Please select Region, District, Ward and Place.")
        return cleaned_data
