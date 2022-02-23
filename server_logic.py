from operator import pos
import random
import math
from typing import List, Dict


def avoid_the_wall(my_head, the_board_height, the_board_width, possible_moves: List[str]) -> List[str]:    
    if my_head["x"] == 0:
        try_remove_move("left", possible_moves)
    if my_head["y"] == 0:
        try_remove_move("down", possible_moves)
    if my_head["x"] == the_board_width-1:
        try_remove_move("right", possible_moves)
    if my_head["y"] == the_board_height-1:
        try_remove_move("up", possible_moves)

    return possible_moves


def avoid_snake(my_head: Dict[str, int], snake_body: List[dict], possible_moves: List[str]) -> List[str]:
    for i in range(0, len(snake_body)):
        body_part = snake_body[i]
        if body_part["y"] == my_head["y"]:
            difference = body_part["x"] - my_head["x"]
            if difference == 1:
                try_remove_move("right", possible_moves)
            elif difference == -1:
                try_remove_move("left", possible_moves)
        
        if body_part["x"] == my_head["x"]:
            difference = body_part["y"] - my_head["y"]
            if difference == 1:
                try_remove_move("up", possible_moves)
            elif difference == -1:
                try_remove_move("down", possible_moves)

    return possible_moves


def point_distance(point1, point2):
    return math.sqrt((point1["x"]-point2["x"])**2 + (point1["y"]-point2["y"])**2)


def find_food_moves(my_head, foods, possible_moves):
    if len(possible_moves) < 1:
        return possible_moves
    if len(foods) == 0:
        return possible_moves

    closest_food = foods[0]
    closest_distance = point_distance(my_head, closest_food)
    for food in foods[1:]:
        current_distance = point_distance(my_head, food)
        if current_distance < closest_distance:
            closest_food = food
            closest_distance = current_distance

    good_moves = []

    if my_head["x"] > closest_food["x"]:
        good_moves.append("left")
    elif my_head["x"] < closest_food["x"]:
        good_moves.append("right")
    if my_head["y"] > closest_food["y"]:
        good_moves.append("down")
    elif my_head["y"] < closest_food["y"]:
        good_moves.append("up")

    move_intersection = set(possible_moves).intersection(set(good_moves))
    if len(move_intersection) > 0:
        return list(move_intersection)
    return possible_moves
    
def go_centric(my_head, the_board_height, the_board_width, possible_moves):
    if(len(possible_moves) < 1):
        return possible_moves
    
    cy = (int)(the_board_height/2)
    cx = (int)(the_board_width/2)

    good_moves = []

    if my_head["x"] > cx:
        good_moves.append("left")
    elif my_head["x"] < cx:
        good_moves.append("right")
    if my_head["y"] > cy:
        good_moves.append("down")
    elif my_head["y"] < cy:
        good_moves.append("up")

    move_intersection = set(possible_moves).intersection(set(good_moves))
    if len(move_intersection) > 0:
        return list(move_intersection)
    return possible_moves


def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    my_head = data["you"]["head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
    my_body = data["you"]["body"]  # A list of x/y coordinate dictionaries like [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]

    # TODO: uncomment the lines below so you can see what this data looks like in your output!
    # print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    # print(f"All board data this turn: {data}")
    # print(f"My Battlesnakes head this turn is: {my_head}")
    # print(f"My Battlesnakes body this turn is: {my_body}")

    possible_moves = ["up", "down", "left", "right"]
    print(possible_moves)

    # do not hit any walls
    the_board_height = data["board"]["height"]
    the_board_width = data["board"]["width"]
    possible_moves = avoid_the_wall(my_head, the_board_height, the_board_width, possible_moves)
    print(possible_moves)


    # do not hit anybody
    possible_moves = avoid_snake(my_head, my_body, possible_moves)
    for snake in data["board"]["snakes"]:
        snake_body = snake["body"]
        possible_moves = avoid_snake(my_head, snake_body, possible_moves)

    # try to move towards food
    possible_moves = find_food_moves(my_head, data["board"]["food"], possible_moves)

    # if have a choice go centric
    possible_moves = go_centric(my_head, the_board_height, the_board_width, possible_moves)

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    move = random.choice(possible_moves)
    # TODO: Explore new strategies for picking a move that are better than random

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move

def try_remove_move(move, possible_moves):
    if move in possible_moves:
        possible_moves.remove(move)