from django.shortcuts import render
from .models import User, File, WebsiteInfo
from django.http import JsonResponse
import json
from django.http import FileResponse
from django.http import JsonResponse
from django.contrib.staticfiles import finders
from .models import IncidentReport
from django.shortcuts import render
from .form import UploadFileForm
#from docx import Document
from attackflow_13pg.utils import analysis
import re
import fitz

# Create your views here.

def home(request):
    return render(request, 'ShenOuyang.html')

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
        #append res  oajis
        #close
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
        os.makedirs(directory)
        file_path = os.path.join(settings.MEDIA_ROOT, 'output_files', 'output1.json')

    # Save 'res' to a file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(res)

        # Serve the file for download
        response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename='downloaded_file.txt')
        return response,render(request, 'upload.html', {'res_content': res})
        

        #return 
    else:
        form = UploadFileForm()
        return render(request, 'upload.html', {'form': form})
    
def save_to_json(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)



