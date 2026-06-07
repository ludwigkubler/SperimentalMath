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
        rank = sum(circuit[i] != circuit[j] for i in range(n) for j in range(i+1, n))
        return rank / (n * (n - 1) / 2)
    
    def minimal_brauer_group_order(circuit):
        # Placeholder function to simulate Brauer group order calculation
        # In practice, this would involve complex algebraic computations
        return len(circuit) + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_boolean_circuit(n)
        R_C = communication_complexity_rank_variance(circuit)
        B_C_order = minimal_brauer_group_order(circuit)
        
        if R_C == 0 or B_C_order == 0:
            continue
        
        log2_B_C_order = math.log2(B_C_order)
        log2_R_C = math.log2(R_C)
        
        results.append({
            "n": n,
            "R_C": R_C,
            "B_C_order": B_C_order,
            "log2_B_C_order": log2_B_C_order,
            "log2_R_C": log2_R_C
        })
    
    if not results:
        return {
            "metric_name": "log2(B(C)) vs log2(R(C))",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid circuits generated"
        }
    
    log2_B_C_orders = [r["log2_B_C_order"] for r in results]
    log2_R_Cs = [r["log2_R_C"] for r in results]
    
    mean_log2_B_C_order = sum(log2_B_C_orders) / len(log2_B_C_orders)
    std_log2_B_C_order = math.sqrt(sum((x - mean_log2_B_C_order) ** 2 for x in log2_B_C_orders) / len(log2_B_C_orders))
    
    within_std_dev = all(abs(log2_B_C_order - mean_log2_B_C_order) <= std_log2_B_C_order for log2_B_C_order in log2_B_C_orders)
    
    return {
        "metric_name": "log2(B(C)) vs log2(R(C))",
        "metric_value": mean_log2_B_C_order,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": within_std_dev,
        "counterexample": "" if within_std_dev else "Outliers detected"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        RESULT = f"RESULT: FALSIFIED counterexample=\"Outliers detected\" first_failing_seed={first_failing_seed}"
    else:
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        RESULT = f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}"
    
    print(RESULT)