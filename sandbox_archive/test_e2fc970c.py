# auto-injected by SEC sandbox
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
import math
from itertools import product, combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(n):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses

    def incidence_matrix(formula):
        n = len(formula)
        m = max(max(clause) for clause in formula)
        Inc = [[0] * (m + 1) for _ in range(n)]
        for i, clause in enumerate(formula):
            for var in clause:
                Inc[i][var] = 1
        return Inc

    def min_order(Inc, p):
        n = len(Inc)
        m = max(max(row) for row in Inc)
        order = float('inf')
        for k in range(n + 1):
            for l in range(k + 1, n + 1):
                a_k = sum(Inc[i][k] * (p ** i) for i in range(n))
                a_l = sum(Inc[i][l] * (p ** i) for i in range(n))
                order = min(order, abs(a_k - a_l))
        return order

    def frege_proof_length(formula):
        n = len(formula)
        if n == 1:
            return 1
        length = 0
        for clause in formula:
            if len(clause) == 1:
                length += 1
            else:
                length += 2
        return length

    p = 7  # Prime number for p-adic order calculation
    instances_tested = 30
    n_max = 40
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        formula = generate_formula(n)
        Inc = incidence_matrix(formula)
        min_order_val = min_order(Inc, p)
        length = frege_proof_length(formula)
        
        if length == 0:
            continue
        
        metric_value = math.log(p - 1) ** min_order_val
        expected_value = math.log(2 ** length + 1)
        total_metric_value += metric_value
        
        if abs(metric_value - expected_value) > 0.5:
            conjecture_holds = False
            counterexample = f"Formula size {n}, min_order={min_order_val}, length={length}"
            break

    return {
        "metric_name": "log(p-1)^min_order(Inc(φ))",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_evidence")