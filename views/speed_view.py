import arcade
from views.game_view import GameView

class SpeedView(arcade.View):
    def __init__(self, game_size):
        super().__init__()
        arcade.set_background_color(arcade.color.BLUE)
        self.game_size = game_size
        self.game_speed = 0.15
        self.speed_text = arcade.Text("Select Your Game Speed:", self.window.width // 2, self.window.height // 2 + 100,
            arcade.color.WHITE, font_size=40, anchor_x="center")
        self.slow_text = arcade.Text("D: Slow", self.window.width // 2, self.window.height // 2 + 60,
            arcade.color.WHITE, font_size=25, anchor_x="center")
        self.medium_text = arcade.Text("E: Medium", self.window.width // 2, self.window.height // 2 + 20,
            arcade.color.WHITE, font_size=25, anchor_x="center")
        self.fast_text = arcade.Text("F: Fast", self.window.width // 2, self.window.height // 2 -20,
            arcade.color.WHITE, font_size=25, anchor_x="center")
        self.progressive_text = arcade.Text("G: Progressive (Starts slow and speeds up)", self.window.width // 2, self.window.height // 2 -60,
            arcade.color.WHITE, font_size=25, anchor_x="center")
        self.start_text = arcade.Text("Press ENTER to Start", self.window.width // 2, self.window.height // 2 -100,
            arcade.color.WHITE, font_size=25, anchor_x="center")
        self.start_text = arcade.Text("During Game Play, press P to pause", self.window.width // 2, self.window.height // 2 -140,
            arcade.color.WHITE, font_size=20, anchor_x="center")

    #draw speed select screen
    def on_draw(self):
        self.clear()
        self.speed_text.draw()
        self.slow_text.draw()
        self.medium_text.draw()
        self.fast_text.draw()
        self.progressive_text.draw()
        self.start_text.draw()

    #what happens when these keys are pressed
    def on_key_press(self, key, modifiers):
        if key == arcade.key.D:
            self.game_speed = 0.25
            game_view = GameView(self.game_size, self.game_speed, progressive=False)
            self.window.show_view(game_view)

        elif key == arcade.key.E:
            self.game_speed = 0.15
            game_view = GameView(self.game_size, self.game_speed, progressive=False)
            self.window.show_view(game_view)

        elif key == arcade.key.F:
            self.game_speed = 0.1
            game_view = GameView(self.game_size, self.game_speed, progressive=False)
            self.window.show_view(game_view)

        elif key == arcade.key.G:
            self.game_speed = 0.20 #start with medium speed and increase as snake grows
            game_view = GameView(self.game_size, self.game_speed, progressive=True)
            self.window.show_view(game_view)

        elif key == arcade.key.ENTER:
            self.game_speed = 0.15
            game_view = GameView(self.game_size, self.game_speed)
            self.window.show_view(game_view)
