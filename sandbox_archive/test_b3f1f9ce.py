# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def communication_rank(f):
    n = len(f)
    rank = 0
    for i in range(n):
        if any(f[j] != f[j ^ (1 << i)] for j in range(len(f))):
            rank += 1
    return rank

def p_adic_galois_representation(f):
    n = len(f)
    order = 2**n
    while True:
        found = False
        for i in range(order):
            if all((f[j] + f[j ^ (1 << k)]) % 2 == 0 for j in range(len(f)) for k in range(n)):
                found = True
                break
        if not found:
            order -= 1
        else:
            return order

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        f = generate_boolean_function(n)
        rho_f = p_adic_galois_representation(f)
        rank_gal_f = communication_rank(f)
        results.append((n, rho_f, rank_gal_f))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    n_max = max(n for _, _, _ in results)
    instances_tested = len(results)
    rho_values = [rho for _, rho, _ in results]
    rank_gal_values = [rank for _, _, rank in results]
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_rho = sum(rho_values) / instances_tested
    mean_rank_gal = sum(rank_gal_values) / instances_tested
    
    correlation_coefficient = 0
    for rho, rank in zip(rho_values, rank_gal_values):
        correlation_coefficient += (rho - mean_rho) * (rank - mean_rank_gal)
    correlation_coefficient /= instances_tested * (sum((rho - mean_rho)**2 for rho in rho_values) / instances_tested) ** 0.5 * (sum((rank - mean_rank_gal)**2 for rank in rank_gal_values) / instances_tested) ** 0.5
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("conjecture_holds" in r and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" in result and not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")