from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "important"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'write a title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'write a description'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'})  
        }

# Este widget evita que lo hagamos en el HTML como lo hicimos en el signup o el singin, pues, estamos aplicando directamente aquí las clases.