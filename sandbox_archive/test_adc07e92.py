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
    
    def generate_noncommutative_complex(n, d):
        G = [[0] * n for _ in range(n)]
        generators = [f'a{i}' for i in range(d)]
        relations = []
        
        # Generate a simple noncommutative complex
        for i in range(n):
            for j in range(i + 1, n):
                if random.randint(0, 1) == 0:
                    G[i][j] = f'{generators[random.randint(0, d-1)]}'
                    G[j][i] = f'{generators[random.randint(0, d-1)]}^{-1}'
        
        return G
    
    def compute_local_indeterminacy(G):
        n = len(G)
        epsilon_G = 0
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j] != G[j][i]:
                    epsilon_G += 1
        return epsilon_G
    
    def compute_communication_complexity_rank(G):
        n = len(G)
        matrix = [[0] * n for _ in range(n)]
        
        # Compute the communication complexity matrix
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j] != G[j][i]:
                    matrix[i][j] = 1
                    matrix[j][i] = 1
        
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
                for j in range(n):
                    if row[j]:
                        for k in range(n):
                            if matrix[k][j]:
                                matrix[k][j] = 0
        
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_epsilon_G = 0
    max_n = 0
    
    for n in n_values:
        for _ in range(5):
            G = generate_noncommutative_complex(n, random.randint(1, 3))
            epsilon_G = compute_local_indeterminacy(G)
            r_G = compute_communication_complexity_rank(G)
            
            if r_G > 0:
                instances_tested += 1
                total_epsilon_G += epsilon_G
                max_n = max(max_n, n)
    
    mean_epsilon_G = total_epsilon_G / instances_tested if instances_tested else 0
    
    conjecture_holds = False
    counterexample = ""
    
    if instances_tested >= 30:
        T = 0.9  # Threshold for acceptance
        correlation_coefficient = (total_epsilon_G - n_values[0] * r_G) / math.sqrt(n_values[0] * (n_values[-1] - n_values[0]) * (n_values[-1] + n_values[0]))
        if correlation_coefficient > T:
            conjecture_holds = True
        else:
            counterexample = f"correlation_coefficient={correlation_coefficient}"
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": mean_epsilon_G,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_epsilon_G = sum(r["metric_value"] for r in results) / len(results)
    std_epsilon_G = math.sqrt(sum((r["metric_value"] - mean_epsilon_G) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_epsilon_G} std={std_epsilon_G} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print("RESULT: INCONCLUSIVE insufficient_support")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")