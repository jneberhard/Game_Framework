import random
import arcade

def make_food(game_size, snake_list):
    while True:
        border = 10
        grid = 20
        x = random.randint((border // grid)+1, (game_size - border) // grid - 1) * grid
        y = random.randint((border // grid)+1, (game_size - border) // grid - 1) * grid

        #make sure food does not appear in the snake
        collision = False
        for segment in snake_list:
            if segment.center_x == x and segment.center_y == y:
                collision = True
                break

        if not collision:
            return x, y

def create_food(food_list, game_size, snake_list):
    food = arcade.Sprite("assets/textures/food.png", scale=.625)
    x, y = make_food(game_size, snake_list)
    food.center_x = x
    food.center_y = y
    food_list.append(food)

    return food

def create_poison(poison_list, game_size, snake_list):
    poison = arcade.Sprite("assets/textures/poison.png", scale=.625)
    x, y = make_food(game_size, snake_list)
    poison.center_x = x
    poison.center_y = y
    poison_list.append(poison)
    return poison
