from django import forms 
from .models import Event, Participant, Category

class StyledFormMixin:
    default_classes = "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.item():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter{field.label.lower()}"
                })

            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder': f"Enter{field.label.lower()}",
                    'rows':5
                })

            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs.update({
                    "class": self.default_classes,
                    "type": "date"
                })

            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({
                    "class": self.default_classes,
                    "type": "time"
                })

            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': self.default_classes
                })

            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })



class EventForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-2 border border-black rounded-lg'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 border border-black rounded-lg'}),
            'date': forms.DateInput(attrs={'class': 'w-full p-2 border border-black rounded-lg', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'w-full p-2 border border-black rounded-lg', 'type': 'time'}),
            'location': forms.TextInput(attrs={'class': 'w-full p-2 border border-black rounded-lg'}),
            'category': forms.Select(attrs={'class': 'w-full p-2 border border-black rounded-lg'}),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.apply_styled_widgets()


class ParticipantForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()



class CategoryForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()