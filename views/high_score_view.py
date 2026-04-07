import arcade
from utils.scores import update_scores
from views.game_over_view import GameOver

#new high score page view
class HighScore(arcade.View):
    def __init__(self, score, game_size, game_speed, progressive):
        super().__init__()
        self.score = score
        self.game_size = game_size
        self.game_speed = game_speed
        self.progressive = progressive
        self.initials = ""
        self.grass_texture = arcade.load_texture("assets/textures/grass03.png")
        self.background_list = arcade.SpriteList()
        self.background_sprite = arcade.Sprite()
        self.background_sprite.texture = self.grass_texture
        self.background_sprite.center_x = self.window.width // 2
        self.background_sprite.center_y = self.window.height // 2
        self.background_sprite.width = self.window.width
        self.background_sprite.height = self.window.height
        self.background_list.append(self.background_sprite)

        self.prompt_text1 = arcade.Text(f"New High Score: {score}!", self.window.width // 2, self.window.height // 2 + 80,
            arcade.color.WHITE, 30, anchor_x="center", align="center")

        self.prompt_text2 = arcade.Text("Enter your initials: ", self.window.width // 2, self.window.height // 2 + 40,
            arcade.color.WHITE, 30, anchor_x="center", align="center")

        self.input_text = arcade.Text(self.initials, self.window.width // 2, self.window.height // 2 - 20,
            arcade.color.WHITE, 40, anchor_x="center")

    #draw the elements
    def on_draw(self):
        self.clear()
        self.background_list.draw()

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