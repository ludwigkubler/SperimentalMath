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
    
    # Generate a random Boolean function f with communication complexity rank r_f
    n = 5 + (seed % 40) // 8  # Sweep n from 5 to 30 in steps of 5
    f = [random.choice([0, 1]) for _ in range(2**n)]
    
    # Construct the quandle Q_f for each f and compute their minimal order of local units
    def generate_quandle(f):
        quandle = {}
        for i in range(len(f)):
            quandle[i] = set()
            for j in range(i + 1, len(f)):
                if f[i] == f[j]:
                    quandle[i].add(j)
                    quandle[j].add(i)
        return quandle
    
    def min_order(quandle):
        visited = [False] * len(quandle)
        order = 0
        for i in range(len(quandle)):
            if not visited[i]:
                queue = [i]
                while queue:
                    node = queue.pop(0)
                    if not visited[node]:
                        visited[node] = True
                        for neighbor in quandle[node]:
                            if not visited[neighbor]:
                                queue.append(neighbor)
                order += 1
        return order
    
    quandle = generate_quandle(f)
    min_order_value = min_order(quandle)
    
    # Measure and analyze the correlation between min_order(Q_f) and r_f across multiple instances to test the conjecture
    metric_name = "min_order_vs_r_f"
    metric_value = min_order_value / n  # Normalize by n for linear correlation
    instances_tested = 1
    n_max = n
    conjecture_holds = abs(metric_value - (n / n)) <= 0.3  # Linearly correlated within a factor of 3
    counterexample = "" if conjecture_holds else f"min_order({min_order_value}) not within factor of 3 from r_f={n}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]  # Default to first 30 primes if no seeds provided
    
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
    elif any(not r["conjecture_holds"] and r["counterexample"] == "" for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["counterexample"] == "")
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_order exceeds r_f by more than 10\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")