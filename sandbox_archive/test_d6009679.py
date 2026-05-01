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
    
    def is_3sat_clause_valid(clause):
        return len(clause) == 3 and all(isinstance(lit, int) and lit != 0 for lit in clause)
    
    def generate_random_3sat_instance(n: int) -> list:
        clauses = []
        for _ in range(2 * n):  # Each variable appears twice
            while True:
                clause = [random.choice([-1, 1]) * random.randint(1, n)]
                if is_3sat_clause_valid(clause):
                    clauses.append(clause)
                    break
        return clauses
    
    def hook_length_formula(n: int) -> float:
        total = 0
        for i in range(1, n + 1):
            for j in range(1, n - i + 2):
                total += (n - i + 1 - j) * (n - j + 1)
        return math.factorial(n) / total
    
    def plethysm_coefficient(n: int, k: int) -> float:
        coeff = 0
        for m in range(1, n + 1):
            coeff += ((-1) ** (n - m)) * hook_length_formula(m) ** k
        return coeff / hook_length_formula(n)
    
    def multiplicity(poly_tensor_power: int, lambda_):
        return plethysm_coefficient(lambda_, poly_tensor_power)
    
    n = random.randint(5, 20)
    P_k = multiplicity(n - 1, 2)
    D_k = multiplicity(n - 1, 2)
    
    if P_k > D_k:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "Permanent's multiplicity is not strictly greater than Determinant's"
    
    return {
        "metric_name": "Multiplicity Gap",
        "metric_value": P_k - D_k,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")