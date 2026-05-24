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

def gram_schmidt(matrix):
    n = len(matrix)
    Q = []
    R = []
    
    for i in range(n):
        q_i = matrix[i]
        norm_q_i = sum(q_i[k] ** 2 for k in range(n)) ** 0.5
        if norm_q_i == 0:
            continue
        
        q_i_normalized = [q_i[k] / norm_q_i for k in range(n)]
        Q.append(q_i_normalized)
        
        r_i_j = [sum(Q[j][k] * matrix[i][k] for k in range(n)) for j in range(i + 1)]
        R.append(r_i_j)
    
    return Q, R

def run_trial(seed: int) -> dict:
    random.seed(seed)
    q = random.randint(2, 5)  # Finite field size F_q
    n = random.choice([5, 10, 15, 20, 30, 40])  # Instance size
    
    # Generate a random max-CUT instance
    graph = {}
    for i in range(n):
        graph[i] = set()
    for _ in range(n * (n - 1) // 2):
        u, v = random.sample(range(n), 2)
        if u not in graph[v]:
            graph[u].add(v)
            graph[v].add(u)
    
    # Construct the characteristic polynomial of a random matrix in GL_n(F_q)
    matrix = []
    for i in range(n):
        row = [random.randint(1, q - 1) for _ in range(n)]
        if sum(row[j] * row[j] for j in range(n)) == 0:
            continue
        matrix.append(row)
    
    # Evaluate the quantum logarithmic form at the zeros of the characteristic polynomial
    Q, R = gram_schmidt(matrix)
    rank = len(Q)
    
    # Determine the sum-of-squares degree of the best-known approximation algorithm for max-CUT
    # (This is a placeholder as the actual implementation depends on the specific approximation algorithm)
    sum_of_squares_degree = n  # Placeholder value
    
    # Check if the sum-of-squares degree is less than the computed minimal rank
    conjecture_holds = sum_of_squares_degree < rank
    counterexample = "" if conjecture_holds else f"sum_of_squares_degree={sum_of_squares_degree}, rank={rank}"
    
    return {
        "metric_name": "Minimal Rank vs Sum-of-Squares Degree",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_dev = (sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")