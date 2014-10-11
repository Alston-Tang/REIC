__author__ = 'tang'


def is_word(mime_type):
    return mime_type == 'application/msword' or mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

def is_pdf(mime_type):
    return mime_type == 'application/pdf' or mime_type == 'application/x-pdf'