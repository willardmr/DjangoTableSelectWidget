from django.forms import CheckboxInput, SelectMultiple, Select, RadioSelect
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils.safestring import mark_safe


class TableSelect(Select):
    """
    Provides selection of items via checkboxes, with a table row
    being rendered for each item, the first cell in which contains the
    checkbox.
    Only for use with a ModelMultipleChoiceField
    """
    def __init__(self, item_attrs, *args, **kwargs):
        """
        item_attrs
            Defines the attributes of each item which will be displayed
            as a column in each table row, in the order given.

            Any callables in item_attrs will be called with the item to be
            displayed as the sole parameter.

            Any callable attribute names specified will be called and have
            their return value used for display.

            All attribute values will be escaped.
        """
        super(TableSelect, self).__init__(*args, **kwargs)
        self.item_attrs = item_attrs

    def render(self, name, value,
               attrs=None, choices=()):
        if value is None:
            value = []
        output = []
        output.append('<table id=%s class="display">' % escape(name))
        head = self.render_head()
        output.append(head)
        body = self.render_body(name, value, attrs)
        output.append(body)
        output.append('</table>')
        return mark_safe('\n'.join(output))

    def render_head(self):
        output = []
        output.append('<thead><tr><th class="no-sort"></th>')
        for item in self.item_attrs:
            output.append('<th>%s</th>' % escape(item.capitalize()))
        output.append('</tr></thead>')
        return ''.join(output)

    def render_body(self, name, value, attrs):
        output = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        str_value = force_text(value)
        for i, (pk, item) in enumerate(self.choices):
            if pk:
                # If an ID attribute was given, add a numeric index as a suffix,
                # so that the checkboxes don't all have the same ID attribute.
                if has_id:
                    final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                item = self.choices.queryset.get(pk=pk)
                if pk == value:
                    rb = '<input id={} name={} value={} type="radio" checked="checked">'.format(final_attrs['id'], name, pk)
                else:
                    rb = '<input id={} name={} value={} type="radio">'.format(final_attrs['id'], name, pk)
                output.append('<tr><td>%s</td>' % rb)
                for attr in self.item_attrs:
                    if callable(attr):
                        content = attr(item)
                    elif callable(getattr(item, attr)):
                        content = getattr(item, attr)()
                    else:
                        content = getattr(item, attr)
                    output.append('<td>%s</td>' % escape(content))
                output.append('</tr>')
        output.append('</tbody>')
        return ''.join(output)

