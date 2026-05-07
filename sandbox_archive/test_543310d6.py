# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def generate_random_odd_sigma(n):
    sigma = [random.choice([0, 1]) for _ in range(n)]
    if sum(sigma) % 2 == 0:
        sigma[random.randint(0, n-1)] = 1 - sigma[-1]
    return sigma

def is_ramanujanish(G, d, lambda_2_threshold):
    degree_sum = sum(degree for _, degree in G.items())
    if degree_sum != len(G) * d:
        return False
    lambda_2 = max(eigenvalue for eigenvalue in get_eigenvalues(G) if eigenvalue > 0)
    return lambda_2 <= lambda_2_threshold

def generate_random_d_regular_graph(n, d):
    G = {}
    edges = set()
    while len(edges) < n * (d // 2):
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            G[u] = G.get(u, set()) | {v}
            G[v] = G.get(v, set()) | {u}
            edges.add((u, v))
    return G

def get_eigenvalues(G):
    n = len(G)
    A = [[0 for _ in range(n)] for _ in range(n)]
    for u, neighbors in G.items():
        for v in neighbors:
            A[u][v] += 1
            A[v][u] += 1
    return eigenvalues(A)

def eigenvalues(matrix):
    n = len(matrix)
    if n == 0:
        return []
    if n == 1:
        return [matrix[0][0]]
    
    def determinant(submatrix):
        if len(submatrix) == 2:
            return submatrix[0][0] * submatrix[1][1] - submatrix[0][1] * submatrix[1][0]
        det = 0
        for j in range(len(submatrix)):
            det += (-1) ** j * submatrix[0][j] * determinant([row[:j] + row[j+1:] for row in submatrix[1:]])
        return det
    
    def characteristic_polynomial(matrix):
        n = len(matrix)
        if n == 2:
            return [matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0], -(matrix[0][0] + matrix[1][1]), 1]
        else:
            char_poly = []
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
                char_poly.append((-1) ** (n-1-j) * determinant(submatrix))
            return char_poly
    
    def roots(poly):
        if len(poly) == 1:
            return []
        elif len(poly) == 2:
            return [-poly[0] / poly[1]]
        else:
            a, b, c = poly[-3], poly[-2], poly[-1]
            discriminant = b**2 - 4*a*c
            if discriminant < 0:
                real_part = -b / (2*a)
                imaginary_part = math.sqrt(-discriminant) / (2*a)
                return [real_part + imaginary_part * 1j, real_part - imaginary_part * 1j]
            elif discriminant == 0:
                return [-b / (2*a)]
            else:
                sqrt_discriminant = math.sqrt(discriminant)
                return [(-b + sqrt_discriminant) / (2*a), (-b - sqrt_discriminant) / (2*a)]
    
    char_poly = characteristic_polynomial(matrix)
    return roots(char_poly)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 12, 16, 20, 24, 28, 32, 36, 40]
    d = 3
    lambda_2_threshold = 2 * math.sqrt(d - 1) + 0.4
    alpha = 1 / 8
    
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        ramanujanish_graphs = [generate_random_d_regular_graph(n, d) for _ in range(30)]
        ramanujanish_graphs = [G for G in ramanujanish_graphs if is_ramanujanish(G, d, lambda_2_threshold)]
        
        for G in ramanujanish_graphs:
            sigma = generate_random_odd_sigma(n)
            P_Gsigma = [[0] * n for _ in range(n)]
            for e, f in combinations(range(n), 2):
                if e in G and f in G[e]:
                    c_ef_sigma = sum(1 for v in G[e] & G[f] if sigma[v] == 1)
                    P_Gsigma[e][f] = 2 * c_ef_sigma
            H = [[0] * n for _ in range(n)]
            for e, f in combinations(range(n), 2):
                H[e][f] = P_Gsigma[e][f]
                H[f][e] = P_Gsigma[e][f]
            
            eigenvalues_H = get_eigenvalues(H)
            delta = sum(1 for eigenvalue in eigenvalues_H if eigenvalue > 0) - 1
            metric_values.append(delta)
            instances_tested += 1
            
            if delta < n / (8 * d**2):
                conjecture_holds = False
                counterexample = f"n={n}, δ={delta} < {n / (8 * d**2)}"
            
            w_TGsigma = 0
            for width in range(2, math.ceil(math.log2(n)) + 1):
                if is_refutation(G, sigma, width):
                    w_TGsigma = width
                    break
            
            metric_values.append(w_TGsigma)
            instances_tested += 1
            
            if w_TGsigma < 2 + 2 * delta:
                conjecture_holds = False
                counterexample = f"n={n}, w={w_TGsigma} < {2 + 2 * delta}"
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = instances_tested // 30
    
    return {
        "metric_name": "Lorentzian defect and resolution width",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def is_refutation(G, sigma, width):
    stack = [(0, 0)]
    visited = set()
    
    while stack:
        node, level = stack.pop()
        if level >= width or node in visited:
            continue
        visited.add(node)
        
        for neighbor in G[node]:
            if neighbor not in visited:
                stack.append((neighbor, level + 1))
    
    return len(visited) == len(G)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")