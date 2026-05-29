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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def hamiltonian_dynamics(f):
        n = int(math.log2(len(f)))
        H_f = 0
        for i in range(2**n):
            for j in range(i + 1, 2**n):
                if f[i] != f[j]:
                    H_f += 1
        return H_f / (2**(n-1) * n)
    
    def resolution_proof_depth(f):
        n = int(math.log2(len(f)))
        depth = 0
        while len(f) > 1:
            new_f = []
            for i in range(0, len(f), 2):
                if f[i] != f[i+1]:
                    new_f.append(1)
                else:
                    new_f.append(0)
            f = new_f
            depth += 1
        return depth
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        H_f = hamiltonian_dynamics(f)
        t_star_f = resolution_proof_depth(f)
        results.append({"n": n, "H_f": H_f, "t_star_f": t_star_f})
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    H_f_squared = [r["H_f"]**2 for r in results]
    correlation_coefficient = sum((H_f_squared[i] - mean_H_f_squared) * (results[i]["t_star_f"] - mean_t_star_f) for i in range(len(results))) / math.sqrt(sum((H_f_squared[i] - mean_H_f_squared)**2 for i in range(len(results))) * sum((results[i]["t_star_f"] - mean_t_star_f)**2 for i in range(len(results))))
    mean_H_f_squared = sum(H_f_squared) / len(H_f_squared)
    mean_t_star_f = sum(r["t_star_f"] for r in results) / len(results)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": correlation_coefficient >= 0.7 and all(r["H_f"]**2 <= r["t_star_f"] for r in results),
        "counterexample": "" if correlation_coefficient >= 0.7 and all(r["H_f"]**2 <= r["t_star_f"] for r in results) else "correlation_coefficient < 0.7 or H(f)^2 > t*(f)"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.getrandbits(32) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] != "" for r in results):
        counterexample = next(r["counterexample"] for r in results if r["counterexample"] != "")
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")