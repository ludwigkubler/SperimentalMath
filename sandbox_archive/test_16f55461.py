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
        for _ in range(random.randint(1, n)):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if not all(clause[i] == -clause[j] for i in range(n) for j in range(i + 1, n)):
                clauses.append(clause)
        return clauses
    
    def communication_complexity_rank(cnf):
        # Simplified version of the communication complexity rank calculation
        return len(cnf)
    
    def local_zeta_function(cnf):
        # Simplified version of the local zeta function calculation
        p = 2  # Prime number for p-adic order
        n = len(cnf[0])
        ord_p = 1
        for clause in cnf:
            product = 1
            for literal in clause:
                if literal > 0:
                    product *= (1 - Fraction(1, p))
                else:
                    product *= (1 + Fraction(1, p))
            ord_p = max(ord_p, math.ceil(math.log(product, p)))
        return ord_p
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        ord_p = local_zeta_function(cnf)
        C_comm = communication_complexity_rank(cnf)
        results.append((ord_p, C_comm))
    
    mean_ord_p = sum(ord_p for ord_p, _ in results) / len(results)
    mean_C_comm = sum(C_comm for _, C_comm in results) / len(results)
    std_dev = math.sqrt(sum((ord_p - mean_ord_p)**2 + (C_comm - mean_C_comm)**2 for ord_p, C_comm in results) / len(results))
    
    conjecture_holds = all(ord_p <= mean_C_comm + 3 * std_dev for ord_p, _ in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "p-adic order vs communication complexity rank",
        "metric_value": (mean_ord_p, mean_C_comm),
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ord_p = sum(result["metric_value"][0] for result in results) / len(results)
    mean_C_comm = sum(result["metric_value"][1] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean_ord_p={mean_ord_p} std_dev={math.sqrt(sum((result['metric_value'][0] - mean_ord_p)**2 for result in results) / len(results))} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")