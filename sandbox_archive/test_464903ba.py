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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def characteristic_polynomial(f):
    n = len(f)
    poly = [[Fraction(0)] * (n + 1) for _ in range(n + 1)]
    poly[0][0] = Fraction(1)
    
    for i in range(n):
        for j in range(i, n):
            if f[i] == 1:
                for k in range(j, -1, -1):
                    poly[j][k] += poly[i][k]
                for k in range(j + 1, n + 1):
                    poly[j][k] -= poly[i][k - 1]
    
    return [sum(row) for row in poly]

def geometric_entropy(poly):
    n = len(poly)
    max_plus_poly = [[max(a, b) for a, b in zip(row, col)] for row, col in zip(*poly)]
    entropy = 0
    for i in range(n):
        for j in range(i + 1, n):
            if max_plus_poly[i][j] > 0:
                entropy += math.log(max_plus_poly[i][j])
    return -entropy / (n * (n - 1) / 2)

def communication_complexity_rank_variance(f):
    n = len(f)
    rank = 0
    for i in range(n):
        if any(f[j] == 1 for j in range(2**i, 2**(i + 1))):
            rank += 1
    return (rank - 1) ** 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        poly = characteristic_polynomial(f)
        ge = geometric_entropy(poly)
        rcv = communication_complexity_rank_variance(f)
        
        if ge == 0 or rcv == 0:
            continue
        
        results.append({
            "n": n,
            "ge": ge,
            "rcv": rcv
        })
    
    if not results:
        return {
            "metric_name": "GE vs RCV",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    n_max = max(result["n"] for result in results)
    ge_values = [result["ge"] for result in results]
    rcv_values = [result["rcv"] for result in results]
    
    correlation_coefficient = sum((x - mean(ge_values)) * (y - mean(rcv_values)) for x, y in zip(ge_values, rcv_values)) / (len(results) * std_dev(ge_values) * std_dev(rcv_values))
    
    return {
        "metric_name": "GE vs RCV",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) > 0.1,  # Significantly different from zero
        "counterexample": ""
    }

def mean(values):
    return sum(values) / len(values)

def std_dev(values):
    avg = mean(values)
    variance = sum((x - avg) ** 2 for x in values) / len(values)
    return math.sqrt(variance)

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean([r['metric_value'] for r in results])} std={std_dev([r['metric_value'] for r in results])} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")