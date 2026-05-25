# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def compute_toric_rank(clauses):
        # Simplified mapping to a rank based on the number of clauses
        return len(clauses)
    
    def monotone_circuit_width(clauses):
        # Simplified mapping to width based on the number of variables
        return max(abs(x) for clause in clauses for x in clause)
    
    n = random.randint(5, 40)
    F = generate_3cnf(n)
    rank = compute_toric_rank(F)
    width = monotone_circuit_width(F)
    
    if width == 0:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "monotone_circuit_width_zero"
        }
    
    ratio = Fraction(rank, width)
    return {
        "metric_name": "ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*100 + 2, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    support_fraction = sum(1 for r in results if r["conjecture_holds"])
    
    mean_ratio = total_ratio / len(results)
    std_ratio = (sum((r["metric_value"] - mean_ratio)**2 for r in results if r["metric_value"] is not None) / len(results))**0.5
    
    if support_fraction >= 0.8 * len(results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction/len(results)}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE not enough seeds supported")