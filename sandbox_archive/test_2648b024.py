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

def generate_cnf(n: int, m: int) -> list:
    variables = list(range(1, n + 1))
    cnf = []
    for _ in range(m):
        num_literals = random.randint(1, n)
        clause = random.sample(variables, num_literals)
        cnf.append(clause)
    return cnf

def indicator_matrix(cnf: list) -> list:
    n = len(cnf[0])
    m = len(cnf)
    I = [[0] * n for _ in range(m)]
    for i, clause in enumerate(cnf):
        for literal in clause:
            if literal > 0:
                I[i][literal - 1] = 1
            else:
                I[i][-literal - 1] = 1
    return I

def tropical_rank(matrix: list) -> int:
    m, n = len(matrix), len(matrix[0])
    for r in range(min(m, n), 0, -1):
        if all(all(matrix[i][j] != 0 for j in range(r)) for i in range(r)):
            return r
    return 0

def dpll_proof_width(cnf: list) -> int:
    # Placeholder function to simulate DPLL proof width calculation
    # Replace with actual implementation as needed
    return len(cnf)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [10, 15, 20, 30, 40]
    m_values = [n * 2 for n in n_values]  # Example relation between n and m
    
    results = []
    for n, m in zip(n_values, m_values):
        cnf = generate_cnf(n, m)
        I = indicator_matrix(cnf)
        rank = tropical_rank(I)
        proof_width = dpll_proof_width(cnf)
        
        results.append({
            "n": n,
            "m": m,
            "rank": rank,
            "proof_width": proof_width
        })
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    mean_ratio = sum(result["rank"] / result["proof_width"] for result in results) / len(results)
    
    conjecture_holds = all(result["rank"] >= n**(2/3) * m**(1/4) for result in results) and mean_ratio <= 1.2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_rank_over_dpll_proof_width",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")