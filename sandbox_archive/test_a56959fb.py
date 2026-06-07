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
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        min_bits = float('inf')
        for i in range(2**n):
            for j in range(2**n):
                if f[i] != f[j]:
                    bits = 0
                    while (i >> bits) & 1 == (j >> bits) & 1:
                        bits += 1
                    min_bits = min(min_bits, bits)
        return min_bits
    
    def minimal_quadratic_residue_degree(f):
        n = int(math.log2(len(f)))
        residues = set()
        for x in range(2**n):
            if f[x] == 1:
                residues.add(x % (2*n))
        return max(residues, default=0)
    
    def variance(values):
        mean = sum(values) / len(values)
        return sum((x - mean)**2 for x in values) / len(values)
    
    n_values = [5, 10, 15, 20, 30, 40]
    V_f_values = []
    D_min_f_values = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        if communication_complexity_rank(f) > 10:
            return {
                "metric_name": "communication_complexity_rank",
                "metric_value": None,
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "communication_complexity_rank > 10"
            }
        V_f = communication_complexity_rank(f)
        D_min_f = minimal_quadratic_residue_degree(f)
        V_f_values.append(V_f)
        D_min_f_values.append(D_min_f**2)
    
    correlation_coefficient = sum((V_f - mean_V_f) * (D_min_f - mean_D_min_f) for V_f, D_min_f in zip(V_f_values, D_min_f_values)) / len(V_f_values)
    mean_V_f = sum(V_f_values) / len(V_f_values)
    std_V_f = math.sqrt(variance(V_f_values))
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 35)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")