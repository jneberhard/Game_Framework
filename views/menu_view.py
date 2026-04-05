import arcade
from utils.scores import draw_high_scores
from views.speed_view import SpeedView
from views.game_view import GameView

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLUE)
        self.game_size = 600
        self.welcome_text = arcade.Text("Welcome to Snake!", self.window.width // 2, self.window.height // 2 + 160,
            arcade.color.WHITE, font_size=50, anchor_x="center")
        self.size_text = arcade.Text("Select Your Game Size:", self.window.width // 2, self.window.height // 2 + 120,
            arcade.color.WHITE, font_size=40, anchor_x="center")
        self.small_text = arcade.Text("A: Small (400x400)", self.window.width // 2, self.window.height // 2 + 80,
            arcade.color.WHITE, font_size=25, anchor_x="center")
        self.medium_text = arcade.Text("B: Medium (600x600)", self.window.width // 2, self.window.height // 2 + 40,
            arcade.color.WHITE, font_size=25, anchor_x="center")
        self.large_text = arcade.Text("C: Large (800x800)", self.window.width // 2, self.window.height // 2,
            arcade.color.WHITE, font_size=25, anchor_x="center")
        self.start_text = arcade.Text("Press ENTER to Start", self.window.width // 2, self.window.height // 2 -40,
            arcade.color.WHITE, font_size=25, anchor_x="center")

    #draw the menu screen
    def on_draw(self):
        self.clear()
        self.welcome_text.draw()
        self.size_text.draw()
        self.small_text.draw()
        self.medium_text.draw()
        self.large_text.draw()
        self.start_text.draw()
        draw_high_scores(self.window, self.window.height // 2 - 140)

    #actions for the key press
    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.game_size = 400
            speed_view = SpeedView(self.game_size)
            self.window.show_view(speed_view)

        elif key == arcade.key.B:
            self.game_size = 600
            speed_view = SpeedView(self.game_size)
            self.window.show_view(speed_view)

        elif key == arcade.key.C:
            self.game_size = 800
            speed_view = SpeedView(self.game_size)
            self.window.show_view(speed_view)

        elif key == arcade.key.ENTER:
            self.game_size = 600
            self.game_speed = 0.15
            game_view = GameView(self.game_size, self.game_speed)
            self.window.show_view(game_view)