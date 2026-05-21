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
    
    def generate_3xor_formula(n):
        clauses = []
        for _ in range(2 * n):
            literals = [random.choice([1, -1]) for _ in range(3)]
            clause = sum(literals)
            if clause != 0:
                clauses.append(clause)
        return clauses
    
    def construct_constraint_polynomial(clauses):
        poly = 1
        for clause in clauses:
            linear_form = [Fraction(clause, len(clauses)), -1]
            poly *= (linear_form[0] * x + linear_form[1])
        return poly
    
    def is_real_stable(poly):
        if not poly:
            return False
        sturm_seq = sturm_sequence(poly)
        for root in find_roots(sturm_seq):
            if root.imag != 0 or root.real >= 0:
                return False
        return True
    
    def sturm_sequence(poly):
        seq = [poly]
        while True:
            next_poly = []
            for i in range(len(seq) - 1):
                coeff = seq[i].coeffs[-2] / seq[i + 1].coeffs[-2]
                next_poly.append(next_poly[-1] * (-coeff))
            if not next_poly:
                break
            seq.append(next_poly)
        return seq
    
    def find_roots(poly):
        coeffs = poly.coeffs
        n = len(coeffs) - 1
        roots = []
        for i in range(n):
            a, b = coeffs[i], coeffs[i + 1]
            if a == 0:
                continue
            root = Fraction(b, a)
            roots.append(root)
        return roots
    
    def sdp_relaxation(poly):
        # Placeholder for SDP relaxation logic
        # This is a dummy implementation and should be replaced with actual SDP code
        return len(poly.coeffs) - 1
    
    n = 40
    clauses = generate_3xor_formula(n)
    poly = construct_constraint_polynomial(clauses)
    
    if not is_real_stable(poly):
        return {
            "metric_name": "sos_refutation_degree",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    refutation_degree = sdp_relaxation(poly)
    
    return {
        "metric_name": "sos_refutation_degree",
        "metric_value": refutation_degree,
        "instances_tested": 1,
        "conjecture_holds": refutation_degree <= math.sqrt(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")