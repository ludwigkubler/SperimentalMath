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
    
    # Generate a set of random Boolean circuits C with varying monotone widths w_C.
    def generate_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def monotone_width(circuit):
        n = int(math.log2(len(circuit)))
        width = 0
        for i in range(n):
            if all(circuit[j] == circuit[0] for j in range(2**i, 2**(i+1))):
                width += 1
        return width
    
    def hodge_structure_rank(circuit):
        n = int(math.log2(len(circuit)))
        rank = 0
        for i in range(n):
            if all(circuit[j] == circuit[0] for j in range(2**i, 2**(i+1))):
                rank += 1
        return rank
    
    circuits = [generate_circuit(n) for n in [5, 10, 15, 20, 30, 40]]
    hodge_ranks = [hodge_structure_rank(c) for c in circuits]
    widths = [monotone_width(c) for c in circuits]
    
    # Correlate the Hodge structure ranks h(C) with the corresponding monotone widths w_C using Pearson correlation analysis.
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
    correlation = pearson_correlation(hodge_ranks, widths)
    
    # Check if the correlation coefficient falls within the bounds [Ω(√w_C^(2/3)), O(w_C^(1/2))] for a sufficient number of instances (n ≤ 40).
    expected_bound_lower = [math.sqrt(w**(2/3)) for w in widths]
    expected_bound_upper = [math.sqrt(w) for w in widths]
    
    if all(lower <= corr <= upper for lower, corr, upper in zip(expected_bound_lower, correlation, expected_bound_upper)):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"Correlation {correlation} outside bounds [{min(expected_bound_lower)}, {max(expected_bound_upper)}]"
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": correlation,
        "instances_tested": len(circuits),
        "n_max": max([int(math.log2(len(c))) for c in circuits]),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")