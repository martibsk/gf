import numpy as np
import cv2
import copy
import time
import random
import os




def playSnake(
    games_played,
    del_tale = True,
    snake = list(),
    solid_wall = True,
    snake_length = 4,
    speed = 12,
    thick = 30,
    height_board = 25,
    width_board = 25,
    bonus = False):

    board_h = thick * height_board
    board_w = thick * width_board
    board = 255 * np.ones(shape=[board_h+20, board_w + 300, 3], dtype=np.uint8)
    bonus_count = 0
    bonus_vis = False
    bonus_score = 0

    # Generate the valuable keys
    valuable_keys = list()
    valuable_keys.append(ord('w'))
    valuable_keys.append(ord('a'))
    valuable_keys.append(ord('s'))
    valuable_keys.append(ord('d'))
    valuable_keys.append(ord('q'))
    valuable_keys.append(81)
    valuable_keys.append(82)
    valuable_keys.append(83)
    valuable_keys.append(84)
    valuable_keys.append(ord('p'))

    # Retrieve the current highscore
    if solid_wall:
        try:
            file = '/home/martibsk/dev/snake/highscores/highscore_solid_b'+ str(width_board) + '_h' + str(height_board) + 's_' + str(speed) + 'bonus_' + str(bonus) + '.txt'
            f = open(file, 'r')
            highscore = int(f.readline())
            f.close()
        except:
            highscore = 0
        text_solid = 'Wall: Solid'
    else:
        try:
            f = open('/home/martibsk/dev/snake/highscores/highscore_not_solid_b'+ str(width_board) + '_h' + str(height_board) + 's_' + str(speed) + 'bonus_' + str(bonus) + '.txt', 'r')
            highscore = int(f.readline())
            f.close()
        except:
            highscore = 0
        text_solid = 'Wall: Transparent'


    max_goal1 = board_w/thick - 1
    max_goal2 = board_h/thick - 1

    # Draw the first bite
    goal = [10,10]
    g1 = np.array(goal)*thick + thick/2
    g2 = g1 + thick/2
    cv2.rectangle(board, tuple(g1), tuple(g2), [0,0,255], thickness = thick/3)
    cv2.rectangle(board, (5,5), (board_w+10, board_h+10), [0,0,0], thickness = 3)

    for k in range(0,snake_length):
        snake.append([k,0])

    k = 1
    while True:

        score = len(snake)-snake_length
        # Visualize the snake
        snake_vis = np.array(snake)
        snake_vis = snake_vis*thick

        new_board = copy.deepcopy(board)
        head_placed = False
        for pos in reversed(snake_vis):
            pos1 = np.array(pos) + thick/2
            pos2 = pos1+thick/2
            pos1 = tuple(pos1)
            pos2 = tuple(pos2)

            if head_placed:
                cv2.rectangle(new_board, pos1, pos2, [255,0,0], thickness = thick/3)
            else:
                cv2.rectangle(new_board, pos1, pos2, [200,0,0], thickness = thick/3)
                head_placed = True

        if games_played > 0:
            text_games_played = 'Games played: {}'.format(games_played)
            cv2.rectangle(new_board, (board_w + 30, int(board_h*0.9)), (board_w + 270, int(board_h*0.95)), [255,100,255], thickness = 20)
            cv2.putText(new_board, text_games_played, (board_w + 30, int(board_h*0.95)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, [0,0,0], 2)

        text_board_size1 = 'Board Info'
        text_board_size2 = 'W: {}'.format(width_board)
        text_board_size3 = 'H: {}'.format(height_board)
        text_speed = 'Speed: {}'.format(speed)
        text_bonus = 'Bonus: {}'.format(bonus)
        text1 = "Highscore: {}".format(highscore)
        text2 = "Score: {}".format(score + bonus_score)
        text_score1 = 'Normal: {}'.format(score)
        text_score2 =  'Bonus: {}'.format(bonus_score)
        cv2.putText(new_board, text_board_size1, (board_w + 30, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, [0,0,0], 2)
        cv2.putText(new_board, text_board_size2, (board_w + 40, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,0,0], 1)
        cv2.putText(new_board, text_board_size3, (board_w + 40, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,0,0], 1)
        cv2.putText(new_board, text_solid, (board_w + 40, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,0,0], 1)
        cv2.putText(new_board, text_speed, (board_w + 40, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,0,0], 1)
        cv2.putText(new_board, text_bonus, (board_w + 40, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,0,0], 1)
        cv2.putText(new_board, text1, (board_w + 30, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, [0,0,0], 2)
        cv2.putText(new_board, text2, (board_w + 30, 145), cv2.FONT_HERSHEY_SIMPLEX, 0.8, [0,0,0], 2)
        cv2.putText(new_board, text_score1, (board_w + 35, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,0,0], 1)
        cv2.putText(new_board, text_score2, (board_w + 35, 175), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,0,0], 1)
        cv2.imshow('snake', new_board)
        key = cv2.waitKey(1000/speed) & 0xFF

        if key == ord('p'):
            key = ord('o')
            while key not in valuable_keys:
                cv2.putText(new_board, '(p)', (int(board_w/2-30), int(board_h/2)), cv2.FONT_HERSHEY_SIMPLEX, 1.5, [0,0,0], 3)
                cv2.imshow('snake', new_board)
                key = cv2.waitKey() & 0xFF
        if key == ord('q'):
            break
        elif (key == ord('w') or key == 82) and k != 2:
            k = 0
        elif (key == ord('a') or key == 81) and k != 1:
            k = 3
        elif (key == ord('s') or key == 84) and k != 0:
            k = 2
        elif (key == ord('d') or key == 83) and k != 3:
            k = 1
        else:
            k = k


        # Use copy in order to not change the original snake
        head_pos = copy.deepcopy(snake[-1])

        # Create the new snake head after movement
        if k == 0:
            head_pos[1] = head_pos[1] - 1
        elif k == 1:
            head_pos[0] = head_pos[0] + 1
        elif k == 2:
            head_pos[1] = head_pos[1] + 1
        elif k == 3:
            head_pos[0] = head_pos[0] - 1

        # Generate the new snake after head is moved
        if del_tale:
            del snake[0]
        else:
            del_tale = True

        if solid_wall:
            if head_pos in snake or head_pos[0] < 0 or head_pos[1] < 0 or head_pos[0]*thick > board_w-thick or head_pos[1]*thick > board_h-thick:
                break
            else:
                snake.append(head_pos)
        else:
            if head_pos in snake:
                break
            else:
                if head_pos[0] > board_w/thick - 1:
                    head_pos[0] = 0
                elif head_pos[1] > board_h/thick - 1:
                    head_pos[1] = 0
                elif head_pos[0] < 0:
                    head_pos[0] = board_w/thick - 1
                elif head_pos[1] < 0:
                    head_pos[1] = board_h/thick - 1
                snake.append(head_pos)

        # Eat the bite
        if goal == head_pos:


            # Remove the bite
            cv2.rectangle(board, tuple(g1), tuple(g2), [255,255,255], thickness = thick/3)

            # Generate new goal
            goal = [random.randint(0,max_goal1),random.randint(0,max_goal2)]
            while goal in snake:
                goal = [random.randint(0,max_goal1),random.randint(0,max_goal2)]
            g1 = np.array(goal)*thick + thick/2
            g2 = g1 + thick/2
            cv2.rectangle(board, tuple(g1), tuple(g2), [0,0,255], thickness = thick/3)
            del_tale = False

            # check for bonus
            if (score+1)%9 == 0:
                bonus_vis = True

                # Generate new bonus
                bonus_bite = [random.randint(0,max_goal1),random.randint(0,max_goal2)]
                while bonus_bite in snake or bonus_bite in goal:
                    bonus_bite = [random.randint(0,max_goal1),random.randint(0,max_goal2)]
                g11 = np.array(bonus_bite)*thick + thick/2
                g22 = g11 + thick/2
                cv2.rectangle(board, tuple(g11), tuple(g22), [255,0,255], thickness = thick/3)

        # Bonus bite
        if bonus_vis:
            if bonus_count > int((width_board + height_board)/2) + 5:
                bonus_vis = False
                bonus_count = 0
                cv2.rectangle(board, tuple(g11), tuple(g22), [255,255,255], thickness = thick/3)
            else:
                if bonus_bite == head_pos:
                    cv2.rectangle(board, tuple(g11), tuple(g22), [255,255,255], thickness = thick/3)
                    bonus_score = bonus_score + 5
                    bonus_vis = False
                    bonus_count = 0
                bonus_count = bonus_count + 1


    # Print scores
    score = len(snake)-snake_length + 1 + bonus_score

    if score > highscore:
        score_text1 = 'Congratulations!'
        score_text2 = 'NEW HIGHSCORE:'
        score_text3 = str(score)
        if solid_wall:
            file = '/home/martibsk/dev/snake/highscores/highscore_solid_b'+ str(width_board) + '_h' + str(height_board) + 's_' + str(speed) + 'bonus_' + str(bonus) + '.txt'
            f = open(file, 'w')
        else:
            file = '/home/martibsk/dev/snake/highscores/highscore_not_solid_b'+ str(width_board) + '_h' + str(height_board) + 's_' + str(speed) + 'bonus_' + str(bonus) + '.txt'
            f = open(file, 'w')

        f.write(str(score))
        f.close()
        cv2.putText(new_board, score_text1, (board_w + 20, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.9, [0,0,255], 2)
        cv2.putText(new_board, score_text2, (board_w + 20, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,0,0], 2)
        cv2.putText(new_board, score_text3, (board_w + 220, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.8, [0,0,255], 2)

    # Ask to play again

    crash(snake, thick, new_board)
    text_play_again1 = 'Want to play again?'
    text_play_again2 = 'yes [y] or no [n]?'
    cv2.putText(new_board, text_play_again1, (board_w + 20, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,0,0], 2)
    cv2.putText(new_board, text_play_again2, (board_w + 20, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,0,0], 2)
    cv2.imshow('snake', new_board)
    key = cv2.waitKey() & 0xFF

    return new_board, key


def crash(snake, thick, new_board):
    # Illustrate the crash
    p1, p2 = snake[-1]
    p1 = p1*thick + thick*3/4
    p2 = p2*thick + thick*3/4
    px = int(thick/3)
    cv2.rectangle(new_board, (p1, p2), (p1, p2), [0,0,255], thickness = px)
    cv2.imshow('snake', new_board)
    key = cv2.waitKey(500)
    cv2.rectangle(new_board, (p1, p2), (p1, p2), [255,255,255], thickness = px)

    cv2.rectangle(new_board, (p1+px, p2+px), (p1+px, p2+px), [0,0,255], thickness = px)
    cv2.rectangle(new_board, (p1-px, p2+px), (p1-px, p2+px), [0,0,255], thickness = px)
    cv2.rectangle(new_board, (p1+px, p2-px), (p1+px, p2-px), [0,0,255], thickness = px)
    cv2.rectangle(new_board, (p1-px, p2-px), (p1-px, p2-px), [0,0,255], thickness = px)

    cv2.imshow('snake', new_board)
    key = cv2.waitKey(300)



if __name__ == '__main__':

    games_played = 0

    while True:
        board, key = playSnake(
        games_played,
        del_tale = True,
        snake = list(),
        solid_wall = False,
        snake_length = 4,
        speed = 11,
        thick = 30,
        height_board = 12,
        width_board = 16,
        bonus = True)

        games_played = games_played + 1
        while key != ord('y') and key != ord('n'):
            key = cv2.waitKey() & 0xFF
        if key == ord('n'):
            break

    cv2.destroyAllWindows()
