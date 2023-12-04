from django.shortcuts import render
from .models import User, File, WebsiteInfo
from django.http import JsonResponse
import json
from django.http import JsonResponse
import subprocess

from django.http import JsonResponse
from django.contrib.staticfiles import finders
from .models import IncidentReport
from django.shortcuts import render
from .form import UploadFileForm
#from docx import Document
from attackflow_13pg.utils import analysis
import re
import fitz
import os
from django.conf import settings

# Create your views here.

def home(request):
    return render(request, 'mainPage.html')

def admin_page(request):
    return render(request, 'admin.html')

def get_users(request):
    users = list(User.objects.values())
    return JsonResponse({'users': users})

def get_files(request):
    files = File.objects.all()
    files_list = []
    for file in files:
        files_list.append({
            'id': file.id,
            'filename': file.filename,
            'author': file.user.username,
        })

    return JsonResponse({'files': files_list})

def update_role(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        userId = data.get('userId')
        newRole = data.get('newRole')

        try:
            user = User.objects.get(id=userId)
            user.role = newRole
            user.save()
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False})
        

# 上传和标注函数
def upload_and_annotate(request):
    if request.method == 'POST':
        file = request.FILES['file']
        incident_report = IncidentReport(file=file)
        incident_report.save()

        # 读取文件内容
        file_extension = incident_report.file.name.split('.')[-1].lower()
        content = ""
        if file_extension == 'pdf':
            with fitz.open(incident_report.file.path) as pdf:
                for page_num in range(len(pdf)):
                    page = pdf.load_page(page_num)
                    content += page.get_text()
        # elif file_extension == 'docx':
        #     doc = Document(incident_report.file.path)
        #     for para in doc.paragraphs:
        #         content += para.text + "\n"

        # 读取example.json的内容
        example_file_path = finders.find('test_example.json')

        with open(example_file_path, 'r', encoding='utf-8') as json_file:
            example_json_content = json_file.read()
        content = re.sub(r'\n', '', content)
        stopwords = [
            "a", "the", "an", "and", "or", "but", "about", "above", "across", "after", "against",
            "along", "among", "around", "as", "at", "is", "am", "are", "was",
            "were", "be", "being", "been", "have", "has", "had", "having", "do",
            "does", "did", "doing", "we", "i", "you", "he", "she", "it", "they"
        ]

        # 创建正则表达式
        pattern = r'\b(?:' + '|'.join(stopwords) + r')\s*\b'

        # 使用 re.sub 删除停用词和它们后面的空格
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)

 
        res = analysis(content, example_json_content)
        ##with open (xxx) +r 
        ##append res  oajis
        ##close

        base_name = os.path.splitext(os.path.basename(incident_report.file.name))[0]
       
        output_dir = os.path.join(settings.MEDIA_ROOT, 'outputFile')
       
        output_path = os.path.join(output_dir, f'{base_name}.json')

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(res)

        return render(request, 'upload.html', {'res_content': res})
    else:
        form = UploadFileForm()
        return render(request, 'upload.html', {'form': form})
    
def save_to_json(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def validate_with_attack_flow(request):
    # Path to the script (Update this path based on where you place the batch script on your system)
    script_path = 'C:\\Users\\Jiayu You\\OneDrive - University of Adelaide\\7015\\code\\attackflow_13pg\\attackflow_13pg\\validate_attack_flow.bat'

    try:
        # Execute the script
        validation_result = subprocess.check_output([script_path], text=True)
        success = True
    except subprocess.CalledProcessError as e:
        validation_result = e.output
        success = False

    # Return the validation result as a JSON response
    return JsonResponse({
        'success': success,
        'result': validation_result
    })



