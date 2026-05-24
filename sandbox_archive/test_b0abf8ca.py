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
    
    def generate_ac0_parity_circuit(n):
        # Generate a random AC0 parity circuit
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_min_non_archimedean_value(circuit):
        # Compute the minimal non-Archimedean value of the function
        min_val = float('inf')
        for x in range(2**len(circuit)):
            val = sum(circuit[i] * (x >> i) & 1 for i in range(len(circuit)))
            if val < min_val:
                min_val = val
        return min_val
    
    def p_adic_log(x, p):
        # Compute the p-adic logarithm of x
        if x <= 0:
            return float('-inf')
        log_val = 0
        while x % p == 0:
            x //= p
            log_val += 1
        return log_val
    
    def spearman_rank_correlation(x, y):
        # Compute the Spearman's rank correlation coefficient
        n = len(x)
        ranks_x = {x[i]: i for i in range(n)}
        ranks_y = {y[i]: i for i in range(n)}
        sorted_ranks_x = sorted(ranks_x.values())
        sorted_ranks_y = sorted(ranks_y.values())
        sum_diff_squares = sum((sorted_ranks_x[i] - sorted_ranks_y[i]) ** 2 for i in range(n))
        return 1 - (6 * sum_diff_squares) / (n * (n**2 - 1))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        circuit_size = len(generate_ac0_parity_circuit(n))
        min_non_archimedean_val = compute_min_non_archimedean_value(circuit)
        p_adic_log_val = p_adic_log(min_non_archimedean_val, 2)  # Assuming base 2 for simplicity
        results.append((circuit_size, p_adic_log_val))
    
    if len(results) < 30:
        return {
            "metric_name": "Spearman's rank correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    x = [result[0] for result in results]
    y = [result[1] for result in results]
    crc = spearman_rank_correlation(x, y)
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": crc,
        "instances_tested": len(results),
        "conjecture_holds": crc >= 0.7,
        "counterexample": "" if crc >= 0.7 else f"Spearman's rank correlation coefficient is {crc}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("metric_value" not in r or r["metric_value"] is None for r in results):
        print("RESULT: INCONCLUSIVE insufficient_data")
    else:
        crc_values = [r["metric_value"] for r in results if "metric_value" in r and r["metric_value"] is not None]
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={sum(crc_values) / len(crc_values)} std={math.sqrt(sum((x - sum(crc_values) / len(crc_values)) ** 2 for x in crc_values) / len(crc_values))} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, r in zip(seeds, results) if "conjecture_holds" not in r or not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"Spearman's rank correlation coefficient is below 0.7\" first_failing_seed={first_failing_seed}")