from flask import Flask, render_template, request, send_file
import openpyxl

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def static_file(path):
    return app.send_static_file(path)

@app.route('/add_student', methods=['POST'])
def add_student():
    if request.method == 'POST':
        save_student_to_excel(request.form.to_dict())
    return render_template('index.html', students_data=read_students_from_excel())

def save_student_to_excel(student_data):
    excel_file_path = '/tmp/students.xlsx'
    headers = ['Name', 'Age', 'Grade']

    try:
        workbook = openpyxl.load_workbook(excel_file_path)
        worksheet = workbook.active
    except FileNotFoundError:
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.append(headers)

    worksheet.append([student_data.get(field, '') for field in headers])
    workbook.save(excel_file_path)

def read_students_from_excel():
    excel_file_path = '/tmp/students.xlsx'
    headers = ['Name', 'Age', 'Grade']

    try:
        workbook = openpyxl.load_workbook(excel_file_path)
        worksheet = workbook.active
    except FileNotFoundError:
        return []

    students_data = [dict(zip(headers, row)) for row in worksheet.iter_rows(min_row=2, values_only=True)]
    return students_data

@app.route('/generate_excel', methods=['POST'])
def generate_excel():
    if request.method == 'POST':
        input_data = request.form.to_dict()
        save_student_to_excel(input_data)
    return send_file('/tmp/students.xlsx', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
