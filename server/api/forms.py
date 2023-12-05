from django import forms
from .models import App

# Model form
class AppRunConfigUploadModelForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ('run_config_file',)
        widgets = {
            'run_config_file': forms.ClearableFileInput(),
        }
        
    def clean_run_config_file(self):
        file = self.cleaned_data['run_config_file']
        ext = file.name.split('.')[-1].lower()
        if ext not in ["arxc", "json"]:
            raise forms.ValidationError("Only arxc and json files are allowed.")
        # return cleaned data is very important.
        return file