__author__ = 'tang'

from model import Page, Section


class NavBar:
    def __init__(self):
        self.structure = {}
        pages = Page.find()
        for page in pages:
            self.structure[page.attr['title']] = []
            for section_id in page.attr['section']:
                section_title = Section(section_id).attr['title']
                self.structure[page.attr['title']].append(section_title)

    def get_structure(self):
        return self.structure