import arcade
from views.menu_view import MenuView

size = 600

window = arcade.Window(size, size, title="Snake")
window.center_window()

menu = MenuView()
window.show_view(menu)
arcade.run()