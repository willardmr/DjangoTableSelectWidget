# DjangoTableSelectWidget
A Django widget for use with a ModelChoiceField to allow easy jQuery DataTables sorting and pagination by rendering the selector as a table.

Example form field:
```python
items = forms.ModelChoiceField(
        queryset=myqueryset, widget=widgets.TableSelect(
        item_attrs=('tablecolumn1', 'tablecolumn2')))
```
        
Render it normally with a Django form.


Recommended Datatables Javascript to disallow sorting on the checkbox column:

```javascript
<script src="https://cdn.datatables.net/1.10.7/js/jquery.dataTables.min.js"></script>

<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.7/css/jquery.dataTables.css"></link>

<script>
$(document).ready(function(){
    $('#items').DataTable({
        "order": [],
        "columnDefs": [{
        "targets"  : 'no-sort',
        "orderable" : false,
    }]
    });
});
</script>
```

Modified from https://djangosnippets.org/snippets/518/ for use with Python 3, Django 1.7.


Very similar to my TableSelectMultiple widget found here: https://github.com/willardmr/DjangoTableSelectMultipleWidget
