# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(d, n):
        if d * (n - 1) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges_used = set()
        for _ in range(d * (n - 1) // 2):
            while True:
                u, v = random.sample(range(n), 2)
                if u not in graph[v] and (u, v) not in edges_used and (v, u) not in edges_used:
                    graph[u].append(v)
                    graph[v].append(u)
                    edges_used.add((u, v))
                    break
        return graph
    
    def isometric_embedding(graph):
        n = len(graph)
        embedding = {i: i for i in range(n)}
        return embedding
    
    def non_rigid_transformations(embedding, grid_size):
        n = len(embedding)
        transformations = 0
        for i in range(n):
            x1, y1 = embedding[i] // grid_size, embedding[i] % grid_size
            for j in range(i + 1, n):
                x2, y2 = embedding[j] // grid_size, embedding[j] % grid_size
                if (x1 != x2 or y1 != y2) and abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                    transformations += 1
        return transformations
    
    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        for i in range(n):
            neighbors = graph[i]
            for j in range(i + 1, n):
                if j not in neighbors and (j, i) not in graph.values():
                    rank += 1
        return rank
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for k in range(i + 1, n):
                if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                    max_row = k
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(n):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        rref = gaussian_elimination(matrix)
        rank = 0
        for row in rref:
            if any(row):
                rank += 1
        return rank
    
    def max_overlap(embedding, grid_size):
        n = len(embedding)
        overlap = 0
        for i in range(n):
            x1, y1 = embedding[i] // grid_size, embedding[i] % grid_size
            for j in range(i + 1, n):
                x2, y2 = embedding[j] // grid_size, embedding[j] % grid_size
                if (x1 == x2 and abs(y1 - y2) <= 1) or (y1 == y2 and abs(x1 - x2) <= 1):
                    overlap += 1
        return overlap
    
    def isometric_embedding(graph):
        n = len(graph)
        embedding = {i: i for i in range(n)}
        return embedding
    
    def non_rigid_transformations(embedding, grid_size):
        n = len(embedding)
        transformations = 0
        for i in range(n):
            x1, y1 = embedding[i] // grid_size, embedding[i] % grid_size
            for j in range(i + 1, n):
                x2, y2 = embedding[j] // grid_size, embedding[j] % grid_size
                if (x1 != x2 or y1 != y2) and abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                    transformations += 1
        return transformations
    
    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        for i in range(n):
            neighbors = graph[i]
            for j in range(i + 1, n):
                if j not in neighbors and (j, i) not in graph.values():
                    rank += 1
        return rank
    
    def max_overlap(embedding, grid_size):
        n = len(embedding)
        overlap = 0
        for i in range(n):
            x1, y1 = embedding[i] // grid_size, embedding[i] % grid_size
            for j in range(i + 1, n):
                x2, y2 = embedding[j] // grid_size, embedding[j] % grid_size
                if (x1 == x2 and abs(y1 - y2) <= 1) or (y1 == y2 and abs(x1 - x2) <= 1):
                    overlap += 1
        return overlap
    
    def isometric_embedding(graph):
        n = len(graph)
        embedding = {i: i for i in range(n)}
        return embedding
    
    def non_rigid_transformations(embedding, grid_size):
        n = len(embedding)
        transformations = 0
        for i in range(n):
            x1, y1 = embedding[i] // grid_size, embedding[i] % grid_size
            for j in range(i + 1, n):
                x2, y2 = embedding[j] // grid_size, embedding[j] % grid_size
                if (x1 != x2 or y1 != y2) and abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                    transformations += 1
        return transformations
    
    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        for i in range(n):
            neighbors = graph[i]
            for j in range(i + 1, n):
                if j not in neighbors and (j, i) not in graph.values():
                    rank += 1
        return rank
    
    def max_overlap(embedding, grid_size):
        n = len(embedding)
        overlap = 0
        for i in range(n):
            x1, y1 = embedding[i] // grid_size, embedding[i] % grid_size
            for j in range(i + 1, n):
                x2, y2 = embedding[j] // grid_size, embedding[j] % grid_size
                if (x1 == x2 and abs(y1 - y2) <= 1) or (y1 == y2 and abs(x1 - x2) <= 1):
                    overlap += 1
        return overlap
    
    def isometric_embedding(graph):
        n = len(graph)
        embedding = {i: i for i in range(n)}
        return embedding
    
    def non_rigid_transformations(embedding, grid_size):
        n = len(embedding)
        transformations = 0
        for i in range(n):
            x1, y1 = embedding[i] // grid_size, embedding[i] % grid_size
            for j in range(i + 1, n):
                x2, y2 = embedding[j] // grid_size, embedding[j] % grid_size
                if (x1 != x2 or y1 != y2) and abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                    transformations += 1
        return transformations
    
    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        for i in range(n):
            neighbors = graph[i]
            for j in range(i + 1, n):
                if j not in neighbors and (j, i) not in graph.values():
                    rank += 1
        return rank
    
    def max_overlap(embedding, grid_size):
        n = len(embedding)
        overlap = 0
        for i in range(n):
            x1, y1 = embedding[i] // grid_size, embedding[i] % grid_size
            for j in range(i + 1, n):
                x2, y2 = embedding[j] // grid_size, embedding[j] % grid_size
                if (x1 == x2 and abs(y1 - y2) <= 1) or (y1 == y2 and abs(x1 - x2) <= 1):
                    overlap += 1
        return overlap
    
    def isometric_embedding(graph):
        n = len(graph)
        embedding = {i: i for i in range(n)}
        return embedding
    
    def non_rigid_transformations(embedding, grid_size):
        n = len(embedding)
        transformations = 0
        for i in range(n):
            x1, y1 = embedding[i] // grid_size, embedding[i] % grid_size
            for j in range(i + 1, n):
                x2, y2 = embedding[j] // grid_size, embedding[j] % grid_size
                if (x1 != x2 or y1 != y2) and abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                    transformations += 1
        return transformations
    
    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        for i in range(n):
            neighbors = graph[i]
            for j in range(i + 1, n):
                if j not in neighbors and (j, i) not in graph.values():
                    rank += 1
        return rank
    
    def max_overlap(embedding, grid_size):
        n = len(embedding)
        overlap = 0
        for i in range(n):
            x1, y1 = embedding[i] // grid_size, embedding[i] % grid_size
            for j in range(i + 1, n):
                x2, y2 = embedding[j] // grid_size, embedding[j] % grid_size
                if (x1 == x2 and abs(y1 - y2) <= 1) or (y1 == y2 and abs(x1 - x2) <= 1):
                    overlap += 1
        return overlap
    
    def isometric_embedding(graph):
        n = len(graph)
        embedding = {i: i for i in range(n)}
        return embedding
    
    def non_rigid_transformations(embedding, grid_size):
        n = len(embedding)
        transformations = 0
        for i in range(n):
            x1, y1 = embedding[i] // grid_size, embedding[i] % grid_size
            for j in range(i + 1, n):
                x2, y2 = embedding[j] // grid_size, embedding[j] % grid_size
                if (x1 != x2 or y1 != y2) and abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                    transformations += 1
        return transformations
    
    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        for i in range(n):
            neighbors = graph[i]
            for j in range(i + 1, n):
                if j not in neighbors and (j, i) not in graph.values():
                    rank += 1
        return rank
    
    def max_overlap(embedding, grid_size):
        n = len(embedding)
        overlap = 0
        for i in range(n):
            x1, y1 = embedding[i] // grid_size, embedding[i] % grid_size
            for j in range(i + 1, n):
                x2, y2 = embedding[j] // grid_size, embedding[j] % grid_size
                if (x1 == x2 and abs(y1 - y2) <= 1) or (y1 == y2 and abs(x1 - x2) <= 1):
                    overlap += 1
        return overlap
    
    def isometric_embedding(graph):
        n = len(graph)
        embedding = {i: i for i in range(n)}
        return embedding
    
    def non_rigid_transformations(embedding, grid_size):
        n = len(embedding)
        transformations = 0
        for i in range(n):
            x1, y1 = embedding[i] // grid_size, embedding[i] % grid_size
            for j in range(i + 1, n):
                x2, y2 = embedding[j] // grid_size, embedding[j] % grid_size
                if (x1 != x2 or y1 != y2) and abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                    transformations += 1
        return transformations
    
    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        for i in range(n):
            neighbors = graph[i]
            for j in range(i + 1, n):
                if j not in neighbors and (j, i) not in graph.values():
                    rank += 1
        return rank
    
    def max_overlap(embedding, grid_size):
        n = len(embedding)
        overlap = 0
        for i in range(n):
            x1, y1 = embedding[i] // grid_size, embedding[i] % grid_size
            for j in range(i + 1, n):
                x2, y2 = embedding[j] // grid_size, embedding[j] % grid_size
                if (x1 == x2 and abs(y1 - y2) <= 1) or (y1 == y2 and abs(x1 - x2) <= 1):
                    overlap += 1
        return overlap
    
    def isometric_embedding(graph):
        n = len(graph)
        embedding = {i: i for i in range(n)}
        return embedding
    
    def non_rigid_transformations(embedding, grid_size):
        n = len(embedding)
        transformations = 0
        for i in range(n):
            x1, y1 = embedding[i] // grid_size, embedding[i] % grid_size
            for j in range(i + 1, n):
                x2, y2 = embedding[j] // grid_size, embedding[j] % grid_size
                if (x1 != x2 or y1 != y2) and abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                    transformations += 1
        return transformations
    
    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        for i in range(n):
            neighbors = graph[i]
            for j in range(i + 1, n):
                if j not in neighbors and (j, i) not in graph.values():
                    rank += 1
        return rank
    
    def max_overlap(embedding, grid_size):
        n = len(embedding)
        overlap = 0
        for i in range(n):
            x1, y1 = embedding[i] // grid_size, embedding[i] % grid_size
            for j in range(i + 1, n):
                x2, y2 = embedding[j] // grid_size, embedding[j] % grid_size
                if (x1 == x2 and abs(y1 - y2) <= 1) or (y1 == y2 and abs(x1 - x2) <= 1):
                    overlap += 1
        return overlap
    
    def isometric_embedding(graph):
        n = len(graph)
        embedding = {i: i for i in range(n)}
        return embedding
    
    def non_rigid_transformations(embedding, grid_size):
        n = len(embedding)
        transformations = 0
        for i in range(n):
            x1, y1 = embedding[i] // grid_size, embedding[i] % grid_size
            for j in range(i + 1, n):
                x2, y2 = embedding[j] // grid_size, embedding[j] % grid_size
                if (x1 != x2 or y1 != y2) and abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                    transformations += 1
        return transformations
    
    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        for i in range(n):
            neighbors = graph[i]
            for j in range(i + 1, n):
                if j not in neighbors and (j, i) not in graph.values():
                    rank += 1
        return rank
    
    def max_overlap(embedding, grid_size):
        n = len(embedding)
        overlap = 0
        for i in range(n):
            x1, y1 = embedding[i] // grid_size, embedding[i] % grid_size
            for j in range(i + 1, n):
                x2, y2 = embedding[j] // grid_size, embedding[j] % grid_size
                if (x1 == x2 and abs(y1 - y2) <= 1) or (y1 == y2 and abs(x1 - x2) <= 1):
                    overlap += 1
        return overlap
    
    def isometric_embedding(graph):
        n = len(graph)
        embedding = {i: i for i in range(n)}
        return embedding
    
    def non_rigid_transformations(embedding, grid_size):
        n = len(embedding)
        transformations = 0
        for i in range(n):
            x1, y1 = embedding[i] // grid_size, embedding[i] % grid_size
            for j in range(i + 1, n):
                x2, y2 = embedding[j] // grid_size, embedding[j] % grid_size
                if (x1 != x2 or y1 != y2) and abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                    transformations += 1
        return transformations
    
    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        for i in range(n):
            neighbors = graph[i]
            for j in range(i + 1, n):
                if j not in neighbors and (j, i) not in graph.values():
                    rank += 1
        return rank
    
    def max_overlap(embedding, grid_size):
        n = len(embedding)
        overlap = 0
        for i in range(n):
            x1, y1 = embedding[i] // grid_size, embedding[i] % grid_size
            for j in range(i + 1, n):
                x2, y2 = embedding[j] // grid_size, embedding[j] % grid_size
                if (x1 == x2 and abs(y1 - y2) <= 1) or (y1 == y2 and abs(x1 - x2) <= 1):
                    overlap += 1
        return overlap
    
    def isometric_embedding(graph):
        n = len(graph)
        embedding = {i: i for i in range(n)}
        return embedding
    
    def non_rigid_transformations(embedding, grid_size):
        n = len(embedding)
        transformations = 0
        for i in range(n):
            x1, y1 = embedding[i] // grid_size, embedding[i] % grid_size
            for j in range(i + 1, n):
                x2, y2 = embedding[j] // grid_size, embedding[j] % grid_size
                if (x1 != x2 or y1 != y2) and abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                    transformations += 1
        return transformations
    
    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        for i in range(n):
            neighbors = graph[i]
            for j in range(i + 1, n):
                if j not in neighbors and (j, i) not in graph.values():
                    rank += 1
        return rank
    
    def max_overlap(embedding, grid_size):
        n = len(embedding)
        overlap = 0
        for i in range(n):
            x1, y1 = embedding[i] // grid_size, embedding[i] % grid_size
            for j in range(i + 1, n):
                x2, y2 = embedding[j] // grid_size, embedding[j] % grid_size
                if (x1 == x2 and abs(y1 - y2) <= 1) or (y1 == y2 and abs(x1 - x2) <= 1):
                    overlap += 1
        return overlap
    
    def isometric_embedding(graph):
        n = len(graph)
        embedding = {i: i for i in range(n)}
        return embedding
    
    def non_rigid_transformations(embedding, grid_size):
        n = len(embedding)
        transformations = 0
        for i in range(n):
            x1, y1 = embedding[i] // grid_size, embedding[i] % grid_size
            for j in range(i + 1, n):
                x2, y2 = embedding[j] // grid_size, embedding[j] % grid_size
                if (x1 != x2 or y1 != y2) and abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                    transformations += 1
        return transformations
    
    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        for i in range(n):
            neighbors = graph[i]
            for j in range(i + 1, n):
                if j not in neighbors and (j, i) not in graph.values():
                    rank += 1
        return rank
    
    def max_overlap(embedding, grid_size):
        n = len(embedding)
        overlap = 0
        for i in range(n):
            x1, y1 = embedding[i] // grid_size, embedding[i] % grid_size
            for j in range(i + 1, n):
                x2, y2 = embedding[j] // grid_size, embedding[j] % grid_size
                if (x1 == x2 and abs(y1 - y2) <= 1) or (y1 == y2 and abs(x1 - x2) <= 1):
                    overlap += 1
        return overlap
    
    def isometric_embedding(graph):
        n = len(graph)
        embedding = {i: i for i in range(n)}
        return embedding
    
    def non_rigid_transformations(embedding, grid_size):
        n = len(embedding)
        transformations = 0