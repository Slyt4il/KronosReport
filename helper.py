from PIL import Image

icon = Image.open('favicon.png')

def get_icon():
    return icon

def convert_readable(input_string):
    return ' '.join(word.title() for word in input_string.split('_'))