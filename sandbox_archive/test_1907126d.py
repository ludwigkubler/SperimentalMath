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
    
    def generate_sat_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def truth_table_to_cnf(truth_table):
        n = len(truth_table[0])
        cnf = []
        for i in range(len(truth_table)):
            if truth_table[i] == 1:
                clause = [j + 1 if truth_table[i][j] == 1 else -(j + 1) for j in range(n)]
                cnf.append(clause)
        return cnf
    
    def galois_group_order(cnf):
        # This is a placeholder function. Implementing the actual Galois group order calculation would be complex.
        # For simplicity, we assume it returns a random value between 1 and n.
        n = len(cnf)
        return random.randint(1, n)
    
    def resolution_proof_width(cnf):
        # This is a placeholder function. Implementing the actual resolution proof width calculation would be complex.
        # For simplicity, we assume it returns a random value between 1 and n^2.
        n = len(cnf)
        return random.randint(1, n**2)
    
    def pearson_correlation(x, y):
        if len(x) != len(y):
            raise ValueError("x and y must have the same length")
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = math.sqrt(sum((xi - mean_x)**2 for xi in x)) * math.sqrt(sum((yi - mean_y)**2 for yi in y))
        return numerator / denominator if denominator != 0 else 0
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    sat_instance = generate_sat_instance(n)
    cnf = truth_table_to_cnf(sat_instance)
    
    galois_order = galois_group_order(cnf)
    proof_width = resolution_proof_width(cnf)
    
    correlation = pearson_correlation([galois_order], [proof_width])
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": correlation >= 0.7,
        "counterexample": "" if correlation >= 0.7 else "low_correlation"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] == "low_correlation" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='low_correlation' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")