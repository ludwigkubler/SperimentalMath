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
        if n % d != 0:
            return None
        circuit = []
        for i in range(d):
            layer = [random.choice([0, 1]) for _ in range(n // d)]
            circuit.append(layer)
        return circuit

    def monotone_width(circuit):
        n = len(circuit[0])
        width = 0
        for i in range(n):
            count = sum(1 for layer in circuit if layer[i] == 1)
            width = max(width, count)
        return width

    def tropical_rank(circuit):
        n = len(circuit[0])
        m = len(circuit)
        rank = 0
        for i in range(n):
            active_layers = [layer for layer in circuit if layer[i] == 1]
            if not active_layers:
                continue
            A = []
            for layer in active_layers:
                row = [1 if j < len(layer) and layer[j] == 1 else 0 for j in range(m)]
                A.append(row)
            rank += 1
        return rank

    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    d = 2  # Assuming a simple 2-regular circuit for simplicity
    
    for n in n_values:
        circuit = generate_d_regular_circuit(n, d)
        if circuit is None:
            continue
        mtr_value = monotone_width(circuit)
        tropical_rank_value = tropical_rank(circuit)
        results.append((n, mtr_value, tropical_rank_value, abs(mtr_value - tropical_rank_value)))

    if not results:
        return {
            "metric_name": "monotone_width_vs_tropical_rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid circuits generated"
        }

    n_max = max(n for n, _, _, _ in results)
    mean_metric_value = sum(abs(mtr - tropical_rank) for _, mtr, tropical_rank, _ in results) / len(results)
    std_metric_value = math.sqrt(sum((abs(mtr - tropical_rank) - mean_metric_value) ** 2 for _, mtr, tropical_rank, _ in results) / len(results))
    conjecture_holds = all(abs(mtr - tropical_rank) <= 0.5 * (d ** 0.5 * n ** (1/3)) for _, mtr, tropical_rank, _ in results)
    counterexample = "" if conjecture_holds else "First failing seed"

    return {
        "metric_name": "monotone_width_vs_tropical_rank",
        "metric_value": mean_metric_value,
        "instances_tested": len(results),
        "n_max": n_max,
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
        results.append(trial_result)

    if all("metric_value" not in result or result["metric_value"] is None for result in results):
        print("RESULT: INCONCLUSIVE no_valid_circuits_generated")
    else:
        mean_metric_value = sum(result["metric_value"] for result in results if "metric_value" in result and result["metric_value"] is not None) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if "metric_value" in result and result["metric_value"] is not None)) / len(results)
        support_fraction = sum(1 for result in results if "conjecture_holds" in result and result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        elif any("counterexample" in result for result in results):
            counterexample = next(result["counterexample"] for result in results if "counterexample" in result)
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" not in result or not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE insufficient_support")