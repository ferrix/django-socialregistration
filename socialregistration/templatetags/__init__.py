from django import template
from django.utils.translation import ugettext_lazy as _

register = template.Library()

m_template = template

def is_quoted(param):
    """ Return True parameter has the same kind of quotes in both ends """
    return (param[0] == param[-1] and param[0] in ('"', "'"))

def button(template):
    """
    Button tag takes two optional arguments. The first is a URL pointing
    to an alternate URL for the button image. The second argument refers
    to a context variable to be appended before the URL.

    The last argument is useful if a variable (eg. STATIC_URL) defines a
    URL root that varies between deployments.
    """

    def tag(parser, token):
        tokens = token.split_contents()
        button = None
        var = None

        token_count = len(tokens)

        if token_count > 3:
            raise m_template.TemplateSyntaxError("%r tag expects zero to two arguments" % token.contents.split()[0])

        if token_count > 2:
            param = tokens[1]
            if not is_quoted(param):
                raise m_template.TemplateSyntaxError("%r tag's first argument should be quoted" % tokens[0])
            button = param[1][1:-1]

        if token_count == 3:
            if is_quoted(tokens[2]):
                raise m_template.TemplateSyntaxError("%r tag's first argument must be an unquoted template context variable" % tokens[0])
            var = tokens[2]

        return ButtonTag(template, button, var)
    return tag

class ButtonTag(template.Node):
    def __init__(self, template, button=None, var=None):
        self.template = template
        self.button = button
        self.var = var
    
    def render(self, context):
        if not 'request' in context:
            raise AttributeError(_("Please add 'django.core.context_processors.request' "
                "'to your settings.TEMPLATE_CONTEXT_PROCESSORS'"))

        if self.var and self.var in context:
            self.button = str(context.get(var, ''))+self.button
        
        return template.loader.render_to_string(self.template, {'button': self.button, 'next': context.get('next', None)}, context)
