import sys

from petitions import Purchases

pc = Purchases()
pc.init()
pc.launch()
pc.login()
if pc.kind_of_basket == "services":
    sys.exit("No... you can't")
pc.access_purchasing()
pc.create_and_show_purchasing()
pc.create_purchasing()
pc.access_basket_options()
if pc.kind_of_basket == "material":
    pc.create_material_basket()
    pc.cost_center()
    pc.article()
    pc.material_form()
    pc.maximize_window()
