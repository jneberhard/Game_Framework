import arcade
from utils.scores import update_scores
from views.game_over_view import GameOver

class HighScore(arcade.View):
    def __init__(self, score, game_size, game_speed, progressive):
        super().__init__()
        self.score = score
        self.game_size = game_size
        self.game_speed = game_speed
        self.progressive = progressive
        self.initials = ""
        arcade.set_background_color(arcade.color.BLUE)

        self.prompt_text1 = arcade.Text(f"New High Score: {score}!", self.window.width // 2, self.window.height // 2 + 80,
            arcade.color.WHITE, 30, anchor_x="center", align="center")

        self.prompt_text2 = arcade.Text(f"Enter your initials: ", self.window.width // 2, self.window.height // 2 + 40,
            arcade.color.WHITE, 30, anchor_x="center", align="center")

        self.input_text = arcade.Text(self.initials, self.window.width // 2, self.window.height // 2 - 20,
            arcade.color.WHITE, 40, anchor_x="center")

    #draw the elements
    def on_draw(self):
        self.clear()

        self.prompt_text1.draw()
        self.prompt_text2.draw()

        display = self.initials + "_ " * (3 - len(self.initials))
        self.input_text.text = display
        self.input_text.draw()

    #imputing initials
    def on_key_press(self, key, modifiers):
        if arcade.key.A <= key <= arcade.key.Z and len(self.initials) < 3:
            self.initials += chr(key).upper()

        elif key == arcade.key.BACKSPACE and len(self.initials) > 0:
            self.initials = self.initials[:-1]

        elif key == arcade.key.ENTER and len(self.initials) > 0:
            update_scores(self.score, self.initials)
            game_over_view = GameOver(self.score, self.game_size, self.game_speed, self.progressive)
            self.window.show_view(game_over_view)