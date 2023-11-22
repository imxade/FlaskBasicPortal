from flask import Flask, render_template, request, send_file
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Store student data in a list
students_data = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_student', methods=['POST'])
def add_student():
    # Get data from the form
    name = request.form['name']
    age = request.form['age']
    grade = request.form['grade']

    # Append data to the list
    students_data.append({'name': name, 'age': age, 'grade': grade})

    return render_template('index.html', students_data=students_data)


@app.route('/generate_xml')
def generate_xml():
    # Create XML structure
    root = ET.Element('students')
    for student in students_data:
        student_elem = ET.SubElement(root, 'student')
        name_elem = ET.SubElement(student_elem, 'name')
        name_elem.text = student['name']
        age_elem = ET.SubElement(student_elem, 'age')
        age_elem.text = student['age']
        grade_elem = ET.SubElement(student_elem, 'grade')
        grade_elem.text = student['grade']

    # Create XML file
    tree = ET.ElementTree(root)
    tree.write('students.xml')

    return send_file('../students.xml', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
