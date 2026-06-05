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
    
    def generate_d_regular_circuit(d, n):
        if d * (n - 1) % (d + 1) != 0:
            return None
        circuit = []
        for i in range(n):
            row = [random.randint(0, 1) for _ in range(n)]
            circuit.append(row)
        return circuit
    
    def monotone_width(circuit):
        n = len(circuit)
        width = 0
        for i in range(n):
            for j in range(i + 1, n):
                if all(circuit[i][k] <= circuit[j][k] for k in range(n)):
                    width += 1
        return width
    
    def tropical_module_rank(circuit):
        n = len(circuit)
        rank = 0
        for i in range(n):
            row = [circuit[j][i] for j in range(n)]
            if any(row[k] == 1 for k in range(n)):
                rank += 1
        return rank
    
    def is_d_regular(circuit, d):
        n = len(circuit)
        degrees = [sum(row) for row in circuit]
        return all(degree == d for degree in degrees)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            d = random.randint(1, min(n - 1, 10))
            circuit = generate_d_regular_circuit(d, n)
            if circuit is None:
                continue
            if not is_d_regular(circuit, d):
                continue
            rank = tropical_module_rank(circuit)
            width = monotone_width(circuit)
            results.append((n, d, rank, width))
    
    if len(results) < 30:
        return {
            "metric_name": "monotone_width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean_rank = sum(rank for _, _, rank, _ in results) / len(results)
    mean_width = sum(width for _, _, _, width in results) / len(results)
    std_dev_rank = math.sqrt(sum((rank - mean_rank) ** 2 for _, _, rank, _ in results) / len(results))
    std_dev_width = math.sqrt(sum((width - mean_width) ** 2 for _, _, _, width in results) / len(results))
    
    conjecture_holds = all(abs(rank - width) <= 0.5 * (d ** 0.5 * n ** 0.3) for _, d, rank, width in results)
    counterexample = "" if conjecture_holds else "monotone_width > 1.5 * O(d^(1/2)n^(1/3))"
    
    return {
        "metric_name": "monotone_width",
        "metric_value": mean_width,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        if "conjecture_holds" in trial_result and not trial_result["conjecture_holds"]:
            break
        results.append(trial_result)
    
    if len(results) == 0 or any(not result["conjecture_holds"] for result in results):
        RESULT = "FALSIFIED counterexample=\"not_enough_valid_trials\" first_failing_seed=1"
    else:
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        RESULT = f"SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}"
    
    print(RESULT)