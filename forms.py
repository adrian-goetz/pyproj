from flask_wtf import Form
from wtforms import widgets, SelectMultipleField


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ItemSelectionForm(Form):
    selected_items = MultiCheckboxField()
