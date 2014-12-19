__author__ = 'tang'

from model import Page, Section
from flask import url_for


class NavBar:
    def __init__(self):
        self.structure = {}
        pages = Page.find()
        for page in pages:
            self.structure[page.attr['title']] = {}
            for section_id in page.attr['section']:
                section_title = Section(section_id).attr['title']
                self.structure[page.attr['title']][section_title] = {}

    def get_structure(self):
        return self.structure

    @staticmethod
    def get_editor():
        rv = {"Add": {"_type": "drop_down",
                      "data": {
                          "Text": {"class": "editor-nav add-text", "add": "text"},
                          "Image": {"class": "editor-nav add-image", "add": "img"},
                          "Picture Wall": {"class": "editor-nav add-picture-wall", "add": "picture-wall"}
                      }}}
        return rv

    @staticmethod
    def get_section_extra():
        return {"Add": {"_type": "button", "data": {"href": url_for('editor')}}}

    @staticmethod
    def get_editor_extra():
        return {"Save": {"_type": "button", "data": {"id": "btn-save", "style": "cursor: pointer"}}}

    @staticmethod
    def get_page_extra():
        return {"Add": {"_type": "button", "data": {"href": url_for('page_editor')}}}