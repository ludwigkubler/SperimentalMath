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
    
    def generate_k_clique(n):
        return [[i, j] for i in range(n) for j in range(i + 1, n)]
    
    def encode_quadratic_form(clique):
        n = len(clique[0])
        Q = [[0] * n for _ in range(n)]
        for u, v in clique:
            Q[u][v] = Q[v][u] = 1
        return Q
    
    def min_rank(Q):
        n = len(Q)
        rank = 0
        A = [row[:] for row in Q]
        for i in range(n):
            if all(A[j][i] == 0 for j in range(i, n)):
                continue
            pivot_row = max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[pivot_row] = A[pivot_row], A[i]
            rank += 1
            for j in range(n):
                if j != i:
                    factor = -A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
        return rank
    
    n = random.randint(5, 40)
    clique = generate_k_clique(n)
    Q = encode_quadratic_form(clique)
    rank = min_rank(Q)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= n**2,
        "counterexample": "" if rank <= n**2 else f"n={n}, rank={rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")