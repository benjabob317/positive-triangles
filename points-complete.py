#!/usr/bin/env python3
adjacencies = [
    [0, 1, 1, 1, 1],
    [1, 0, 1, 1, 1],
    [1, 1, 0, 1, 1],
    [1, 1, 1, 0, 1],
    [1, 1, 1, 1, 0]
]

moves = []

triangles = []

def move(v1, v2, sign, player):
    