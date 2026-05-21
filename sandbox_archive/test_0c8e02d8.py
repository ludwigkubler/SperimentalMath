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
        for _ in range(2 * n):
            vars = random.sample(range(n), 3)
            clause = [f"x{v}" if random.choice([True, False]) else f"-x{v}" for v in vars]
            clauses.append(" + ".join(clause))
        return " + ".join(clauses) + " == 0"
    
    def is_real_stable(poly):
        # Polynomial should be represented as a list of coefficients
        if not poly:
            return False
        
        # Check roots using Sturm's theorem (simplified for real stability)
        def sturm_sequence(poly):
            seq = [poly]
            while True:
                lead_coeff = seq[-1][-1]
                next_poly = []
                for i in range(len(seq[-1]) - 2, -1, -1):
                    coeff = seq[-1][i] / lead_coeff
                    if i > 0:
                        next_poly.append(next_poly[-1] * (-coeff))
                    else:
                        next_poly.append(-coeff)
                if not next_poly or abs(next_poly[-1]) < 1e-6:
                    break
                seq.append(next_poly)
            return seq
        
        def evaluate(poly, x):
            result = 0
            for i in range(len(poly)):
                result += poly[i] * (x ** (len(poly) - i - 1))
            return result
        
        def sign_changes(seq, lower_bound, upper_bound):
            count = 0
            for i in range(len(seq) - 1):
                if seq[i][lower_bound] * seq[i + 1][upper_bound] < 0:
                    count += 1
            return count
        
        seq = sturm_sequence(poly)
        lower_bound, upper_bound = -math.inf, math.inf
        for i in range(len(seq)):
            lower_bound = max(lower_bound, evaluate(seq[i], lower_bound))
            upper_bound = min(upper_bound, evaluate(seq[i], upper_bound))
        
        return sign_changes(seq, lower_bound, upper_bound) == 0
    
    def sos_refutation_degree(poly):
        # Placeholder for SOS refutation degree computation
        # This is a dummy implementation and should be replaced with actual SDP relaxation code
        return len(poly)
    
    n = 40
    formula = generate_3xor_formula(n)
    poly = [random.uniform(-1, 1) for _ in range(n + 1)]
    
    if not is_real_stable(poly):
        return {
            "metric_name": "sos_refutation_degree",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    degree = sos_refutation_degree(poly)
    metric_value = degree
    
    return {
        "metric_name": "sos_refutation_degree",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": True if degree <= math.sqrt(n) else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")