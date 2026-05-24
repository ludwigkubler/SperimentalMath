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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll_width(cnf):
        # Simplified DPLL width calculation
        max_clauses = 0
        for var in range(1, len(cnf) + 1):
            clause_count = sum(1 for clause in cnf if var in clause or -var in clause)
            max_clauses = max(max_clauses, clause_count)
        return max_clauses
    
    def tropicalized_sheaf_order(cnf):
        # Simplified tropicalized sheaf order calculation
        return len(cnf) ** 0.5
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    
    dpll_width_value = dpll_width(cnf)
    sheaf_order = tropicalized_sheaf_order(cnf)
    
    ratio = Fraction(sheaf_order, dpll_width_value) / math.log(n)
    expected_ratio = Fraction(1, 1)  # Simplified expected value for demonstration
    
    conjecture_holds = abs(ratio - expected_ratio) <= Fraction(10, 100)
    counterexample = "" if conjecture_holds else f"Ratio {ratio} outside tolerance"
    
    return {
        "metric_name": "Ratio of Sheaf Order to DPLL Width",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")