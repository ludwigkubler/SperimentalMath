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
    
    def generate_cnf(m, n):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def norm_of_noncommutative_space(cnf):
        # Placeholder function to compute the norm of the noncommutative space
        # This is a dummy implementation for demonstration purposes
        m = len(cnf)
        n = max(abs(lit) for clause in cnf for lit in clause)
        return Fraction(m * n, 1)
    
    def resolution_proof_length(cnf):
        # Placeholder function to compute the resolution proof length
        # This is a dummy implementation for demonstration purposes
        m = len(cnf)
        n = max(abs(lit) for clause in cnf for lit in clause)
        return m + n
    
    results = []
    for _ in range(30):
        m = random.randint(5, 40)
        n = random.randint(5, 40)
        cnf = generate_cnf(m, n)
        norm = norm_of_noncommutative_space(cnf)
        proof_length = resolution_proof_length(cnf)
        results.append((norm, proof_length))
    
    if not results:
        return {
            "metric_name": "N(φ)",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    n_values = [(norm, n) for norm, _ in results]
    m_values = [(proof_length, m) for _, proof_length in results]
    
    metric_value = sum(norm for norm, _ in results) / len(results)
    instances_tested = len(results)
    n_max = max(n for _, n in n_values)
    
    conjecture_holds = all(0.95 * norm <= proof_length <= 1.1 * norm for norm, proof_length in results)
    counterexample = "" if conjecture_holds else "norm_exceeds_bound"
    
    return {
        "metric_name": "N(φ)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = Fraction(len([r for r in results if r["conjecture_holds"]]), len(results))
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"norm_exceeds_bound\" first_failing_seed={first_failing_seed}")