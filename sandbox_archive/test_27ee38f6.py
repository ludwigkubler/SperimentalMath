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
    n = random.randint(10, 40)
    G = generate_random_graph(n)
    
    chi_t_G = tropical_euler_characteristic(G)
    ac0_depth_G = ac0_parity_depth(G)
    
    metric_value = chi_t_G
    conjecture_holds = chi_t_G >= c * math.log(n) if 'c' in locals() else False
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    
    return {
        "metric_name": "tropical_euler_characteristic",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def generate_random_graph(n: int) -> list:
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    return G

def tropical_euler_characteristic(G: list) -> float:
    n = len(G)
    det_tropical = max_entrywise_nonnegative_real_numbers(tropical_determinant(G))
    return det_tropical

def tropical_determinant(G: list) -> float:
    n = len(G)
    if n == 1:
        return G[0][0]
    det = -float('inf')
    for i in range(n):
        submatrix = [row[:i] + row[i+1:] for row in G[1:]]
        det = max(det, G[0][i] + tropical_determinant(submatrix))
    return det

def max_entrywise_nonnegative_real_numbers(matrix: list) -> float:
    n = len(matrix)
    result = 0
    for i in range(n):
        for j in range(n):
            if matrix[i][j] > result:
                result = matrix[i][j]
    return result

def ac0_parity_depth(G: list) -> int:
    n = len(G)
    # Placeholder function, actual implementation required
    return 1  # Replace with actual AC0 parity depth computation

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")