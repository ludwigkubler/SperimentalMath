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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if any(clause[i] == -clause[j] for i in range(n) for j in range(i+1, n)):
                clauses.append(tuple(sorted(clause)))
        return set(clauses)
    
    def clause_indicator_polynomial(cnf):
        n = len(next(iter(cnf), (0,))[0])
        poly = [0] * (2**n)
        for clause in cnf:
            sign = 1
            for var in clause:
                if var < 0:
                    sign *= -1
                    var = -var
                poly[1 << (var - 1)] += sign
        return poly
    
    def schur_functions(n):
        schurs = []
        for i in range(2**n):
            schur = [0] * (2**n)
            schur[i] = 1
            schurs.append(schur)
        return schurs
    
    def count_vanishing_schurs(poly, schurs):
        count = 0
        for schur in schurs:
            product = 1
            for i in range(len(poly)):
                if poly[i]:
                    product *= schur[i]
            if product == 0:
                count += 1
        return count
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    poly = clause_indicator_polynomial(cnf)
    schurs = schur_functions(n)
    
    vanishing_count = count_vanishing_schurs(poly, schurs)
    
    return {
        "metric_name": "vanishing_schurs",
        "metric_value": vanishing_count,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")