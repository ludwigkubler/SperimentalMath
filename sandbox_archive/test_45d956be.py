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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_quandle(n, r):
        quandle = []
        for i in range(r):
            row = [random.randint(0, n-1) for _ in range(n)]
            if all(row[j] != j for j in range(n)):
                quandle.append(row)
        return quandle
    
    def communication_complexity(quandle, n):
        complexity = 0
        for i in range(n):
            for j in range(i+1, n):
                if quandle[i][j] == quandle[j][i]:
                    continue
                complexity += 1
        return Fraction(complexity, n * (n - 1) // 2)
    
    def minimal_rank(quandle):
        r = len(quandle)
        for i in range(r):
            if any(quandle[i][j] == j for j in range(n)):
                return r
        return r
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_complexity = 0
    instances_tested = 0
    
    for n in n_values:
        quandle = generate_quandle(n, minimal_rank(generate_quandle(n, random.randint(1, n))))
        complexity = communication_complexity(quandle, n)
        total_complexity += complexity
        instances_tested += 1
    
    metric_value = total_complexity / instances_tested
    conjecture_holds = False
    counterexample = ""
    
    if metric_value > (n_values[-1]**2) / (2 * 0.5):
        conjecture_holds = True
    else:
        counterexample = f"Average complexity {metric_value} < {(n_values[-1]**2) / (2 * 0.5)}"
    
    return {
        "metric_name": "Randomized Communication Complexity",
        "metric_value": float(metric_value),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif any(r["metric_value"] > (n_values[-1]**2) / (2 * 0.5) for n_values, r in zip([n_values] * len(results), results)):
        first_failing_seed = next(i for i, r in enumerate(results) if r["metric_value"] > (n_values[-1]**2) / (2 * 0.5))
        print(f"RESULT: FALSIFIED counterexample='Average complexity {results[first_failing_seed]['metric_value']} < {(n_values[-1]**2) / (2 * 0.5)}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")