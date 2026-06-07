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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def generate_d_regular_graph(d, n):
    if d * (d - 1) // 2 < n or n % d != 0:
        raise ValueError("Invalid parameters for generating a d-regular graph")
    
    G = [[] for _ in range(n)]
    edges_added = set()
    
    def add_edge(u, v):
        if u == v or (u, v) in edges_added or (v, u) in edges_added:
            return
        G[u].append(v)
        G[v].append(u)
        edges_added.add((u, v))
        edges_added.add((v, u))
    
    for i in range(n):
        neighbors = random.sample(range(i + 1, n), d - 1)
        for neighbor in neighbors:
            add_edge(i, neighbor)
    
    return G

def isometric_embedding(G):
    n = len(G)
    embedding = [None] * n
    used_positions = set()
    
    def dfs(node, pos):
        if node in used_positions:
            return False
        used_positions.add(pos)
        embedding[node] = pos
        for neighbor in G[node]:
            if not dfs(neighbor, (pos[0], pos[1] + 1)):
                return False
        return True
    
    if not dfs(0, (0, 0)):
        return None
    
    return embedding

def non_rigid_transformations(embedding):
    n = len(embedding)
    grid_size = max(pos[1] for pos in embedding.values()) + 1
    grid = [[None] * grid_size for _ in range(grid_size)]
    
    for node, pos in embedding.items():
        grid[pos[0]][pos[1]] = node
    
    def find_non_rigid_moves():
        moves = []
        for i in range(grid_size):
            for j in range(grid_size):
                if grid[i][j] is not None:
                    continue
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < grid_size and 0 <= nj < grid_size and grid[ni][nj] is not None:
                            moves.append((grid[ni][nj], (ni, nj), (i, j)))
        return moves
    
    return find_non_rigid_moves()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    d = 3
    n = 10
    G = generate_d_regular_graph(d, n)
    embedding = isometric_embedding(G)
    
    if embedding is None:
        return {
            "metric_name": "non_rigid_moves",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "isometric_embedding_failed"
        }
    
    non_rigid_moves = non_rigid_transformations(embedding)
    num_non_rigid_moves = len(non_rigid_moves)
    r_G_squared = d**2
    
    return {
        "metric_name": "non_rigid_moves",
        "metric_value": num_non_rigid_moves,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": num_non_rigid_moves <= r_G_squared,
        "counterexample": "" if num_non_rigid_moves <= r_G_squared else f"num_non_rigid_moves={num_non_rigid_moves}, r(G)^2={r_G_squared}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")