#!/usr/bin/env python3
import random
import tkinter
import math

num = 5
current_move = 1
p1_score = 0
p2_score = 0

adjacencies = [
    [0, 1, 1, 1, 1],
    [1, 0, 1, 1, 1],
    [1, 1, 0, 1, 1],
    [1, 1, 1, 0, 1],
    [1, 1, 1, 1, 0]
]

current_player = 1

moves = []

triangles = []

def generate_triangles(n):
    global triangles
    global num
    global adjacencies
    num = n
    triangles = []
    l = []
    for v in range(0, n-2):
        l.append([v, v+1, n-1, v])
    l.append([n-2, 0, n-1, n-2])
    
    for x in l:
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
            if i != j:
                if abs(i - j) == 1: # perimiter vertices next to each other
                    adjacencies[i].append(1)
                elif i == n-1 or j == n-1: #central vertex involved
                    adjacencies[i].append(1)
                elif i == n-2 and j == 0: # first and last initial vertex
                    adjacencies[i].append(1)
                elif i == 0 and j == n-2: # first and last initial vertex
                    adjacencies[i].append(1)
                else: 
                    adjacencies[i].append(0)
            else:
                adjacencies[i].append(0)

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
        if x[1] == 1 or x[1] == 3:
            if moves[x[0] - 1][3] == 1:
                p1_score += 1
            if moves[x[0] - 1][3] == 2:
                p2_score += 1

generate_triangles(int(input("Wheel graph on how many vertices? > ")))
window = tkinter.Tk()
w = tkinter.Canvas(window, width=800, height=800) 
w.pack()

lines = {}
for x in range(0, num):
    lines[x] = {}
for x in range(0, num-1):
    w.create_oval(390+300*math.cos(2*math.pi*x/(num-1)), 390+300*math.sin(2*math.pi*x/(num-1)), 410+300*math.cos(2*math.pi*x/(num-1)), 410+300*math.sin(2*math.pi*x/(num-1)), fill='black')
    w.create_text(400+350*math.cos(2*math.pi*x/(num-1)), 400+350*math.sin(2*math.pi*x/(num-1)),fill="black",font="Times 20 bold", text=f"{x}")
w.create_oval(390, 390, 410, 410, fill="black")
for i in range(0, num):
    for j in range(0, num):
        if adjacencies[i][j] != 0:
            if i == num-1 or j == num-1:
                lines[i][j] = w.create_line(400+300*math.cos(2*math.pi*min(i, j)/(num-1)), 400+300*math.sin(2*math.pi*min(i, j)/(num-1)), 400, 400, fill="blue", width=5)
            else:
                lines[i][j] = w.create_line(400+300*math.cos(2*math.pi*i/(num-1)), 400+300*math.sin(2*math.pi*i/(num-1)), 400+300*math.cos(2*math.pi*j/(num-1)), 400+300*math.sin(2*math.pi*j/(num-1)), fill="blue", width=5)
w.create_text(400+50*math.cos(2*math.pi*1.5/(num-1)), 400+50*math.sin(2*math.pi*1.5/(num-1)),fill="black",font="Times 20 bold", text=f"{num-1}")
scoreboard = w.create_text(100, 70, fill="black", font="Times 20 bold", text=f"{current_move} edges marked\n\nPlayer {current_player} is up!")


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
    if [v1, v2] not in previous_edges_marked and v1 != v2 and v1 < num and v2 < num and adjacencies[v1][v2] != 0:
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
            if v1 == num-1 or v2 == num-1:
                lines[v1][v2] = w.create_line(400+300*math.cos(2*math.pi*min(v1, v2)/(num-1)), 400+300*math.sin(2*math.pi*min(v1, v2)/(num-1)), 400, 400, fill="black", width=5)
            else:
                lines[v1][v2] = w.create_line(400+300*math.cos(2*math.pi*v1/(num-1)), 400+300*math.sin(2*math.pi*v1/(num-1)), 400+300*math.cos(2*math.pi*v2/(num-1)), 400+300*math.sin(2*math.pi*v2/(num-1)), fill="black", width=5)
        if sign == '+':
            if v1 == num-1 or v2 == num-1:
                lines[v1][v2] = w.create_line(400+300*math.cos(2*math.pi*min(v1, v2)/(num-1)), 400+300*math.sin(2*math.pi*min(v1, v2)/(num-1)), 400, 400, fill="red", width=5)
            else:
                lines[v1][v2] = w.create_line(400+300*math.cos(2*math.pi*v1/(num-1)), 400+300*math.sin(2*math.pi*v1/(num-1)), 400+300*math.cos(2*math.pi*v2/(num-1)), 400+300*math.sin(2*math.pi*v2/(num-1)), fill="red", width=5)
        
        if current_player == 1:
            current_player = 2
        else:
            current_player = 1
    else: 
        print("Invalid move!")

import time

delay = float(input("Delay between each move? (in seconds) > "))
positive_chance = float(input("Chance to mark an edge positive? (0-1) > "))

time.sleep(1)
while p1_score == 0 and p2_score == 0: #ends the loop once all possible moves have been made
    if p1_score == 0 and p2_score == 0:
        w.itemconfig(scoreboard, text=f"{current_move - 1} edges marked\n\nPlayer {current_player} is up!")
        previous_edges = [x[0:2] for x in moves]
        v1 = math.floor(random.random()*num)
        v2 = math.floor(random.random()*num)
        vertices = [v1, v2]
        v1 = min(vertices)
        v2 = max(vertices)
        while [v1, v2] in previous_edges or v1 == v2 or adjacencies[v1][v2] == 0: #deals with invalid moves
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
        w.itemconfig(scoreboard, text=f"{current_move - 1} edges marked\n\nPlayer {current_player} is up!")
        w.update()
w.itemconfig(scoreboard, text=f"{current_move - 1} edges marked\n\nPlayer {2 - (len(moves) % 2)} won!\n\nGame over!")
w.update()
time.sleep(10)