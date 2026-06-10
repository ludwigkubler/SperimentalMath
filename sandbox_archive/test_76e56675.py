# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def construct_stabilizer_state(cnf):
        n = len(set(abs(lit) for lit in cnf))
        state = [0] * (2 ** n)
        return state
    
    def calculate_entropy(state):
        total = sum(state)
        if total == 0:
            return 0
        p = [x / total for x in state]
        entropy = -sum(p_i * math.log2(p_i) for p_i in p if p_i > 0)
        return entropy
    
    def calculate_resolution_width(cnf):
        # Placeholder function, replace with actual resolution width calculation
        return len(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            cnf = [[random.randint(-n, n) for _ in range(random.randint(1, 3))] for _ in range(n)]
            state = construct_stabilizer_state(cnf)
            entropy = calculate_entropy(state)
            width = calculate_resolution_width(cnf)
            
            metric_values.append((entropy, width))
            instances_tested += 1
            n_max = max(n_max, n)
    
    if len(metric_values) < 30:
        return {
            "metric_name": "Entropy vs Width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    entropies = [v[0] for v in metric_values]
    widths = [v[1] for v in metric_values]
    mean_entropy = sum(entropies) / len(entropies)
    mean_width = sum(widths) / len(widths)
    
    correlation_coefficient = 0
    if mean_entropy != 0 and mean_width != 0:
        numerator = sum((entropies[i] - mean_entropy) * (widths[i] - mean_width) for i in range(len(entropies)))
        denominator = math.sqrt(sum((entropies[i] - mean_entropy) ** 2 for i in range(len(entropies)))) * math.sqrt(sum((widths[i] - mean_width) ** 2 for i in range(len(widths))))
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = correlation_coefficient >= 0.9
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.9"
    
    return {
        "metric_name": "Entropy vs Width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None]))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] == "correlation_coefficient < 0.9" for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.9\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")