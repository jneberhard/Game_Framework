import arcade
import os
import json

SCORE_FILE = "snake_scores.json"

def load_scores():
    if not os.path.exists(SCORE_FILE):
        return [{"initials": "---", "score": 0} for _ in range(10)]
    with open(SCORE_FILE, "r") as f:
        return json.load(f)

#saving scores to the json file
def save_scores(scores):
    with open(SCORE_FILE, 'w') as f:
        json.dump(scores, f)

#update the scores to file
def update_scores(new_score, initials):
    scores = load_scores()
    scores.append({"initials": initials, "score": new_score})
    #sort scores (descending)
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:10]
    save_scores(scores)
    return scores

#create high scores
def draw_high_scores(window, center_y):
    scores = load_scores()

    title_text = arcade.Text("High Scores", window.width // 2, center_y + 40,
        arcade.color.YELLOW, 40, anchor_x="center")
    title_text.draw()

    left_x = window.width // 2 - 100
    right_x = window.width // 2 + 100
    y = center_y
    #make it two columns
    for i, entry in enumerate(scores):
        text = f"{i+1}. {entry['initials']}: {entry['score']}"

        if i  < 5:
            score_text = arcade.Text(text, left_x, y - (i * 30),
                arcade.color.YELLOW, 20, anchor_x="center")

        else:
            score_text = arcade.Text(text, right_x, y - ((i-5) * 30),
                arcade.color.YELLOW, 20, anchor_x="center")

        score_text.draw()