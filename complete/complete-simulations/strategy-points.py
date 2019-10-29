#!/usr/bin/env python3
import random
import tkinter
import math

num = 5
current_move = 1
p1_score = 0
p2_score = 0

current_player = 1

adjacencies = [
    [0, 1, 1, 1, 1],
    [1, 0, 1, 1, 1],
    [1, 1, 0, 1, 1],
    [1, 1, 1, 0, 1],
    [1, 1, 1, 1, 0]
]


moves = []

triangles = []

def generate_triangles(n):
    global triangles
    global num
    global adjacencies
    num = n
    triangles = []
    l = []
    iterate_l = [x for x in range(0, n)]
    for v1 in iterate_l:
        v2_l = iterate_l.copy()
        v2_l.remove(v1)
        for v2 in v2_l:
            v3_l = iterate_l.copy()
            v3_l.remove(v1)
            v3_l.remove(v2)
            for v3 in v3_l:
                l.append([v1, v2, v3])

    l2 = l.copy()
    for x in l2:
        x.sort()
        
    l3 = []
    for x in l2:
        if x not in l3:
            l3.append(x)
    for x in range(0, len(l3)):
        l3[x].append(l3[x][0])
    for x in l3:
        new_data = []
        for i in range(0, 3):
            data = [x[i], x[i+1]]
            data.sort()
            data.append('a')
            new_data.append(data)
        triangles.append(new_data)
    adjacencies = []
    for i in range(0, n):
        adjacencies.append([])
        for j in range(0, n):
            if i == j:
                adjacencies[i].append(0)
            else:
                adjacencies[i].append(1)

def check_triangles(): # used to update scores
    filled_triangles = []
    global p1_score
    global p2_score
    for x in range(0, len(triangles)):
        counter = 0
        sign_counter = 0
        for i in range(0, 3):
            if triangles[x][i][2] != 'a':
                counter += 1
                if moves[triangles[x][i][2] - 1][2] == "+":
                    sign_counter += 1
        if counter == 3:
            filled_triangles.append([max([i[2] for i in triangles[x]]), sign_counter])

    p1_score = 0
    p2_score = 0
    for x in filled_triangles:
        if x[1] == 1 or x[1] == 3: #if triangle is positive
            if moves[x[0] - 1][3] == 1:
                p1_score += 1
            if moves[x[0] - 1][3] == 2:
                p2_score += 1

generate_triangles(int(input("Complete graph on how many vertices? > ")))
window = tkinter.Tk()
w = tkinter.Canvas(window, width=800, height=800) 
w.pack()

lines = {}
for x in range(0, num):
    lines[x] = {}
for x in range(0, num):
    w.create_oval(390+300*math.cos(2*math.pi*x/num), 390+300*math.sin(2*math.pi*x/num), 410+300*math.cos(2*math.pi*x/num), 410+300*math.sin(2*math.pi*x/num), fill='black')
    w.create_text(400+350*math.cos(2*math.pi*x/num), 400+350*math.sin(2*math.pi*x/num),fill="black",font="Times 20 bold", text=f"{x}")
for i in range(0, num):
    for j in range(0, num):
        lines[i][j] = w.create_line(400+300*math.cos(2*math.pi*i/num), 400+300*math.sin(2*math.pi*i/num), 400+300*math.cos(2*math.pi*j/num), 400+300*math.sin(2*math.pi*j/num), fill="blue", width=5)

scoreboard = w.create_text(100, 70, fill="black", font="Times 20 bold", text=f"{current_move} edges marked\n\nP1 score: {p1_score}\nP2 score: {p2_score}\n\nPlayer {current_player} is up!")

def safe_moves(): # generates a list of moves that do not involve any already moved on vertices
    previous_edges = [x[0:2] for x in moves]
    previous_vertices = []
    for x in previous_edges:
        if x[0] not in previous_vertices:
            previous_vertices.append(x[0])
        if x[1] not in previous_vertices:
            previous_vertices.append(x[1])
    safe_vertices = [x for x in range(0, num)]
    for x in previous_vertices:
        safe_vertices.remove(x)
    l = []
    for i in safe_vertices:
        for j in (safe_vertices[0:i] + safe_vertices[i+1:len(safe_vertices)]):
            edge = [i, j]
            l.append([min(edge), max(edge)])
    valid_moves = []
    for x in l:
        if x not in valid_moves and x[0] != x[1]:
            valid_moves.append(x)
    return valid_moves 

