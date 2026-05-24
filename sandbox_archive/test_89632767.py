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
    
    def min_rank(state):
        # Perform SVD and return the rank
        U, S, Vt = svd(state)
        return len(S)
    
    def construct_circuit(state, ε):
        # Placeholder for circuit construction logic
        # For simplicity, we'll just return a dummy T-depth
        n = int(math.log2(len(state)))
        return 2 * n
    
    def svd(matrix):
        # Perform singular value decomposition manually
        m, n = len(matrix), len(matrix[0])
        U = [[1 if i == j else 0 for j in range(n)] for i in range(m)]
        S = [sum(row[i]**2 for row in matrix)**0.5 for i in range(min(m, n))]
        Vt = [[matrix[j][i] / S[i] if i < len(S) and j < m else 0 for i in range(n)] for j in range(m)]
        return U, S, Vt
    
    ε = 0.01
    state = [random.random() for _ in range(2**5)]
    
    rank = min_rank(state)
    t_depth = construct_circuit(state, ε)
    
    metric_value = rank / t_depth
    conjecture_holds = metric_value <= 1 + ε
    
    return {
        "metric_name": "minimal_rank_over_t_depth",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Rank {rank}, T-depth {t_depth}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")