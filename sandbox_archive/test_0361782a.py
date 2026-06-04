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
    
    def generate_formula(n, m):
        formula = []
        for _ in range(m):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            formula.append(clause)
        return formula
    
    def hodge_norm(formula):
        n = len(formula[0])
        m = len(formula)
        norm = 0
        for clause in formula:
            norm += sum(abs(lit) for lit in clause) ** 2
        norm /= (n * m)
        return math.sqrt(norm)
    
    def mean(lst):
        return sum(lst) / len(lst)
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_hodge_norm = 0.0
    max_n = 0
    
    for n in n_values:
        for _ in range(5):
            formula = generate_formula(n, m)
            hodge = hodge_norm(formula)
            total_hodge_norm += hodge
            instances_tested += 1
            max_n = max(max_n, n)
    
    mean_hodge_norm = total_hodge_norm / instances_tested
    
    conjecture_holds = False
    counterexample = ""
    
    if abs(mean_hodge_norm - m ** (3/2) * n ** (1/4)) <= 0.1 * m ** (3/2) * n ** (1/4):
        conjecture_holds = True
    
    return {
        "metric_name": "Hodge Norm",
        "metric_value": mean_hodge_norm,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")