__author__ = 'tang'

import model


def nav_bar_structure():
    structure = {}
    pages = model.page.get_all_content()
    for page_ite in pages:
        structure[page_ite['title']]=[]
        for section in page_ite['section_detail']:
            structure[page_ite['title']].append(section['title'])
    return structure