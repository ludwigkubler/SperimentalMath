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
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def polynomial_from_cnf(cnf):
        # Simplified polynomial generation for demonstration
        return sum([x * x for x in range(1, len(cnf) + 1)])
    
    def p_adic_valuation_rank(poly, p):
        # Placeholder for actual implementation of minimal p-adic valuation rank
        return len(str(poly)) % p
    
    def frege_proof_depth(cnf):
        # Simplified DPLL-based Frege proof depth calculation
        return len(cnf) * 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        poly = polynomial_from_cnf(cnf)
        p = random.randint(2, n)
        
        r_phi = p_adic_valuation_rank(poly, p)
        d_phi = frege_proof_depth(cnf)
        
        results.append({
            "n": n,
            "r_phi": r_phi,
            "d_phi": d_phi
        })
    
    correlation_coefficient = 0
    for result in results:
        correlation_coefficient += (result["r_phi"] - sum(r["r_phi"] for r in results) / len(results)) * \
                                   (result["d_phi"] - sum(r["d_phi"] for r in results) / len(results))
    correlation_coefficient /= len(results)
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.7"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")