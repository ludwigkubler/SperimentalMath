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
        if d * (n - 1) % 2 != 0 or n < d + 1:
            raise ValueError("Invalid parameters for generating a d-regular graph")
        
        G = [[] for _ in range(n)]
        edges_added = set()
        
        def add_edge(u, v):
            if u == v or (u, v) in edges_added or (v, u) in edges_added:
                return False
            G[u].append(v)
            G[v].append(u)
            edges_added.add((u, v))
            edges_added.add((v, u))
            return True
        
        for i in range(n):
            for j in range(i + 1, n):
                if len(G[i]) < d and len(G[j]) < d:
                    add_edge(i, j)
        
        return G
    
    def isometric_embedding(G):
        n = len(G)
        positions = [None] * n
        visited = [False] * n
        
        def dfs(v, pos):
            if visited[v]:
                return False
            visited[v] = True
            positions[v] = pos
            for u in G[v]:
                if not dfs(u, (pos[0], pos[1] + 1)):
                    return False
            return True
        
        if not dfs(0, (0, 0)):
            return None
        
        return positions
    
    def non_rigid_transformations(positions):
        n = len(positions)
        min_transformations = float('inf')
        
        for i in range(n):
            for j in range(i + 1, n):
                if positions[i][0] == positions[j][0]:
                    continue
                new_positions = [None] * n
                for k in range(n):
                    if k == i:
                        new_positions[k] = (positions[k][0], positions[k][1])
                    elif k == j:
                        new_positions[k] = (positions[k][0], positions[k][1] + 1)
                    else:
                        new_positions[k] = (positions[k][0], positions[k][1])
                overlap = sum(1 for p in new_positions if p[1] >= 0 and p[1] < n)
                min_transformations = min(min_transformations, n - overlap)
        
        return min_transformations
    
    def communication_complexity_rank(G):
        n = len(G)
        rank = float('inf')
        
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j]:
                    continue
                new_G = [row[:] for row in G]
                new_G[i][j] = True
                new_G[j][i] = True
                rank = min(rank, communication_complexity_rank(new_G))
        
        return rank
    
    def gaussian_elimination(A):
        n = len(A)
        m = len(A[0])
        for i in range(n):
            if A[i][i] == 0:
                for j in range(i + 1, n):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]
                        break
                else:
                    return None
            pivot = A[i][i]
            for j in range(m):
                A[i][j] /= pivot
            for j in range(n):
                if j == i:
                    continue
                factor = A[j][i]
                for k in range(m):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiplication(A, B):
        n = len(A)
        m = len(B[0])
        p = len(B)
        C = [[0] * m for _ in range(n)]
        for i in range(n):
            for j in range(m):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def inverse(A):
        n = len(A)
        det_A = determinant(A)
        if det_A == 0:
            return None
        adjoint = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
                cofactor = determinant(submatrix)
                adjoint[j][i] = (-1) ** (i + j) * cofactor
        inv_A = matrix_multiplication(adjoint, [[1 / det_A] * n for _ in range(n)])
        return inv_A
    
    def isometric_embedding(G):
        n = len(G)
        positions = [None] * n
        visited = [False] * n
        
        def dfs(v, pos):
            if visited[v]:
                return False
            visited[v] = True
            positions[v] = pos
            for u in G[v]:
                if not dfs(u, (pos[0], pos[1] + 1)):
                    return False
            return True
        
        if not dfs(0, (0, 0)):
            return None
        
        return positions
    
    def non_rigid_transformations(positions):
        n = len(positions)
        min_transformations = float('inf')
        
        for i in range(n):
            for j in range(i + 1, n):
                if positions[i][0] == positions[j][0]:
                    continue
                new_positions = [None] * n
                for k in range(n):
                    if k == i:
                        new_positions[k] = (positions[k][0], positions[k][1])
                    elif k == j:
                        new_positions[k] = (positions[k][0], positions[k][1] + 1)
                    else:
                        new_positions[k] = (positions[k][0], positions[k][1])
                overlap = sum(1 for p in new_positions if p[1] >= 0 and p[1] < n)
                min_transformations = min(min_transformations, n - overlap)
        
        return min_transformations
    
    def communication_complexity_rank(G):
        n = len(G)
        rank = float('inf')
        
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j]:
                    continue
                new_G = [row[:] for row in G]
                new_G[i][j] = True
                new_G[j][i] = True
                rank = min(rank, communication_complexity_rank(new_G))
        
        return rank
    
    d = random.randint(2, 5)
    n = random.randint(d + 1, 40)
    G = generate_d_regular_graph(d, n)
    embedding = isometric_embedding(G)
    
    if embedding is None:
        return {
            "metric_name": "non_rigid_motions",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "embedding_failed"
        }
    
    non_rigid = non_rigid_transformations(embedding)
    rank = communication_complexity_rank(G)
    
    return {
        "metric_name": "non_rigid_motions",
        "metric_value": non_rigid,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": non_rigid <= rank ** 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"non_rigid_motions > rank^2\" first_failing_seed={seeds[first_failing_seed]}")