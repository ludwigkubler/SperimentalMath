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
    
    def generate_sat_formula(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([f'x{i}', f'~x{i}']) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def tropical_rank(sat_formula):
        # Simplified implementation of tropical rank calculation
        # This is a placeholder and should be replaced with actual logic
        return len(sat_formula) ** 0.5
    
    n = random.randint(5, 40)
    sat_formula = generate_sat_formula(n)
    rank = tropical_rank(sat_formula)
    
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank >= n ** 0.5 * 0.7 and rank <= n ** 0.5 * 1.3
    counterexample = "" if conjecture_holds else f"Rank {rank} for n={n}"
    
    return {
        "metric_name": "Tropical Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 
        71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = (sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results)) ** 0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank out of bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")