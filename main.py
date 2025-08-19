# Instructions 

# Goal:
#   • Work together to reach the black goal circle ("Meaning and Fulfillment").
#   • Both players must enter the goal one at a time or together to finish the game.
#
# Controls:
#   • Player 1:
#       - Left Arrow  → Move Left
#       - Right Arrow → Move Right
#       - Up Arrow    → Jump
#   • Player 2:
#       - A → Move Left
#       - D → Move Right
#       - W → Jump
#
# Gameplay:
#   • Avoid falling off platforms or you’ll lose life.
#   • Interact with special buttons to create bridges or platforms.
#   • "Catch-up" blocks appear permanently once triggered, helping players stay together.
#   • Losing all life = Game Over.
#   • Both players reaching the goal circle = Game Over (restart to Title Screen).
#
# Notes:
#   • The game loops back to the Title Screen after Game Over or victory.
#
# ==============================================

import turtle

# Optional music setup
try:
    import pygame
    pygame.mixer.init()
    pygame.mixer.music.load("[1] - BG GAME MUSIC - CP - PT -.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(10)
except Exception:
    pass

# Screen setup
screen = turtle.Screen()
screen.setup(900, 800)
screen.bgcolor("white")
screen.tracer(0)
screen.title("Paths We Build")
try:
    screen.cv._rootwindow.resizable(False, False)
    screen.cv._rootwindow.iconbitmap("wiz-tab-icon.ico")
except Exception:
    pass

# Constants
GRAVITY = -3
JUMP = 20
BOOST_JUMP = 25
LIFE_LOSS = 10
LIFE_GAIN = 20

# Game state
players, blocks = [], []
life_labels = []
game_running = False
struggle_button = perspective_button = unity_button = None
bridge = platform2 = platform3 = final_step = None
goal = health_pickup = None
support_button = support_platform = None
catchup_blocks = []
final_step_msg_shown = False
winner_declared = False
loser_declared = False
support_unlocked = False  
support_used = False      
players_reached_goal = [False, False]  # track if each player reached the goal

# Create player
def create_player(x):
    p = turtle.Turtle()
    p.shape("circle")
    p.color("#212121")
    p.penup()
    p.goto(x, -200)
    p.dy = 0
    p.life = 100
    return p

# Create block
def create_block(x, y, w, color="black"):
    b = turtle.Turtle()
    b.shape("square")
    b.color(color)
    b.penup()
    b.goto(x, y)
    b.shapesize(1, w)
    return b

# Create life label
def create_life_label(player):
    label = turtle.Turtle()
    label.hideturtle()
    label.color("black")
    label.penup()
    return label

# Create label
def label(text, x, y, font_style="normal", font_size=12):
    t = turtle.Turtle()
    t.hideturtle()
    t.color("black")
    t.penup()
    t.goto(x, y)
    t.write(text, align="center", font=("Courier", font_size, font_style))
    return t

# Title screen
def show_title():
    global game_running, winner_declared, loser_declared, final_step_msg_shown
    global support_unlocked, support_used, players_reached_goal
    game_running = False
    winner_declared = False
    loser_declared = False
    final_step_msg_shown = False
    support_unlocked = False
    support_used = False
    players_reached_goal = [False, False]  #  reset at title

    screen.clear()
    screen.bgcolor("white")
    screen.tracer(0)

    title = turtle.Turtle()
    title.hideturtle()
    title.color("black")
    title.penup()
    title.goto(0, 80)
    title.write("Paths We Build", align="center", font=("Courier", 36, "bold"))

    title.goto(0, 60)
    title.write("Task Performance | Computer Graphics", align="center", font=("Courier", 13, "normal"))

    title.goto(0, 40)
    title.write("Selisana", align="center", font=("Courier", 7, "normal"))

    title.goto(0,10)
    title.write("Press SPACE to begin", align="center", font=("Courier", 16, "normal"))

    screen.onkey(start_game, "space")
    screen.listen()
    screen.update()

# Start game
def start_game():
    global players, blocks, struggle_button, perspective_button, unity_button, bridge, platform2, platform3
    global final_step, goal, life_labels, game_running, health_pickup
    global support_button, support_platform, final_step_msg_shown, catchup_blocks
    global support_unlocked, support_used, players_reached_goal

    screen.clear()
    screen.bgcolor("white")
    screen.tracer(0)
    game_running = True
    final_step_msg_shown = False
    catchup_blocks = []
    support_unlocked = False
    support_used = False
    players_reached_goal = [False, False]  #  reset state

    players = [create_player(-200), create_player(200)]
    life_labels = [create_life_label(players[0]), create_life_label(players[1])]

    blocks = [
        create_block(0, -220, 30),     
        create_block(-150, -100, 10), 
        create_block(150, 0, 10)      
    ]

    struggle_button = create_block(-150, -80, 2, "yellow")
    perspective_button = create_block(150, 10, 2, "orange")
    unity_button = create_block(0, 180, 2, "purple")

    bridge = create_block(0, -40, 20); bridge.hideturtle()
    platform2 = create_block(0, 100, 10); platform2.hideturtle()
    platform3 = create_block(0, 150, 10); platform3.hideturtle()
    final_step = create_block(0, 230, 5, "gray"); final_step.hideturtle()

    goal = turtle.Turtle()
    goal.shape("circle")
    goal.color("black")
    goal.penup()
    goal.goto(0, 250)

    health_pickup = turtle.Turtle()
    health_pickup.shape("circle")
    health_pickup.color("green")
    health_pickup.penup()
    health_pickup.goto(-100, -180)

    # Support objects
    support_button = create_block(-250, -150, 2, "red"); support_button.hideturtle()
    support_platform = create_block(-320, -155, 5, "#9BAC00"); support_platform.hideturtle()

    label("Support lifts others,", -250, 30)
    label("even when unseen.", -270, 10)
    label("Make your way", 300, -100)
    label("to the top.", 285, -115)
    label("Struggles", -150, -70)
    label("Perspective", 150, 50)
    label("Keep going! Malapit ka na.", -160, 130)
    label("You've done it. Proud ako sayo :)", 0, 210)
    label("Meaning and Fulfillment", 0, 290, font_style="bold", font_size=14)

    bind_keys()
    screen.listen()
    screen.update()

# Gravity
def apply_gravity(p):
    p.dy += GRAVITY
    new_y = p.ycor() + p.dy

    platforms = [b for b in blocks + [bridge, platform2, platform3, final_step, support_platform] + catchup_blocks if b and b.isvisible()]
    for b in platforms:
        if abs(p.xcor() - b.xcor()) < b.shapesize()[1]*10 and \
           p.ycor() >= b.ycor() and new_y <= b.ycor() + 10:
            new_y = b.ycor() + 10
            p.dy = 0

    for other in players:
        if other != p and other.isvisible() and abs(p.xcor() - other.xcor()) < 20:
            if p.ycor() >= other.ycor() and new_y <= other.ycor() + 20:
                new_y = other.ycor() + 20
                p.dy = 0

    p.sety(new_y)

# Movement
def move(p, dx): 
    p.setx(p.xcor() + dx)

def jump(p):
    platforms = [b for b in blocks + [bridge, platform2, platform3, final_step, support_platform] + catchup_blocks if b and b.isvisible()]
    for b in platforms:
        if abs(p.xcor() - b.xcor()) < b.shapesize()[1]*10 and abs(p.ycor() - (b.ycor() + 10)) < 5:
            p.dy = JUMP
            return

    for other in players:
        if other != p and other.isvisible() and abs(p.xcor() - other.xcor()) < 20 and \
           abs(p.ycor() - (other.ycor() + 20)) < 5:
            p.dy = BOOST_JUMP
            other.life -= LIFE_LOSS
            update_life_labels()
            if other.life <= 0:
                game_over(other)
            return

# Pressure plate
def is_pressing_plate(plate, threshold=20):
    return any(p.distance(plate) < threshold for p in players if p.isvisible())

# Button logic
def check_buttons(p):
    global final_step_msg_shown, catchup_blocks, support_unlocked, support_used

    if is_pressing_plate(struggle_button):
        bridge.showturtle()
        struggle_button.color("darkred")
        if not support_unlocked:
            support_button.showturtle()
            support_unlocked = True
    else:
        bridge.hideturtle()
        struggle_button.color("yellow")

    if is_pressing_plate(perspective_button):
        platform2.showturtle()
        perspective_button.color("darkred")
        if not any(step.isvisible() for step in catchup_blocks):
            for i in range(5):
                step = create_block(-50 + i*20, -200 + i*40, 4, "#444444")
                catchup_blocks.append(step)
                step.showturtle()
    else:
        platform2.hideturtle()
        perspective_button.color("orange")

    if unity_button and p.distance(unity_button) < 20:
        platform3.showturtle()
        unity_button.color("darkred")

        if len(catchup_blocks) < 10:
            for i in range(5):
                step = create_block(150 - i*20, 30+ i*40, 4, "#5D1300")
                catchup_blocks.append(step)

        if all(pl.distance(unity_button) < 20 for pl in players) and not final_step.isvisible():
            final_step.showturtle()
            if not final_step_msg_shown:
                msg = turtle.Turtle()
                msg.hideturtle()
                msg.color("gray")
                msg.penup()
                msg.goto(0, 200)
                msg.write("Unity unlocks the final step.", align="center", font=("Courier", 12, "italic"))
                final_step_msg_shown = True
    else:
        unity_button.color("purple")

    if support_unlocked and support_button and is_pressing_plate(support_button):
        support_platform.showturtle()
        support_button.color("darkred")
        support_used = True

    if support_used:
        support_platform.showturtle()
        support_button.color("darkred")

# Health
def check_win():
    global winner_declared, players_reached_goal
    if winner_declared:
        return

    if final_step and final_step.isvisible() and goal.isvisible():
        for i, player in enumerate(players):
            if not players_reached_goal[i] and player.isvisible() and player.distance(goal) < 25:
                player.hideturtle()
                players_reached_goal[i] = True

        if all(players_reached_goal):
            winner_declared = True

            # Hide everything
            for obj in players + blocks + [struggle_button, perspective_button, unity_button,
                                           bridge, platform2, platform3, final_step, goal,
                                           health_pickup, support_button, support_platform] \
                                           + life_labels + catchup_blocks:
                if obj:
                    obj.hideturtle()

            # Display "Game Over"
            msg = turtle.Turtle()
            msg.hideturtle()
            msg.color("black")
            msg.penup()
            msg.goto(0, 0)
            msg.write("Game Over", align="center", font=("Courier", 24, "bold"))

            # Return to title after 4 seconds
            screen.ontimer(show_title, 4000)

# Game over
# Game over
def game_over(player):
    global loser_declared
    if loser_declared:
        return
    loser_declared = True

    # Hide everything
    for obj in players + blocks + [struggle_button, perspective_button, unity_button,
                                   bridge, platform2, platform3, final_step, goal,
                                   health_pickup, support_button, support_platform] \
                                   + life_labels + catchup_blocks:
        if obj:
            obj.hideturtle()

    # Display message
    msg = turtle.Turtle()
    msg.hideturtle()
    msg.color("black")
    msg.penup()
    msg.goto(0, 0)

    loser = "Player 1" if player == players[0] else "Player 2"
    msg.write(f"{loser} ran out of life!\nGame Over",
              align="center", font=("Courier", 20, "bold"))

    # Return to title after 3 seconds
    screen.ontimer(show_title, 3000)

# Life labels
def update_life_labels():
    for i, label in enumerate(life_labels):
        p = players[i]
        label.clear()
        if p.isvisible():
            label.goto(p.xcor(), p.ycor() + 30)
            label.write(f"Life: {p.life}", align="center", font=("Courier", 10, "normal"))

# Loop
def loop():
    if game_running:
        for p in players:
            if p.isvisible():
                apply_gravity(p)
                check_buttons(p)

                # ✅ Health pickup detection
                if health_pickup and health_pickup.isvisible() and p.distance(health_pickup) < 25:
                    p.life += LIFE_GAIN
                    if p.life > 100:
                        p.life = 100
                    health_pickup.hideturtle()
                    update_life_labels()

        check_win()
        update_life_labels()
        screen.update()
    screen.ontimer(loop, 50)

# Controls
def bind_keys():
    screen.onkey(lambda: move(players[0], -20), "a")
    screen.onkey(lambda: move(players[0], 20), "d")
    screen.onkey(lambda: jump(players[0]), "w")
    screen.onkey(lambda: move(players[1], -20), "Left")
    screen.onkey(lambda: move(players[1], 20), "Right")
    screen.onkey(lambda: jump(players[1]), "Up")

# Launch
show_title()
loop()
screen.mainloop()
