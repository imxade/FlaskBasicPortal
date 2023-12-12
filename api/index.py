from flask import Flask, render_template, request, send_file
import openpyxl

app = Flask(__name__)

def get_workbook(excel_file_path):
    try:
        return openpyxl.load_workbook(excel_file_path)
    except FileNotFoundError:
        return openpyxl.Workbook()

def get_worksheet(workbook):
    return workbook.active

def get_headers():
    return ['Name', 'Age', 'Grade']

def append_headers(worksheet):
    worksheet.append(get_headers())

def append_student_data(worksheet, student_data):
    headers = get_headers()
    worksheet.append([student_data.get(field, '') for field in headers])

def save_workbook(excel_file_path, workbook):
    workbook.save(excel_file_path)

def save_student_to_excel(student_data):
    excel_file_path = '/tmp/students.xlsx'
    workbook = get_workbook(excel_file_path)
    worksheet = get_worksheet(workbook)

    if not worksheet.dimensions:
        append_headers(worksheet)

    append_student_data(worksheet, student_data)
    save_workbook(excel_file_path, workbook)

def read_students_from_excel():
    excel_file_path = '/tmp/students.xlsx'
    workbook = get_workbook(excel_file_path)
    worksheet = get_worksheet(workbook)

    if not worksheet.dimensions:
        return []

    headers = get_headers()
    students_data = [dict(zip(headers, row)) for row in worksheet.iter_rows(min_row=2, values_only=True)]
    return students_data

@app.route('/')
def index():
    return render_elements()

@app.route('/static/<path:path>')
def static_file(path):
    return app.send_static_file(path)

@app.route('/add_student', methods=['POST'])
def add_student():
    if request.method == 'POST':
        student_data = request.form.to_dict()
        save_student_to_excel(student_data)
    return render_elements()

def render_elements():
    return render_template('index.html', students_data=read_students_from_excel())

@app.route('/generate_excel', methods=['POST'])
def generate_excel():
    if request.method == 'POST':
        input_data = request.form.to_dict()
        save_student_to_excel(input_data)
    return send_file('/tmp/students.xlsx', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
