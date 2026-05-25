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

def negation_cayley_representation(k_cnf):
    n = len(k_cnf)
    rep = [0] * (2 * n + 1)
    for clause in k_cnf:
        for lit in clause:
            if abs(lit) > n:
                return None
            rep[-lit - 1] -= 1
            rep[lit - 1] += 1
    return rep

def minimal_rank(rep):
    max_val = max(abs(x) for x in rep)
    min_val = min(abs(x) for x in rep if x != 0)
    return max_val / min_val

def monotone_k_clique_circuit_size(n, k):
    # Simplified approximation based on known results
    return 2 ** (n ** (1/2 - k))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    k_cnf = []
    for _ in range(n):
        clause = [random.choice([-i, i]) for i in range(1, n + 1)]
        k_cnf.append(clause)
    
    rep = negation_cayley_representation(k_cnf)
    if rep is None:
        return {
            "metric_name": "minimal_rank",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    rank = minimal_rank(rep)
    expected_size = monotone_k_clique_circuit_size(n, k)
    tolerance = 0.1 * expected_size
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": abs(rank - expected_size) <= tolerance and rank <= expected_size,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")