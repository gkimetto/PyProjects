from widgetastic.widget import View
from widgetastic_patternfly import Button


class CockpitView(View):
    add = Button('Add', classes=[Button.PRIMARY])
