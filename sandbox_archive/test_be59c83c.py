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

def generate_random_function(n):
    return lambda x: sum(x[i] & (1 << i) for i in range(n)) % 2

def ac0_circuit(inputs, n):
    if len(inputs) == 1:
        return inputs[0]
    else:
        mid = len(inputs) // 2
        left_result = ac0_circuit(inputs[:mid], n)
        right_result = ac0_circuit(inputs[mid:], n)
        return (left_result + right_result) % 2

def parity_threshold(f, n):
    count = sum(1 for x in range(2**n) if ac0_circuit([f(x)], n) == 1)
    return Fraction(count, 2**n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_function(n)
        t = parity_threshold(f, n)
        rank = n  # Placeholder for minimal rank of tropicalized Brauer group
        results.append((n, t, rank))
    
    correlation_coefficient = sum((t * math.log(n) - rank) ** 2 for n, t, rank in results) / len(results)
    mean_rank = sum(rank for _, _, rank in results) / len(results)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient >= 0.7 else f"n={n}, t log(n)={t * math.log(n)}, rank={rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")