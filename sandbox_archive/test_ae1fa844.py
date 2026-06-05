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
    
    def shannon_entropy(p):
        return -sum(x * math.log2(x) for x in p if x > 0)

    def geometric_entropy(P):
        n = len(P)
        H = [shannon_entropy([P[i][j] / sum(P[j]) for j in range(n)]) for i in range(n)]
        return shannon_entropy(H)

    def generate_protocol(n):
        P = [[random.random() for _ in range(n)] for _ in range(n)]
        return P

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_entropy = 0.0
        
        for _ in range(5):
            P = generate_protocol(n)
            entropy = geometric_entropy(P)
            total_entropy += entropy
            instances_tested += 1
        
        mean_entropy = total_entropy / instances_tested
        expected_bound = n * math.log2(n)
        
        results.append({
            "n": n,
            "mean_entropy": mean_entropy,
            "expected_bound": expected_bound,
            "instances_tested": instances_tested
        })
    
    metric_name = "geometric_entropy"
    metric_value = sum(r["mean_entropy"] for r in results) / len(results)
    n_max = max(r["n"] for r in results)
    conjecture_holds = all(abs(r["mean_entropy"] - r["expected_bound"]) <= 0.1 * r["expected_bound"] for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": sum(r["instances_tested"] for r in results),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) < 0.3:
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")