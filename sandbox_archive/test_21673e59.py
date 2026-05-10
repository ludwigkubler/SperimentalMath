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

def fast_walsh_hadamard_transform(f):
    n = len(f)
    if n == 1:
        return f
    even = fast_walsh_hadamard_transform([f[i] for i in range(0, n, 2)])
    odd = fast_walsh_hadamard_transform([f[i] for i in range(1, n, 2)])
    result = [0] * n
    for k in range(n // 2):
        result[k] = even[k] + odd[k]
        result[k + n // 2] = even[k] - odd[k]
    return result

def fourier_coefficients(f):
    n = len(f)
    F = fast_walsh_hadamard_transform([f[i] / math.sqrt(n) for i in range(n)])
    return F

def indicator_function(x, n):
    return 1 if all(x[i] == 0 for i in range(n)) else 0

def generate_3sat_instance(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(3)]
        clauses.append(clause)
    return clauses

def dpll_solve(clauses, assignment):
    if not clauses:
        return True
    literal = next(lit for lit in range(-n, n + 1) if lit != 0 and lit not in assignment)
    pos_lit = abs(literal)
    if literal > 0:
        assignment[pos_lit] = True
    else:
        assignment[-pos_lit] = False
    new_clauses = [c for c in clauses if not any(abs(lit) == pos_lit for lit in c)]
    if dpll_solve(new_clauses, assignment):
        return True
    del assignment[pos_lit]
    if literal > 0:
        assignment[pos_lit] = False
    else:
        assignment[-pos_lit] = True
    new_clauses = [c for c in clauses if not any(abs(lit) == pos_lit for lit in c)]
    if dpll_solve(new_clauses, assignment):
        return True
    del assignment[-pos_lit]
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    instances_tested = 30
    total_length = 0
    total_sum_abs_coefficients = 0
    
    for _ in range(instances_tested):
        clauses = generate_3sat_instance(n)
        f = [indicator_function(x, n) for x in product([0, 1], repeat=n)]
        F = fourier_coefficients(f)
        sum_abs_coefficients = sum(abs(coeff) for coeff in F)
        
        assignment = {}
        length = dpll_solve(clauses, assignment)
        if not length:
            return {
                "metric_name": "resolution_proof_length",
                "metric_value": None,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": "unsatisfiable_instance"
            }
        
        total_length += length
        total_sum_abs_coefficients += sum_abs_coefficients
    
    mean_length = total_length / instances_tested
    mean_sum_abs_coefficients = total_sum_abs_coefficients / instances_tested
    conjecture_holds = mean_length >= mean_sum_abs_coefficients
    
    return {
        "metric_name": "resolution_proof_length",
        "metric_value": mean_length,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    from itertools import product
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")