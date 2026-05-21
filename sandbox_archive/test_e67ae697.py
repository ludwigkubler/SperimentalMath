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
    
    def construct_constraint_polynomial(clauses):
        n = len(clauses[0])
        poly = 1
        x = [Fraction(1, 1)] * n
        for clause in clauses:
            linear_form = [random.choice([-1, 1]) for _ in range(n)]
            poly *= (linear_form[0] * x[0] + linear_form[1])
        return poly

    def is_real_stable(poly):
        roots = [complex(root) for root in poly.roots]
        for root in roots:
            if not (root.imag == 0 and root.real >= 0):
                return False
        return True

    def sdp_relaxation(poly, max_iter=100):
        n = len(poly)
        x = [Fraction(1, 1)] * n
        for _ in range(max_iter):
            gradient = [sum(coeff * root ** i for coeff, root in zip(poly, roots)) for i in range(n)]
            step_size = Fraction(1, sum(abs(g) for g in gradient))
            x = [x_i - step_size * grad_i for x_i, grad_i in zip(x, gradient)]
        return max(abs(x_i) for x_i in x)

    n = 40
    clause_density = 1.5
    num_clauses = int(n * clause_density)
    clauses = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(num_clauses)]
    
    poly = construct_constraint_polynomial(clauses)
    if not is_real_stable(poly):
        return {
            "metric_name": "sos_refutation_degree",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    sos_refutation_degree = sdp_relaxation(poly)
    conjecture_holds = sos_refutation_degree <= math.sqrt(n)
    
    return {
        "metric_name": "sos_refutation_degree",
        "metric_value": sos_refutation_degree,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(result['metric_value'] for result in results)/len(results)} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")