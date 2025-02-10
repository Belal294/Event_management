from django import forms 
from .models import Event, Participant, Category
from django.contrib.auth.models import User

class StyledFormMixin:
    default_classes = "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
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




class StyledFormMixin:
    def apply_styled_widgets(self):  
        for field_name, field in self.fields.items():  
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 mt-2 text-sm text-gray-900 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            })

            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-2 mt-2 text-sm text-gray-900 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none'
                })
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-2 mt-2 text-sm text-gray-900 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 cursor-pointer'
                })




class CategoryForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()  



class UserParticipantForm(StyledFormMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


        
