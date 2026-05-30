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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_k_cnf(n: int, k: int):
        clauses = []
        for _ in range(k):
            clause = random.sample(range(1, n+1), 2)
            clauses.append(clause)
        return clauses
    
    def hodge_index(n: int) -> float:
        # Simplified heuristic for Hodge index
        return math.log2(n)
    
    def resolution_proof_size(n: int) -> float:
        # Simplified heuristic for resolution proof size
        return math.log2(n)
    
    n = random.choice([10, 20, 40])
    k = n // 2
    if not is_prime(n):
        return {
            "metric_name": "hodge_index",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "n_not_prime"
        }
    
    cnf = generate_k_cnf(n, k)
    p = random.randint(2, min(100, n))
    h_C = hodge_index(n)
    t_F = resolution_proof_size(n)
    
    return {
        "metric_name": "hodge_index",
        "metric_value": h_C,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if h_C <= k / (p ** n) else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" not in res or res["conjecture_holds"] for res in results):
        RESULT = "SUPPORTED"
    elif any(res["counterexample"] != "" for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if res["counterexample"] != "")
        RESULT = f"FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}"
    else:
        mean_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
        std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results if res["metric_value"] is not None) / len(results))
        support_fraction = sum(1 for res in results if "conjecture_holds" in res and res["conjecture_holds"]) / len(results)
        RESULT = f"SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}"
    
    print(RESULT)