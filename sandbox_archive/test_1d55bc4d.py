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
    
    def generate_boolean_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(circuit):
        n = len(circuit)
        rank = sum(circuit[i] != circuit[j] for i in range(n) for j in range(i+1, n)) / (n * (n - 1))
        return rank
    
    def minimal_brauer_group_order(circuit):
        n = len(circuit)
        order = 2 ** n
        return order
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    results = []
    for _ in range(30):
        circuit = generate_boolean_circuit(random.randint(5, 40))
        R_C = communication_complexity_rank_variance(circuit)
        B_C_order = minimal_brauer_group_order(circuit)
        log_B_C = log2(B_C_order)
        results.append((log_B_C, R_C))
    
    if not results:
        return {
            "metric_name": "log2(|B(C)|) vs R_C",
            "metric_value": float('nan'),
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    log_B_C_values = [x[0] for x in results]
    R_C_values = [x[1] for x in results]
    
    mean_log_B_C = sum(log_B_C_values) / len(log_B_C_values)
    std_log_B_C = math.sqrt(sum((x - mean_log_B_C) ** 2 for x in log_B_C_values) / len(log_B_C_values))
    
    support_fraction = sum(1 for log_B_C, R_C in results if abs(log_B_C - R_C) <= std_log_B_C) / len(results)
    
    return {
        "metric_name": "log2(|B(C)|) vs R_C",
        "metric_value": mean_log_B_C,
        "instances_tested": 30,
        "n_max": max(len(circuit) for circuit in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"support_fraction={support_fraction:.2f}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(x["metric_value"] for x in results if not math.isnan(x["metric_value"])) / len(results)
    std_metric_value = math.sqrt(sum((x["metric_value"] - mean_metric_value) ** 2 for x in results if not math.isnan(x["metric_value"])) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(math.isnan(x["metric_value"]) for x in results):
        print("RESULT: INCONCLUSIVE no_results")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction={support_fraction:.2f}\" first_failing_seed={first_failing_seed}")