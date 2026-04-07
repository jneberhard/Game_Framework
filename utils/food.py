import random
import arcade

def make_food(game_size, snake_list, poison_list):
    while True:
        border = 10
        grid = 20
        x = random.randint((border // grid)+1, (game_size - border) // grid - 1) * grid
        y = random.randint((border // grid)+1, (game_size - border) // grid - 1) * grid

        if any(segment.center_x == segment.center_y ==y for segment in snake_list):
            continue

        if any(poison.center_x == poison.center_y ==y for poison in poison_list):
            continue

        return x, y

def create_food(food_list, game_size, snake_list, poison_list):
    x, y = make_food(game_size, snake_list, poison_list)

    food = arcade.Sprite("assets/textures/food.png", scale=.625)
    food.center_x = x
    food.center_y = y
    food_list.append(food)

    return food

def create_poison(poison_list, game_size, snake_list, food_list):
    while True:
        border = 10
        grid = 20
        x = random.randint((border // grid) + 1, (game_size - border) // grid - 1) * grid
        y = random.randint((border // grid) + 1, (game_size - border) // grid - 1) * grid

        #avoid snake
        if any(segment.center_x == x and segment.center_y == y for segment in snake_list):
            continue

        # avoid food
        if any(food.center_x == x and food.center_y == y for food in food_list):
            continue

        # avoid other poison
        if any(poison.center_x == x and poison.center_y == y for poison in poison_list):
            continue

        poison = arcade.Sprite("assets/textures/poison.png", scale=.625)
        poison.center_x = x
        poison.center_y = y
        poison_list.append(poison)
        return poison
