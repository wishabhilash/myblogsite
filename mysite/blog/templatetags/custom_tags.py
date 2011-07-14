import datetime
from django import template

register = template.Library()



''' Tag structure : {% get_current_time "format_string" as variable_name %}
						{{ variable_name }}'''

class CurrentTimeNode(template.Node):
	def __init__(self, format_string, var):
		self.format_string = format_string
		self.variable = var
		
	def render(self, context):
		now = datetime.datetime.now()
		context[self.variable] = now.strftime(self.format_string)
		return ""
		
@register.tag(name = 'get_current_time')
def do_current_time(parser, token):
	try:
		tag, arg = token.contents.split(None, 1)
	except ValueError:
		msg = "%r tag requires arguments." % token.contents[0]
		raise template.TemplateSyntaxError(msg)
	
	import re
	m = re.search(r'(.*?) as (\w+)', arg)
	
	if m:
		fmt, var = m.groups()
	else:
		msg = "%r tag had invalid arguments." % tag
		raise template.TemplateSyntaxError(msg)
	
	if not (fmt[0] == fmt[-1] and fmt[0] in ('"', "'")):
		msg = "%r must be within quotes" % fmt
		raise template.TemplateSyntaxError(msg)
	
	return CurrentTimeNode(fmt[1:-1], var)
		

'''Tag structure : {% uppercase %} {% enduppercase %}'''

class UppercaseNode(template.Node):
	def __init__(self, nodelist):
		self.nodelist = nodelist
		
	def render(self, context):
		output = self.nodelist.render(context)
		return output.upper()

@register.tag(name = 'uppercase')
def uppercase(parser, token):
	nodelist = parser.parse(('enduppercase',))
	parser.delete_first_token()
	return UppercaseNode(nodelist)



''' Tag structure : {% assign vararg to varassign %}'''
class AssignVariableNode(template.Node):
	def __init__(self, vararg, varassign):
		self.vararg, self.varassign = map(template.Variable, vararg), varassign
		
	def render(self, context):
		self.vararg = self.vararg.resolve(context, True)
		context[self.varassign] = self.vararg
		return ""

@register.tag(name = "assign")
def assignvar(parser, token):
	try:
		tag, arg = token.contents.split(None, 1)
	except ValueError:
		msg = "%r tag requires arguments." % token.contents[0]
		raise template.TemplateSyntaxError(msg)
	
	arglist = arg.split()
	if len(arglist) is not 3:
		raise template.TemplateSyntaxError("Not enough arguments")
	else:
		vararg = arglist[0]
		varassign = arglist[-1]
	return AssignVariableNode(vararg, varassign)






'''class IfEqualNode(Node):
    child_nodelists = ('nodelist_true', 'nodelist_false')

    def __init__(self, var1, var2, nodelist_true, nodelist_false, negate):
        self.var1, self.var2 = var1, var2
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
        self.negate = negate

    def __repr__(self):
        return "<IfEqualNode>"

    def render(self, context):
        val1 = self.var1.resolve(context, True)
        val2 = self.var2.resolve(context, True)
        if (self.negate and val1 != val2) or (not self.negate and val1 == val2):
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)


def do_ifequal(parser, token, negate):
    bits = list(token.split_contents())
    if len(bits) != 3:
        raise TemplateSyntaxError("%r takes two arguments" % bits[0])
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    val1 = parser.compile_filter(bits[1])
    val2 = parser.compile_filter(bits[2])
    return IfEqualNode(val1, val2, nodelist_true, nodelist_false, negate)

@register.tag(name = "ifnotequal")
def ifequal(parser, token):
    """
    Outputs the contents of the block if the two arguments equal each other.

    Examples::

        {% ifequal user.id comment.user_id %}
            ...
        {% endifequal %}

        {% ifnotequal user.id comment.user_id %}
            ...
        {% else %}
            ...
        {% endifnotequal %}
    """
    return do_ifequal(parser, token, False)
'''
