from PIL import Image
import re

def get_icon():
    return Image.open('favicon.png')

def convert_readable(input_string):
    return ' '.join(word.title() for word in input_string.split('_'))

def escape_student(student):
    escaped_student = re.escape(student)
    literal_student = rf'(?<!\S){escaped_student}(?!\S)'
    return literal_student