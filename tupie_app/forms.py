from django import forms

from .models import Item, Region, District, Ward, Place, Street

class ItemForm(forms.ModelForm):
    region = forms.ModelChoiceField(queryset= Region.objects.all(), empty_label= 'Select Region')
    district = forms.ModelChoiceField(queryset= District.objects.none(), empty_label= 'Select District')
    ward = forms.ModelChoiceField(queryset= Ward.objects.none(), empty_label= 'Select Ward')
    place = forms.ModelChoiceField(queryset= Place.objects.none(), empty_label= 'Select Place')
    street = forms.ModelChoiceField(queryset= Street.objects.all(), required=False, empty_label= 'Optional Street')

    class Meta:
        model = Item
        fields = ['title', 'description', 'region', 'district', 'ward', 'place', 'street']

    def __init__(self, *args, **kwangs):
        super().__init__(*args, **kwangs)
        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['district'].queryset = District.objects.filter(region_id = region_id)
            except (ValueError, TypeError):
                self.fields['district'].queryset = District.objects.none()
        elif self.instance.pk:
            self.fields['district'].queryset = self.instance.region.district_set.all()

        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['ward'].queryset = Ward.objects.filter(district_id = district_id)
            except (ValueError, TypeError):
                self.fields['ward'].querset = Ward.objects.none()
        elif self.instance.pk:
            self.fields['ward'].queryset = self.instance.district.ward_set.all()

        if 'ward' in self.data:
            try:
                ward_id = int(self.data.get('ward'))
                self.fields['place'].queryset = Place.objects.filter(ward_id = ward_id)
            except (ValueError, TypeError):
                self.fields['place'].querset = Place.objects.none()
        elif self.instance.pk:
            self.fields['place'].queryset = self.instance.district.place_set.all()

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('region') or not cleaned_data.get('district') or not cleaned_data.get('ward'):
            raise forms.ValidationError("Please select a region, District, Ward and Place")
        return cleaned_data