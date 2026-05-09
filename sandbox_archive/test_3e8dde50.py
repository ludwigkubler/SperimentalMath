# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), 3)]
            clauses.append(clause)
        return clauses
    
    def symmetric_function(clauses):
        f_Φ = {}
        for clause in clauses:
            monomial = tuple(sorted(abs(x) for x in clause))
            if monomial not in f_Φ:
                f_Φ[monomial] = 0
            f_Φ[monomial] += 1
        return f_Φ
    
    def plethysm(f_Φ, λ):
        result = 0
        for monomial, count in f_Φ.items():
            if len(monomial) == sum(λ):
                result += count
        return result
    
    def circuit_size(clauses):
        depth = 1
        for clause in clauses:
            depth = max(depth, max(abs(x) for x in clause))
        return depth
    
    n = random.randint(5, 40)
    Φ = generate_3cnf(n)
    f_Φ = symmetric_function(Φ)
    
    plethysm_values = [plethysm(f_Φ, λ) * circuit_size(Φ) for λ in [[n], [n-1, 1], [n-2, 1]]]
    
    conjecture_holds = all(value <= 2**(0.5 * n) for value in plethysm_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "plethysm_coefficient",
        "metric_value": sum(plethysm_values),
        "instances_tested": len(plethysm_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")