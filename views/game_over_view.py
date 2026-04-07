import arcade
from utils.scores import draw_high_scores
from views.game_view import GameView
from views.menu_view import MenuView

DEFAULT_WINDOW_SIZE = 600

class GameOver(arcade.View):
    def __init__(self, score, game_size, game_speed, progressive):
        super().__init__()
        self.score = score
        self.game_size = game_size
        self.game_speed = game_speed
        self.progressive = progressive
        arcade.set_background_color(arcade.color.BLUE)

        self.over_text = arcade.Text("Game Over", self.window.width // 2, self.window.height // 2 + 140,
            arcade.color.WHITE, 50, anchor_x="center")

        self.final_text = arcade.Text(f"Final Score: {self.score}", self.window.width // 2, self.window.height // 2 + 100 ,
            arcade.color.GREEN, 40, anchor_x="center")

        self.restart_text = arcade.Text("Press R to Restart", self.window.width // 2, self.window.height // 2 + 60,
            arcade.color.LIGHT_GRAY, 30, anchor_x="center")

        self.main_text = arcade.Text("Press M for Main Menu", self.window.width // 2, self.window.height // 2 + 20,
            arcade.color.LIGHT_GRAY, 30, anchor_x="center")

        self.quit_text = arcade.Text("Press Q to Quit", self.window.width // 2, self.window.height // 2 - 20,
            arcade.color.LIGHT_GRAY, 30, anchor_x="center")

    #draw game over page
    def on_draw(self):
        self.clear()
        self.over_text.draw()
        self.final_text.draw()
        self.restart_text.draw()
        self.main_text.draw()
        self.quit_text.draw()
        draw_high_scores(self.window, self.window.height // 2 - 120 )

    #key selection actions
    def on_key_press(self, key, modifiers):
        #play again with same settings
        if key == arcade.key.R:
            game_view = GameView(self.game_size, self.game_speed, self.progressive)
            self.window.show_view(game_view)

        #go back to menu to select new game size and speed
        elif key == arcade.key.M:
            self.window.set_size(DEFAULT_WINDOW_SIZE, DEFAULT_WINDOW_SIZE)
            menu = MenuView()
            self.window.show_view(menu)

        #quit game
        elif key == arcade.key.Q:
            arcade.close_window()