def scoring_moves(): # used to find moves that will fill a triangle
    edges = []
    for x in range(0, len(triangles)):
        counter = 0
        sign_counter = 0
        unfilled_edges = []
        for i in range(0, 3):
            if triangles[x][i][2] != 'a':
                counter += 1
                if moves[triangles[x][i][2] - 1][2] == "+":
                    sign_counter += 1
            else:
                unfilled_edges.append(triangles[x][i][0:2])
        if counter == 2:
            if sign_counter == 1:
                unfilled_edges[0].append('-')
            else:
                unfilled_edges[0].append('+')
            edges.append(unfilled_edges[0])

    return edges
    

def move(v1, v2, sign, player):
    global moves
    global triangles
    global current_move
    global adjacencies
    global current_player
    vertices = [v1, v2]
    v1 = min(vertices)
    v2 = max(vertices)
    previous_edges_marked = [x[0:2] for x in moves]
    if [v1, v2] not in previous_edges_marked and v1 != v2 and v1 < num and v2 < num:
        moves.append([v1, v2, sign, player])
        for tri in range(0, len(triangles)):
            for edge in range(0, 3):
                if triangles[tri][edge][0:2] == [v1, v2]:
                    triangles[tri][edge][2] = current_move
        adjacencies[v1][v2] = sign
        adjacencies[v2][v1] = sign
        current_move += 1
        
        w.delete(lines[v1][v2])
        if sign == '-':
            lines[v1][v2] = w.create_line(400+300*math.cos(2*math.pi*v1/num), 400+300*math.sin(2*math.pi*v1/num), 400+300*math.cos(2*math.pi*v2/num), 400+300*math.sin(2*math.pi*v2/num), fill="black", width=5)
        if sign == '+':
            lines[v1][v2] = w.create_line(400+300*math.cos(2*math.pi*v1/num), 400+300*math.sin(2*math.pi*v1/num), 400+300*math.cos(2*math.pi*v2/num), 400+300*math.sin(2*math.pi*v2/num), fill="red", width=5)
        
        if current_player == 1:
            current_player = 2
        else:
            current_player = 1
    else: 
        print(f"{v1, v2} is an invalid move!")

import time

delay = float(input("Delay between each move? (in seconds) > "))
positive_chance = float(input("Chance to mark an edge positive? (0-1) > "))

time.sleep(1)
while len(moves) < num*(num-1)/2: #ends the loop once all possible moves have been made
    print(safe_moves())
    print(scoring_moves())
    w.itemconfig(scoreboard, text=f"{current_move - 1} edges marked\n\nP1 score: {p1_score}\nP2 score: {p2_score}\n\nPlayer {current_player} is up!")
    
    if len(scoring_moves()) > 0:
        next_move = random.choice(scoring_moves())
        v1 = next_move[0]
        v2 = next_move[1]
        sign = next_move[2]
    elif len(safe_moves()) > 0:
        next_move = random.choice(safe_moves())
        v1 = next_move[0]
        v2 = next_move[1]
        sign = random.random()
        if sign < positive_chance:
            sign = '+'
        else:
            sign = '-'
    else:
        previous_edges = [x[0:2] for x in moves]
        v1 = math.floor(random.random()*num)
        v2 = math.floor(random.random()*num)
        vertices = [v1, v2]
        v1 = min(vertices)
        v2 = max(vertices)
        while [v1, v2] in previous_edges or v1 == v2: #deals with invalid moves
            v1 = math.floor(random.random()*num)
            v2 = math.floor(random.random()*num)
            vertices = [v1, v2]
            v1 = min(vertices)
            v2 = max(vertices)
        sign = random.random()
        if sign < positive_chance:
            sign = '+'
        else:
            sign = '-'

    move(int(v1), int(v2), sign, current_player)
    check_triangles()
    time.sleep(delay)
    w.itemconfig(scoreboard, text=f"{current_move - 1} edges marked\n\nP1 score: {p1_score}\nP2 score: {p2_score}\n\nPlayer {current_player} is up!")
    w.update()
w.itemconfig(scoreboard, text=f"{current_move - 1} edges marked\n\nP1 score: {p1_score}\nP2 score: {p2_score}\n\nGame over!")
w.update()
time.sleep(10)