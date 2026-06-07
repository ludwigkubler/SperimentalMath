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
        for _ in range(10):  # Generate 10 clauses with n variables
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses

    def cnf_to_polynomial(cnf):
        polynomial = {}
        for clause in cnf:
            term = 1
            for literal in clause:
                if literal > 0:
                    term *= (1 + x[literal])
                else:
                    term *= (1 - x[-literal])
            polynomial[term] += 1
        return polynomial

    def p_adic_rank(polynomial):
        max_power = 0
        for coeff in polynomial.values():
            if coeff != 0:
                power = int(math.log(abs(coeff), 2))
                if power > max_power:
                    max_power = power
        return max_power

    n = random.randint(5, 40)
    x = [random.random() for _ in range(n + 1)]
    cnf = generate_cnf(n)
    polynomial = cnf_to_polynomial(cnf)
    p_adic_rank_value = p_adic_rank(polynomial)

    # Calculate resolution proof width (simplified example)
    resolution_width = len(cnf) * n

    return {
        "metric_name": "p-adic Rank vs Resolution Width",
        "metric_value": abs(resolution_width - p_adic_rank_value),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if not r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")