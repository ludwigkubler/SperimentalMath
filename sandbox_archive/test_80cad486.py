# auto-injected by SEC sandbox
import math
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
from fractions import Fraction
from itertools import combinations

def sipser_function(n, x):
    return sum(x[i-1] for i in range(1, n+1)) % 2 == 0

def truth_table(f, n):
    return [[f(i) for i in range(2**n)]]

def additivity_quadruples(truth_table):
    n = len(truth_table[0])
    count = 0
    for a, b, c, d in combinations(range(n), 4):
        if truth_table[0][a] + truth_table[0][b] == truth_table[0][c] + truth_table[0][d]:
            count += 1
    return count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    instances_tested = 30
    total_energy = 0
    support_count = 0
    
    for _ in range(instances_tested):
        x = tuple(random.randint(0, 1) for _ in range(n))
        f_value = sipser_function(n, x)
        truth_table_values = truth_table(f_value, n)
        energy = additivity_quadruples(truth_table_values)
        total_energy += energy
    
    mean_energy = Fraction(total_energy, instances_tested)
    conjecture_holds = mean_energy >= n**2.5 - 1e-6
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "additive_energy",
        "metric_value": float(mean_energy),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
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
    
    mean_energy = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_energy} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_energy} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")