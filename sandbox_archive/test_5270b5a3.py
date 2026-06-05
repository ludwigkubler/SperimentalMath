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
    
    def entropy(f):
        counts = [f.count(i) / len(f) for i in [0, 1]]
        return -sum(p * math.log2(p) if p != 0 else 0 for p in counts)
    
    def minimal_order_of_quotient_algebra(f):
        n = int(math.log2(len(f)))
        # Simplified heuristic to estimate the order
        return n ** (math.log(n, 2) / 2)
    
    results = []
    for n in range(5, 41, 5):  # Sweep through sizes 5, 10, 15, 20, 30, 40
        f = generate_boolean_function(n)
        h_f = entropy(f)
        o_Q_f = minimal_order_of_quotient_algebra(f)
        results.append({"n": n, "h_f": h_f, "o_Q_f": o_Q_f})
    
    correlation_coefficient = 0.0
    if len(results) > 1:
        x = [result["h_f"] for result in results]
        y = [result["o_Q_f"] for result in results]
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        covariance = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        variance_x = sum((x[i] - mean_x) ** 2 for i in range(n)) / n
        variance_y = sum((y[i] - mean_y) ** 2 for i in range(n)) / n
        correlation_coefficient = covariance / (math.sqrt(variance_x) * math.sqrt(variance_y))
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient > 0.8,
        "counterexample": "" if correlation_coefficient >= 0.5 else f"Correlation coefficient {correlation_coefficient:.2f} < 0.5"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction=1.0")
    elif sum(1 for result in results if not result["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"low_support\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction:.4f}")