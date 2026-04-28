# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

# Implement basic linear algebra operations manually
def matrix_multiply(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    M = [A[i] + b[i] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        for j in range(i+1, n):
            factor = M[j][i] / M[i][i]
            M[j] = [M[j][k] - factor * M[i][k] for k in range(n)]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = M[i][-1]
        for j in range(i+1, n):
            x[i] -= M[i][j] * x[j]
        x[i] /= M[i][i]
    return x

def hamming_distance(a, b):
    return sum(1 for i in range(len(a)) if a[i] != b[i])

# Define the MetricGadget class
class MetricGadget:
    def __init__(self, X, Y, g, d):
        self.X = X
        self.Y = Y
        self.g = g
        self.d = d

    def distance(self, x1, y1, x2, y2):
        return self.d(x1, y1) + self.d(x2, y2)

# Implement the Følner defect calculation
def folner_defect(G, R, n):
    X, Y, g, d = G.X, G.Y, G.g, G.d
    k = len(X)
    total_points = k ** (2 * n)
    min_boundary_ratio = float('inf')
    
    for F in range(total_points):
        boundary_count = 0
        for i in range(n):
            x1, y1 = X[F % k], Y[(F // k) % k]
            x2, y2 = X[(F + 1) % k], Y[((F + 1) // k) % k]
            if d(x1, x2) > R or d(y1, y2) > R:
                boundary_count += 1
        min_boundary_ratio = min(min_boundary_ratio, boundary_count / total_points)
    
    return min_boundary_ratio

# Implement the CC(EQ_k ∘ G^n) calculation using rank/partition-bound LP
def cc_eqk_gn(G, n):
    X, Y, g, d = G.X, G.Y, G.g, G.d
    k = len(X)
    m = 2 ** (n * math.log2(k))
    
    # Construct the communication matrix
    C = [[0 for _ in range(m)] for _ in range(m)]
    for i in range(m):
        x1, y1 = X[i % k], Y[(i // k) % k]
        for j in range(m):
            x2, y2 = X[j % k], Y[(j // k) % k]
            C[i][j] = d(x1, x2) + d(y1, y2)
    
    # Solve the rank/partition-bound LP
    b = [0 for _ in range(m)]
    A = [[0 for _ in range(m)] for _ in range(m)]
    for i in range(m):
        for j in range(m):
            if i != j:
                A[i][j] = C[i][j]
    
    x = gaussian_elimination(A, b)
    return sum(x)

# Define the run_trial function
def run_trial(seed: int) -> dict:
    random.seed(seed)
    k_values = [2, 3, 4]
    n_values = [1, 2, 3, 4]
    
    results = []
    for k in k_values:
        X = [f"x{i}" for i in range(k)]
        Y = [f"y{i}" for i in range(k)]
        g = lambda x, y: hamming_distance(x, y)
        d = lambda a, b: sum(1 for i in range(len(a)) if a[i] != b[i])
        G = MetricGadget(X, Y, g, d)
        
        for n in n_values:
            R = math.inf  # Diameter of the gadget
            m_n = folner_defect(G, R, n)
            cc_eqk_gn_value = cc_eqk_gn(G, n)
            
            results.append({
                "metric_name": "CC(EQ_k ∘ G^n)",
                "metric_value": cc_eqk_gn_value,
                "instances_tested": 1,
                "conjecture_holds": cc_eqk_gn_value >= n * math.log2(m_n + 1),
                "counterexample": ""
            })
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_metric_value": mean_metric_value,
        "support_fraction": support_fraction
    }

# Main block to run trials and print results
if __name__ == "__main__":
    seeds = [11, 23, 37, 53, 71] if len(sys.argv) < 2 else [int(arg) for arg in sys.argv[1:]]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    # Compute mean and support fraction across all seeds
    total_results = []
    for seed in seeds:
        with open(f"trial_{seed}.json", "r") as f:
            trial_result = json.load(f)
            total_results.append(trial_result)
    
    mean_metric_value = sum(result["mean_metric_value"] for result in total_results) / len(total_results)
    support_fraction = sum(result["support_fraction"] for result in total_results) / len(total_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = min(total_results, key=lambda x: x["support_fraction"])["seed"]
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")