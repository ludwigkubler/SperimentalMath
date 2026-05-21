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
    
    def compute_clause_indicator_poly(cnf):
        n = len(cnf[0])
        x = [Fraction(1, 2)] * (n + 1)
        term = Fraction(1, 1)
        for clause in cnf:
            product = Fraction(1, 1)
            for var in clause:
                if abs(var) > n:
                    return None
                product *= (1 + x[abs(var)])
            term *= product
        return term
    
    def schur_function(n):
        # Placeholder implementation of Schur function
        # This is a dummy function and should be replaced with an actual implementation
        return Fraction(1, 2**n)
    
    def count_vanishing_schurs(poly, n):
        count = 0
        for i in range(1 << n):
            term = Fraction(1, 1)
            for j in range(n):
                if (i >> j) & 1:
                    term *= (1 + x[j+1])
                else:
                    term *= (1 - x[j+1])
            if poly == term:
                count += 1
        return count
    
    def is_acc0_circuit_size_bounded(cnf):
        # Placeholder implementation of ACC^0 circuit size check
        # This is a dummy function and should be replaced with an actual implementation
        return len(cnf) <= n**2
    
    n = random.randint(5, 40)
    cnf = [[random.randint(-n, n) for _ in range(random.randint(1, 3))] for _ in range(n)]
    
    clause_indicator_poly = compute_clause_indicator_poly(cnf)
    if clause_indicator_poly is None:
        return {
            "metric_name": "vanishing_schurs",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    vanishing_schurs = count_vanishing_schurs(clause_indicator_poly, n)
    acc0_bounded = is_acc0_circuit_size_bounded(cnf)
    
    return {
        "metric_name": "vanishing_schurs",
        "metric_value": vanishing_schurs,
        "instances_tested": 1,
        "conjecture_holds": vanishing_schurs == math.log(n, 2) and acc0_bounded,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv[1:]) > 0:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        seeds = [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")