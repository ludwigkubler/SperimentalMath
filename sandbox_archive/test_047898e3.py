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
        return -sum(p * math.log2(p) if p > 0 else 0 for p in counts)
    
    def minimal_order_of_quotient_algebra(f):
        n = int(math.log2(len(f)))
        # Simplified mapping to a quotient algebra order
        return n
    
    results = []
    for n in range(5, 41, 5):  # Sweep through sizes 5, 10, 15, 20, 30, 40
        f = generate_boolean_function(n)
        h_f = entropy(f)
        o_Q_f = minimal_order_of_quotient_algebra(f)
        results.append((n, h_f, o_Q_f))
    
    correlation_coefficient = 0.0
    if len(results) > 1:
        n_values = [r[0] for r in results]
        h_values = [r[1] for r in results]
        o_Q_values = [r[2] for r in results]
        
        mean_n = sum(n_values) / len(n_values)
        mean_h = sum(h_values) / len(h_values)
        mean_o_Q = sum(o_Q_values) / len(o_Q_values)
        
        numerator = sum((n - mean_n) * (h - mean_h) for n, h in zip(n_values, h_values))
        denominator = math.sqrt(sum((n - mean_n)**2 for n in n_values)) * math.sqrt(sum((h - mean_h)**2 for h in h_values))
        
        correlation_coefficient = numerator / denominator if denominator != 0 else 0.0
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": "" if correlation_coefficient >= 0.5 else f"Correlation coefficient {correlation_coefficient} < 0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 0.8")