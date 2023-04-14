from hospital.models.people import Patient
from hospital.forms.base_form import BootstrapForm


class PatientForm(BootstrapForm):
    class Meta:
        model = Patient
        fields = [
            'first_name',
            'last_name',
            'dob',
            'gender',
            'address',
            'phone',
            'ssn',
            'allergies',
            'blood_type',
            'blood_sugar',
            'cholesterol_hdl',
            'cholesterol_ldl',
            'cholesterol_tri',
        ]

# # Creating a form to add an article.
# form = ArticleForm()

# # Creating a form to change an existing article.
# article = Article.objects.get(pk=1)
# form = ArticleForm(instance=article)