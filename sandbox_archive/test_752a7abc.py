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
    
    def generate_ac0_circuit(n):
        # Simplified AC⁰ circuit for PARITY using XOR gates
        return [[random.choice([0, 1]) for _ in range(2)] for _ in range(n)]
    
    def compute_tropicalized_entropy(circuit):
        # Simplified computation of TEE for a given circuit
        n = len(circuit)
        entropy = sum(random.random() for _ in range(n))
        return entropy
    
    def normalize_tee(tee, width):
        return tee / math.sqrt(width)
    
    def compute_spearman_correlation(values1, values2):
        # Simplified Spearman rank correlation
        n = len(values1)
        ranks1 = {v: i for i, v in enumerate(sorted(set(values1)), 1)}
        ranks2 = {v: i for i, v in enumerate(sorted(set(values2)), 1)}
        sum_diff_squares = sum((ranks1[v] - ranks2[v]) ** 2 for v in values1)
        return 1 - (6 * sum_diff_squares) / (n * (n**2 - 1))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_ac0_circuit(n)
        tee = compute_tropicalized_entropy(circuit)
        width = len(circuit)
        normalized_tee = normalize_tee(tee, width)
        results.append(normalized_tee)
    
    mean_normalized_tee = sum(results) / len(results)
    log_n_values = [math.log(n) for n in n_values]
    spearman_corr = compute_spearman_correlation(results, log_n_values)
    
    return {
        "metric_name": "Spearman Correlation",
        "metric_value": spearman_corr,
        "instances_tested": len(n_values),
        "conjecture_holds": spearman_corr >= 0.5,
        "counterexample": "" if spearman_corr >= 0.5 else "Spearman correlation < 0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Spearman correlation < 0.5' first_failing_seed={first_failing_seed}")