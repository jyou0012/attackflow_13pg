from django import forms
from .models import IncidentReport  # 假设您已经在 models.py 中定义了一个 IncidentReport 模型

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = IncidentReport
        fields = ['file']  # 'file' 是 IncidentReport 模型中定义的一个 FileField
