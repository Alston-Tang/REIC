__author__ = 'tang'

import model


def nav_bar_structure():
    structure = {}
    pages = model.Page().get_all_content()
    for page in pages:
        structure[page['title']]=[]
        for section in page['section_detail']:
            structure[page['title']].append(section['title'])
    return structure