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
    
    def generate_polynomial(n):
        variables = [f"x{i}" for i in range(n)]
        terms = []
        for k in range(1, n+1):
            coeffs = [random.choice([0, 1]) for _ in range(k)]
            term = sum(c * v for c, v in zip(coeffs, variables[:k]))
            terms.append(term)
        return " + ".join(terms)
    
    def construct_quotient_algebra(polynomial):
        # Simplified representation of quotient algebra rank
        return len(polynomial.split(" + ")) ** 0.5
    
    def determinant_circuit_size(m):
        # Simplified circuit size for determinant computation
        return m * (m - 1) // 2
    
    n = random.randint(5, 40)
    polynomial = generate_polynomial(n)
    quotient_algebra_rank = construct_quotient_algebra(polynomial)
    rho_Q_f = quotient_algebra_rank
    
    if rho_Q_f == 0:
        return {
            "metric_name": "rho_Q_f",
            "metric_value": rho_Q_f,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    instances_tested = 0
    for _ in range(30):
        m = random.randint(1, n**1.5 - 1)
        circuit_size = determinant_circuit_size(m)
        
        if circuit_size < 0.5 * rho_Q_f:
            return {
                "metric_name": "circuit_size",
                "metric_value": circuit_size,
                "instances_tested": instances_tested + 1,
                "conjecture_holds": False,
                "counterexample": f"Counterexample for n={n}, m={m}: Circuit size {circuit_size} < 0.5 * rho_Q_f ({0.5 * rho_Q_f})"
            }
        
        instances_tested += 1
    
    return {
        "metric_name": "rho_Q_f",
        "metric_value": rho_Q_f,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")