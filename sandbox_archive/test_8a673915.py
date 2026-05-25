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
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    def tropicalized_rank(matrix):
        n = len(matrix)
        for i in range(n):
            matrix[i][i] -= 1
        for k in range(n):
            for i in range(n):
                if i == k:
                    continue
                for j in range(n):
                    if j == k:
                        continue
                    matrix[j][k] = max(matrix[j][k], matrix[j][i] + matrix[k][j])
        rank = 0
        for row in matrix:
            if any(x != float('-inf') for x in row):
                rank += 1
        return rank
    
    def quantum_circuit_depth(N):
        return int(2 * log2(N) - 1)
    
    N = random.randint(5, 40)
    state = [random.choice([0, 1]) for _ in range(2**N)]
    matrix = [[float('-inf')] * (2**N) for _ in range(2**N)]
    for i in range(len(state)):
        matrix[i][i] = state[i]
    
    rank = tropicalized_rank(matrix)
    depth = quantum_circuit_depth(N)
    
    if rank < 3:
        return {
            "metric_name": "minimal_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "minimal_rank_less_than_3"
        }
    
    C = 2
    if depth <= 2 * log2(N) - 1 and rank <= C * log2(rank):
        conjecture_holds = True
    else:
        conjecture_holds = False
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        from sympy import primerange
        seeds = list(primerange(2, 100))[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"minimal_rank_less_than_3\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_evidence")