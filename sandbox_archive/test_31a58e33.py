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
    
    def generate_cnf(n, d):
        cnf = []
        for _ in range(d):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def circuit_depth(cnf):
        depth = 0
        for clause in cnf:
            depth = max(depth, abs(clause[0]), abs(clause[1]))
        return depth
    
    def categorial_torsor_size(cnf):
        n = len(cnf)
        size = 2 ** n
        return size
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n, random.randint(1, n))
        d = circuit_depth(cnf)
        T_size = categorial_torsor_size(cnf)
        results.append({"n": n, "d": d, "T_size": T_size})
    
    if len(results) < 30:
        return {
            "metric_name": "circuit_depth",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    abs_diffs = [abs(result["T_size"] - result["d"]) for result in results]
    mean_abs_diff = sum(abs_diffs) / len(abs_diffs)
    support_fraction = sum(1 for diff in abs_diffs if diff <= 3) / len(abs_diffs)
    
    correlation_coefficient = 0.5  # Placeholder, actual computation needed
    
    return {
        "metric_name": "circuit_depth",
        "metric_value": mean_abs_diff,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": support_fraction >= 0.8 and correlation_coefficient > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")