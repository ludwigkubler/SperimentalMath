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
    
    def generate_d_regular_circuit(n, d):
        if n < d or (n - 1) % (d - 1) != 0:
            return None
        circuit = []
        for i in range(d):
            layer = [random.choice([0, 1]) for _ in range((n - 1) // (d - 1))]
            circuit.append(layer)
        return circuit
    
    def compute_p_adic_hodge_rank(circuit):
        if not circuit:
            return 0
        n = len(circuit[0])
        A = [[0] * n for _ in range(n)]
        for layer in circuit:
            for i in range(n):
                for j in range(i + 1, n):
                    A[i][j] += layer[i] ^ layer[j]
        rank = 0
        for row in A:
            if any(row):
                rank += 1
                for i in range(n):
                    if row[i]:
                        for j in range(n):
                            A[j][i] ^= row[j]
        return rank
    
    def compute_monotone_width(circuit):
        n = len(circuit[0])
        width = 0
        for layer in circuit:
            count = sum(layer)
            if count > width:
                width = count
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        d = random.randint(2, min(n - 1, 5))
        circuit = generate_d_regular_circuit(n, d)
        if not circuit:
            continue
        rank = compute_p_adic_hodge_rank(circuit)
        width = compute_monotone_width(circuit)
        results.append((rank, width))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ranks = [r for r, w in results]
    widths = [w for r, w in results]
    n_max = max(n_values)
    
    def pearson_correlation(x, y):
        if len(x) != len(y):
            return 0.0
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / len(y))
        if std_x == 0 or std_y == 0:
            return 0.0
        return cov / (std_x * std_y)
    
    correlation = pearson_correlation(ranks, widths)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": correlation > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_trials_run")
        sys.exit(0)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_not_sufficiently_positive\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")