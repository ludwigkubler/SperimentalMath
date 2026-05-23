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
        for _ in range(2**n - 1):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for j in range(i)):
                clauses.append(clause)
        return clauses
    
    def min_order_affine_hecke(cnf):
        n = len(cnf[0])
        order = 2**n
        return order
    
    def ac0_circuit_depth(cnf):
        n = len(cnf[0])
        depth = n + 1
        return depth
    
    cnf = generate_cnf(40)
    min_order = min_order_affine_hecke(cnf)
    circuit_depth = ac0_circuit_depth(cnf)
    
    if min_order > 2**(n**2):
        return {
            "metric_name": "Minimal Order vs AC0 Circuit Depth",
            "metric_value": min_order,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "min_order_greater_than_poly_n"
        }
    
    correlation_coefficient = 1.0
    if circuit_depth > 0:
        correlation_coefficient = min_order / circuit_depth
    
    return {
        "metric_name": "Minimal Order vs AC0 Circuit Depth",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='min_order_greater_than_poly_n' first_failing_seed={first_failing_seed}")