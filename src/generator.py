import os
from jinja2 import Template


class TemplateLoader:
    def get_template(self, name):
        assert isinstance(name, str)

        template_file = self._template_file(name)
        with open(template_file) as fd:
            return Template(fd.read())

    def _template_file(self, name):
        current = os.path.dirname(__file__)
        filename = name + '.jinja'
        return os.path.join(current, 'templates', filename)


class Generator:
    def __init__(self, template_name):
        self._tmpl_loader = TemplateLoader()
        self.template_name = template_name

    def render_file(self, context):
        template = self._tmpl_loader.get_template(self.template_name)
        return template.render(context)
