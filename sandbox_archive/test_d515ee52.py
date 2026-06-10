# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def polynomial_from_boolean_function(f):
        n = len(next(iter(f.keys())))
        poly = [0] * (2**n)
        for x, y in f.items():
            index = sum(1 << i if bit == '1' else 0 for i, bit in enumerate(x))
            poly[index] = y
        return poly
    
    def tropical_derivative(poly):
        n = int(math.log2(len(poly)))
        mt = [0] * (2**n)
        for i in range(2**n):
            if i == 0:
                continue
            for j in range(n):
                if i & (1 << j) != 0:
                    neighbor = i ^ (1 << j)
                    mt[i] = max(mt[i], poly[neighbor])
        return mt
    
    def communication_complexity_rank_variance(f):
        n = len(next(iter(f.keys())))
        circuit_ranks = []
        for k in range(1, n+1):
            rank = 0
            for comb in combinations(range(n), k):
                subfunction = {x: f[x] for x in f if all(x[i] == '1' for i in comb)}
                rank = max(rank, len(subfunction))
            circuit_ranks.append(rank)
        return sum((r - n/2)**2 for r in circuit_ranks) / n
    
    def correlation_coefficient(mt, rc):
        n = len(mt)
        if n != len(rc):
            raise ValueError("Mismatched lengths")
        mean_mt = sum(mt) / n
        mean_rc = sum(rc) / n
        numerator = sum((mt[i] - mean_mt) * (rc[i] - mean_rc) for i in range(n))
        denominator = math.sqrt(sum((mt[i] - mean_mt)**2 for i in range(n))) * math.sqrt(sum((rc[i] - mean_rc)**2 for i in range(n)))
        return numerator / denominator if denominator != 0 else 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    mt_list = []
    rc_list = []
    
    for n in n_values:
        f = {bin(i)[2:].zfill(n): random.choice([0, 1]) for i in range(2**n)}
        poly = polynomial_from_boolean_function(f)
        mt = tropical_derivative(poly)
        rc = communication_complexity_rank_variance(f)
        mt_list.extend(mt)
        rc_list.extend(rc)
    
    if not mt_list or not rc_list:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Empty function set"
        }
    
    correlation = correlation_coefficient(mt_list, rc_list)
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": len(mt_list),
        "n_max": max(n_values),
        "conjecture_holds": 0.7 <= correlation < 0.9,
        "counterexample": "" if 0.7 <= correlation < 0.9 else f"Correlation {correlation:.2f} outside [0.7, 0.9]"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if 0.7 <= r["metric_value"] < 0.9) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results) and 0.7 <= min(r["metric_value"] for r in results if r["metric_value"] is not None) < 0.9:
        print(f"RESULT: FALSIFIED counterexample=\"Correlation outside [0.7, 0.9]\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds'] and 0.7 <= r['metric_value'] < 0.9))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(results)}")