from django import forms

from src.leads.models import Lead
from src.services.models import Service


class LeadForm(forms.ModelForm):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)
    _TOPICS_MAX = 20
    _TOPIC_LEN = 300

    class Meta:
        model = Lead
        fields = ('name', 'phone', 'email', 'consent', 'service', 'selected_topics')
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control form-input',
                    'placeholder': ' ',
                    'autocomplete': 'name',
                    'inputmode': 'text',
                    'maxlength': '120',
                    'spellcheck': 'false',
                },
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control form-input',
                    'placeholder': ' ',
                    'autocomplete': 'tel',
                    'inputmode': 'tel',
                    'maxlength': '19',
                },
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control form-input',
                    'placeholder': ' ',
                    'autocomplete': 'email',
                    'inputmode': 'email',
                    'maxlength': '254',
                },
            ),
            'consent': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input custom-checkbox__input',
                    'required': True,
                },
            ),
            'service': forms.HiddenInput(),
            'selected_topics': forms.HiddenInput(
                attrs={'data-selected-topics': '1'},
            ),
        }

    def __init__(self, *args, source: str = Lead.Source.HOME, **kwargs):
        super().__init__(*args, **kwargs)
        self.source = source
        self.fields['consent'].required = True
        self.fields['service'].required = False
        self.fields['selected_topics'].required = False
        self.fields['service'].queryset = Service.objects.filter(is_published=True)
        if not self.is_bound and not self.initial.get('phone'):
            self.fields['phone'].initial = '+380'
        if not self.is_bound and self.initial.get('selected_topics') is None:
            self.fields['selected_topics'].initial = []

    def clean_consent(self):
        consent = self.cleaned_data.get('consent')
        if not consent:
            raise forms.ValidationError(
                'Потрібна згода на обробку персональних даних.',
            )
        return consent

    def clean_honeypot(self):
        if self.cleaned_data.get('honeypot'):
            raise forms.ValidationError('Bot detected')
        return ''

    def clean_service(self):
        service = self.cleaned_data.get('service')
        if service and not service.is_published:
            raise forms.ValidationError('Обрана послуга недоступна.')
        return service

    def clean_selected_topics(self):
        topics = self.cleaned_data.get('selected_topics')
        if not topics:
            return []
        if not isinstance(topics, list):
            return []
        cleaned: list[str] = []
        for item in topics[: self._TOPICS_MAX]:
            if not isinstance(item, str):
                continue
            text = item.strip()[: self._TOPIC_LEN]
            if text and text not in cleaned:
                cleaned.append(text)
        return cleaned
