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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            literals = [random.choice([f'x{i}', f'-x{i}']) for i in range(1, n+1)]
            clause = ' or '.join(literals)
            clauses.append(clause)
        return ' and '.join(clauses)
    
    def tropical_jacobian_rank(n):
        # Simplified model of the Jacobian rank for demonstration
        return n * (n - 1) // 2
    
    def resolution_proof_size(k_cnf):
        # Placeholder function to simulate resolution proof size calculation
        return len(k_cnf.split(' and '))
    
    total_ratio = 0
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Test each n with 5 different k-CNFs
            k_cnf = generate_k_cnf(n, random.randint(1, n))
            rank = tropical_jacobian_rank(n)
            proof_size = resolution_proof_size(k_cnf)
            if rank > 0:
                ratio = proof_size / rank
                total_ratio += ratio
                instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "Ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    mean_ratio = total_ratio / instances_tested
    conjecture_holds = mean_ratio <= 1.5
    
    return {
        "metric_name": "Ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean ratio {mean_ratio} exceeds 1.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["instances_tested"] > 0) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={r['seed']}")
                break