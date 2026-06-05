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
    
    def generate_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def monotone_width(circuit):
        n = len(circuit)
        width = 0
        for i in range(n):
            if circuit[i] == 1:
                width += 1
        return width
    
    def algebraic_k_theory_rank(circuit):
        n = len(circuit)
        rank = sum(1 for x in circuit if x == 1)
        return rank
    
    def contains_and_gate(circuit):
        n = len(circuit)
        for i in range(n-2):
            if circuit[i] == 1 and circuit[i+1] == 0 and circuit[i+2] == 1:
                return True
        return False
    
    metrics = []
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_circuit(n)
            r_K = algebraic_k_theory_rank(circuit)
            w_mon = monotone_width(circuit)
            
            metrics.append((r_K, w_mon))
            instances_tested += 1
            
            if abs(r_K - w_mon) > 3:
                conjecture_holds = False
                counterexample = f"Circuit with n={n} and r_K={r_K}, w_mon={w_mon}"
            
            if r_K > 2 * w_mon and not contains_and_gate(circuit):
                conjecture_holds = False
                counterexample = f"Circuit with n={n} and r_K={r_K}, w_mon={w_mon}"
    
    if instances_tested < 30:
        return {
            "metric_name": "algebraic_k_theory_rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    r_K_values, w_mon_values = zip(*metrics)
    correlation_coefficient = sum((r_K - mean_r_K) * (w_mon - mean_w_mon) for r_K, w_mon in metrics) / math.sqrt(sum((r_K - mean_r_K)**2 for r_K in r_K_values) * sum((w_mon - mean_w_mon)**2 for w_mon in w_mon_values))
    mean_r_K = sum(r_K_values) / len(r_K_values)
    
    return {
        "metric_name": "algebraic_k_theory_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] != "" for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if not r['conjecture_holds'] and r['counterexample'] != 'insufficient_instances')}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")