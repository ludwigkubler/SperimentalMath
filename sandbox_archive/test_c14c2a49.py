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
    
    def communication_complexity_rank(f):
        n = len(f)
        truth_table = list(f.items())
        rank = 0
        while truth_table:
            min_bits = float('inf')
            for i in range(n):
                bits = [truth_table[j][1] for j in range(len(truth_table)) if (j >> i) & 1]
                if len(set(bits)) < min_bits:
                    min_bits = len(set(bits))
            rank += math.ceil(math.log2(min_bits))
            truth_table = [(k, v) for k, v in truth_table if (k >> rank) & 1 == v]
        return rank
    
    def minimal_quadratic_residue_degree(f):
        n = len(f)
        residues = set()
        for x in range(1, n + 1):
            if pow(x, 2, n) not in residues:
                residues.add(pow(x, 2, n))
        return len(residues)
    
    def variance(values):
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)
    
    n_values = [5, 10, 15, 20, 30, 40]
    V_f_values = []
    D_min_f_values = []
    
    for n in n_values:
        f = {tuple(random.randint(0, 1) for _ in range(n)): random.choice([0, 1]) for _ in range(2**n)}
        if communication_complexity_rank(f) > 10:
            continue
        V_f_values.append(variance(list(f.values())))
        D_min_f_values.append(minimal_quadratic_residue_degree(f))
    
    if not V_f_values or not D_min_f_values:
        return {
            "metric_name": "Variance of Communication Complexity Rank",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_metric"
        }
    
    V_f_mean = sum(V_f_values) / len(V_f_values)
    D_min_f_squared_mean = sum(x**2 for x in D_min_f_values) / len(D_min_f_values)
    correlation_coefficient = (sum((V_f_values[i] - V_f_mean) * (D_min_f_values[i]**2 - D_min_f_squared_mean) for i in range(len(V_f_values))) /
                               math.sqrt(sum((V_f_values[i] - V_f_mean)**2 for i in range(len(V_f_values))) *
                                         sum((D_min_f_values[i]**2 - D_min_f_squared_mean)**2 for i in range(len(D_min_f_values)))))
    
    return {
        "metric_name": "Variance of Communication Complexity Rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(V_f_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    V_f_values = [r["metric_value"] for r in results if "metric_value" in r and not r["counterexample"]]
    instances_tested = sum(r["instances_tested"] for r in results)
    n_max = max(r["n_max"] for r in results)
    conjecture_holds = all(r["conjecture_holds"] for r in results if "conjecture_holds" in r and not r["counterexample"])
    
    if conjecture_holds:
        mean = sum(V_f_values) / len(V_f_values)
        std = math.sqrt(sum((x - mean)**2 for x in V_f_values) / len(V_f_values))
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction=1.0")
    elif V_f_values:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" not in result and not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")