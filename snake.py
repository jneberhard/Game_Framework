import arcade
import random

size = 600

window = arcade.Window(size, size, title="Snake")
window.center_window()


#############################################
#          MENU VIEW                   #
##############################################
class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLUE)
        self.game_size = 600

    def on_draw(self):
        self.clear()
        arcade.draw_text("Welcome to Snake!", self.window.width // 2, self.window.height // 2 + 100,
            arcade.color.WHITE, font_size=30, anchor_x="center")
        arcade.draw_text("Select Your Game Size:", self.window.width // 2, self.window.height // 2 + 50,
            arcade.color.LIGHT_GRAY, font_size=25, anchor_x="center")
        arcade.draw_text("A: Small (380x380)", self.window.width // 2, self.window.height // 2 + 20,
            arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")
        arcade.draw_text("B: Medium (600x600)", self.window.width // 2, self.window.height // 2 + -10,
            arcade.color.LIGHT_GRAY, font_size=20,  anchor_x="center")
        arcade.draw_text("C: Large (1000x1000)", self.window.width // 2, self.window.height // 2 + -40,
            arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")
        arcade.draw_text("Press ENTER to Start", self.window.width // 2, self.window.height // 2 + -80,
            arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.game_size = 380
            speed_view = SpeedView(self.game_size)
            self.window.show_view(speed_view)

        elif key == arcade.key.B:
            self.game_size = 600
            speed_view = SpeedView(self.game_size)
            self.window.show_view(speed_view)

        elif key == arcade.key.C:
            self.game_size = 900
            speed_view = SpeedView(self.game_size)
            self.window.show_view(speed_view)

        if key == arcade.key.ENTER:
            speed_view = SpeedView(self.game_size)
            self.window.show_view(speed_view)


class SpeedView(arcade.View):
    def __init__(self, game_size):
        super().__init__()
        arcade.set_background_color(arcade.color.BLUE)
        self.game_size = game_size
        self.game_speed = 0.15

    def on_draw(self):
        self.clear()
        arcade.draw_text("Select Your Game Speed:", self.window.width // 2, self.window.height // 2 + 50,
            arcade.color.LIGHT_GRAY, font_size=25, anchor_x="center")
        arcade.draw_text("D: Slow", self.window.width // 2, self.window.height // 2 + 20,
            arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")
        arcade.draw_text("E: Medium", self.window.width // 2, self.window.height // 2 + -10,
            arcade.color.LIGHT_GRAY, font_size=20,  anchor_x="center")
        arcade.draw_text("F: Fast", self.window.width // 2, self.window.height // 2 + -40,
            arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")
        arcade.draw_text("G: Progressive (Starts slow and speeds up)", self.window.width // 2, self.window.height // 2 + -70,
            arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")
        arcade.draw_text("Press ENTER to Start", self.window.width // 2, self.window.height // 2 + -100,
            arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.D:
            self.game_speed = 0.25
            game_view = GameView(self.game_size, self.game_speed)
            self.window.show_view(game_view)

        elif key == arcade.key.E:
            self.game_speed = 0.15
            game_view = GameView(self.game_size, self.game_speed)
            self.window.show_view(game_view)

        elif key == arcade.key.F:
            self.game_speed = 0.1
            game_view = GameView(self.game_size, self.game_speed)
            self.window.show_view(game_view)

        elif key == arcade.key.G:
            self.game_speed = 0.15 #start with medium speed and increase as snake grows longer
            game_view = GameView(self.game_size, self.game_speed)
            self.window.show_view(game_view)

        if key == arcade.key.ENTER:
            game_view = GameView(self.game_size, self.game_speed)
            self.window.show_view(game_view)


#############################################
#          GAME VIEW                   #
###############################################
class GameView(arcade.View):

    def __init__(self, game_size=600, game_speed=0.15):
        super().__init__()
        arcade.set_background_color(arcade.color.BLUE)
        self.game_size = game_size
        self.game_speed = game_speed
        self.move_delay = self.game_speed
        self.move_timer = 0
        self.direction = (20, 0)
        self.game_over = False
        self.window.set_size(self.game_size, self.game_size)
        self.snake_list = arcade.SpriteList()

        #create snake head and 2 segments
        starting_positions = [(0, 0), (-20, 0), (-40, 0)]

        for position in starting_positions:
            segment = arcade.SpriteSolidColor(20, 20, color=arcade.color.GREEN)
            segment.center_x = (self.game_size // 2) + position[0]
            segment.center_y = (self.game_size // 2) + position[1]
            self.snake_list.append(segment)

        #create food if it does not exist
        self.food_list = arcade.SpriteList()
        self.food = arcade.SpriteSolidColor(20, 20, color=arcade.color.RED)
        self.food.center_x = random.randint(0, (self.game_size // 2)) // 20 * 20   #the // 20 * 20 ensure the food is placed on the gride the snake will move
        self.food.center_y = random.randint(0, (self.game_size // 2)) // 20 * 20
        self.food_list.append(self.food)

    def on_draw(self):
        self.clear()
        self.snake_list.draw()
        self.food_list.draw()
        if self.game_over:
            arcade.draw_text("Game Over", self.game_size // 2, self.game_size // 2, arcade.color.WHITE, font_size=50, anchor_x="center", anchor_y="center")

    def on_update(self, delta_time):
        if self.game_over:
            return
        self.move_timer += delta_time

        if self.move_timer >= self.move_delay:
            self.move_timer = 0

            for i in range(len(self.snake_list) - 1, 0, -1):
                self.snake_list[i].center_x = self.snake_list[i-1].center_x
                self.snake_list[i].center_y = self.snake_list[i-1].center_y

            #move head
            head = self.snake_list[0]
            head.center_x += self.direction[0]
            head.center_y += self.direction[1]

            #check for collision with food
            food_hit = arcade.check_for_collision_with_list(head, self.food_list)
            for food in food_hit:
                self.food_list.remove(food)
                #add new segment to snake
                new_segment = arcade.SpriteSolidColor(20, 20, color=arcade.color.GREEN)
                new_segment.center_x = self.snake_list[-1].center_x
                new_segment.center_y = self.snake_list[-1].center_y
                self.snake_list.append(new_segment)

                #create new food
                self.food = arcade.SpriteSolidColor(20, 20, color=arcade.color.RED)
                self.food.center_x = random.randint(0, (self.game_size - 20) // 20) * 20
                self.food.center_y = random.randint(0, (self.game_size - 20) // 20) * 20
                self.food_list.append(self.food)

            #check for collision with walls
            if head.center_x < 0 or head.center_x >= self.game_size or head.center_y < 0 or head.center_y >= self.game_size:
                self.game_over = True

            #check for collision with self
            for segment in self.snake_list[1:]:
                if arcade.check_for_collision(head, segment):
                    self.game_over = True

#change snake direction
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP and self.direction != (0, -20):
            self.direction = (0, 20)
        elif key == arcade.key.DOWN and self.direction != (0, 20):
            self.direction = (0, -20)
        elif key == arcade.key.LEFT and self.direction != (20, 0):
            self.direction = (-20, 0)
        elif key == arcade.key.RIGHT and self.direction != (-20, 0):
            self.direction = (20, 0)

#create food





#detect collision with food and grow snake

#scoreboard

#detect collision with walls and self and end game

#restart game

#main game loop

#intro screen


menu = MenuView()
window.show_view(menu)
arcade.run()