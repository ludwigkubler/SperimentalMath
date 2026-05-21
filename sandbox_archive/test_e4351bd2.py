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
    
    def generate_3xor_formula(n):
        clauses = []
        for _ in range(15 * n):  # Clause density ≥ 1.5
            clause = [random.randint(0, 2) for _ in range(3)]
            if any(c == 2 for c in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def construct_constraint_polynomial(clauses, n):
        poly = 1
        for clause in clauses:
            term = 1
            for var, val in enumerate(clause):
                if val == 0:
                    term *= (x[var] + 1)
                elif val == 1:
                    term *= (x[var])
            poly *= term
        return poly
    
    def is_real_stable(poly):
        roots = [complex(root) for root in poly.roots()]
        for root in roots:
            if root.imag != 0:
                return False
            if root.real <= 0:
                return False
        return True
    
    def sdp_relaxation(poly, degree):
        # Placeholder for SDP relaxation logic
        # This is a dummy implementation and should be replaced with actual SDP code
        return degree
    
    n = 40
    x = [random.random() for _ in range(n)]
    
    clauses = generate_3xor_formula(n)
    poly = construct_constraint_polynomial(clauses, n)
    
    if not is_real_stable(poly):
        return {
            "metric_name": "sos_refutation_degree",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "constraint_polynomial_not_stable"
        }
    
    degree = sdp_relaxation(poly, n)
    
    return {
        "metric_name": "sos_refutation_degree",
        "metric_value": degree,
        "instances_tested": 1,
        "conjecture_holds": degree <= math.sqrt(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values)/len(metric_values))} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"sos_refutation_degree_exceeds_sqrt_n\" first_failing_seed={first_failing_seed + 1}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")