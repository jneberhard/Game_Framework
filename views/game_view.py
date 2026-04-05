import arcade
import random
from utils.food import create_food, create_poison
from utils.scores import load_scores, update_scores

class GameView(arcade.View):
    def __init__(self, game_size=600, game_speed=0.15, progressive=False):
        super().__init__()
        #arcade.set_background_color(arcade.color.BLUE)
        self.game_size = game_size
        #make the grass texture
        self.grass_texture = arcade.load_texture("assets/textures/grass03.png")

        self.grass_list = arcade.SpriteList()
        grass = arcade.Sprite()
        grass.texture = self.grass_texture
        grass.center_x = self.game_size // 2
        grass.center_y = self.game_size // 2
        grass.width = self.game_size
        grass.height = self.game_size
        self.grass_list.append(grass)
        self.game_speed = game_speed
        self.progressive = progressive
        self.move_delay = self.game_speed
        self.move_timer = 0
        self.direction = (20, 0)
        self.game_over = False
        self.window.set_size(self.game_size, self.game_size)
        self.snake_list = arcade.SpriteList()
        self.high_score = max([entry["score"] for entry in load_scores()])
        self.collision_sound = arcade.load_sound("assets/audio/big_boom.mp3")
        self.eat_sound = [
            arcade.load_sound("assets/audio/yummy.mp3"),
            arcade.load_sound("assets/audio/go.mp3"),
            arcade.load_sound("assets/audio/go1.mp3"),
            arcade.load_sound("assets/audio/go2.mp3"),
            arcade.load_sound("assets/audio/go3.mp3")
        ]
        self.start_delay = 1.5
        self.paused = False
        self.pause_text = arcade.Text("PAUSED - Press P to continue", self.game_size // 2, self.game_size // 2, arcade.color.WHITE, 25, anchor_x="center")
        self.score = 0
        self.score_text = arcade.Text(f"Score: {self.score}", 10, self.game_size - 25, arcade.color.WHITE, 18)  #use arcade.Text
        self.poison_list = arcade.SpriteList()

        #create snake head and 2 segments
        starting_positions = [(0, 0), (-20, 0), (-40, 0)]

        for i, position in enumerate(starting_positions):
            if i == 0:
                segment = arcade.Sprite("assets/textures/snake_head.png", scale=.625)
            else:
                segment = arcade.Sprite("assets/textures/snake_body.png", scale=.625)
            segment.center_x = (self.game_size // 2) + position[0]
            segment.center_y = (self.game_size // 2) + position[1]
            self.snake_list.append(segment)

        #create food if it does not exist
        self.food_list = arcade.SpriteList()
        self.food = create_food(self.food_list, self.game_size, self.snake_list)

    #draw the play screen
    def on_draw(self):
        self.clear()
        self.grass_list.draw()
        #make a border on the outside
        arcade.draw_lrbt_rectangle_outline(0, self.game_size, 0, self.game_size, arcade.color.WHITE, border_width=10)
        self.snake_list.draw()
        self.food_list.draw()
        self.poison_list.draw()
        self.score_text.draw()
        if self.paused:
            self.pause_text.draw()

        #draw high score in top right
        high_score_text = arcade.Text(f"High Score: {self.high_score}", self.game_size - 10, self.game_size - 25,
            arcade.color.YELLOW, 18, anchor_x="right")
        high_score_text.draw()

    #what happens with each movement
    def on_update(self, delta_time):

        #pause before snake starts
        if self.start_delay > 0:
            self.start_delay -= delta_time
            return
        if self.paused:
            return
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

            #check for collision with food and grow snake
            food_hit = arcade.check_for_collision_with_list(head, self.food_list)
            for food in food_hit:
                self.food_list.remove(food)
                sound = random.choice(self.eat_sound)
                arcade.play_sound(sound)
                #add new segment to snake
                new_segment = arcade.Sprite("assets/textures/snake_body.png", scale=.625)
                new_segment.center_x = self.snake_list[-1].center_x
                new_segment.center_y = self.snake_list[-1].center_y
                self.snake_list.append(new_segment)

                #create new food (from utils food.py)
                self.food = create_food(self.food_list, self.game_size, self.snake_list)

                #add to the score
                self.score += 1
                self.score_text.text = f"Score: {self.score}"

                if self.score %5 == 0:
                    create_poison(self.poison_list, self.game_size, self.snake_list)


                #if in progressive mode, make each time you eat the snake moves faster
                if self.progressive:
                    self.move_delay = max(0.02, self.move_delay - .005)

            #check for collision with walls - end game
            border = 10
            head = self.snake_list[0]
            if (
                head.center_x <= border or
                head.center_x >= self.game_size - border or
                head.center_y <= border or
                head.center_y >= self.game_size - border
            ):
                self.handle_game_over()


            #check for collision with self - end game
            for segment in self.snake_list[1:]:
                if arcade.check_for_collision(head, segment):
                    self.handle_game_over()

            #check for collision with poison
            poison_hit = arcade.check_for_collision_with_list(head, self.poison_list)
            if poison_hit:
                self.handle_game_over()

    def handle_game_over(self):
        if self.game_over:
            return

        arcade.play_sound(self.collision_sound)
        self.game_over = True
        top_scores = load_scores()

        from views.high_score_view import HighScore
        from views.game_over_view import GameOver

        #if top 10, go to initial entry screen to enter initials
        if self.score > top_scores[-1]["score"]:
            entry_view = HighScore(self.score, self.game_size, self.game_speed, self.progressive)
            self.window.show_view(entry_view)

        #if not in top 10, go to game over view
        else:
            update_scores(self.score, "---")
            game_over_view = GameOver(self.score, self.game_size, self.game_speed, self.progressive)
            self.window.show_view(game_over_view)


#change snake direction
    def on_key_press(self, key, modifiers):
        if (key == arcade.key.UP or key == arcade.key.W) and self.direction != (0, -20):
            self.direction = (0, 20)
        elif (key == arcade.key.DOWN or key == arcade.key.S) and self.direction != (0, 20):
            self.direction = (0, -20)
        elif (key == arcade.key.LEFT or key == arcade.key.A) and self.direction != (20, 0):
            self.direction = (-20, 0)
        elif (key == arcade.key.RIGHT or key == arcade.key.D) and self.direction != (-20, 0):
            self.direction = (20, 0)
        elif key == arcade.key.P:
            self.paused = not self.paused
            return
