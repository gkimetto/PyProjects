from navmazing import NavigateToAttribute


from cfme import BaseLoggedInPage
from utils.appliance import Navigatable
from utils.appliance.implementations.ui import CFMENavigateStep, navigator

class CfmePage(Navigatable):
    def __init__(self, name=None, appliance=None):
        self.name = name
        Navigatable.__init__(self, appliance=appliance)


@navigator.register(CfmePage, 'All')
class CfmePageAll(CFMENavigateStep):
    # Widgetastic View
    VIEW = BaseLoggedInPage
    prerequisite = NavigateToAttribute('appliance.server', 'LoggedIn')

    def step(self):
        self.view.navigation.select('Compute','Infrastructure', 'CfmePage')

from utils.appliance.implementations.ui import navigate_to
navigate_to(CfmePage,'All')
