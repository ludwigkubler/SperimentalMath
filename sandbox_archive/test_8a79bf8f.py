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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def construct_quandle_representation(f):
        n = int(math.log2(len(f)))
        Q = [[f[i]] + [f[i] ^ f[j] for j in range(i+1, len(f))] for i in range(len(f))]
        return Q
    
    def min_rank_trop(Q):
        m, n = len(Q), len(Q[0])
        rank = 0
        for i in range(m):
            if all(Q[i][j] == 0 for j in range(n)):
                continue
            pivot_col = next(j for j in range(n) if Q[i][j] != 0)
            for j in range(i+1, m):
                factor = Q[j][pivot_col] / Q[i][pivot_col]
                for k in range(n):
                    Q[j][k] -= factor * Q[i][k]
            rank += 1
        return rank
    
    def sum_of_squares_circuit_size(Q):
        n = len(Q[0])
        size = 0
        for i in range(len(Q)):
            if all(Q[i][j] == 0 for j in range(n)):
                continue
            pivot_col = next(j for j in range(n) if Q[i][j] != 0)
            for j in range(i+1, len(Q)):
                factor = Q[j][pivot_col] / Q[i][pivot_col]
                size += 2
        return size
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        Q = construct_quandle_representation(f)
        rank_trop = min_rank_trop(Q)
        size_circuit = sum_of_squares_circuit_size(Q)
        
        if rank_trop >= n**2 and size_circuit >= 2**n:
            results.append((True, f"n={n}, rank_trop={rank_trop}, size_circuit={size_circuit}"))
        else:
            results.append((False, f"n={n}, rank_trop={rank_trop}, size_circuit={size_circuit}"))
    
    conjecture_holds = all(result[0] for result in results)
    counterexample = next(result[1] for result in results if not result[0]) if not conjecture_holds else ""
    
    return {
        "metric_name": "minRank_trop vs size(Q_sum_of_squares)",
        "metric_value": sum(1 for result in results if result[0]),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")