from django.forms import ModelForm


class BootstrapForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BootstrapForm, self).__init__(*args, **kwargs)

        # you can iterate all fields here
        for _, f in self.fields.items():
            f.widget.attrs['class'] = 'form-control'
