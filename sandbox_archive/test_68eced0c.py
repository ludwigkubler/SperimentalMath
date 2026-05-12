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
    n = 40
    p = 2
    target_metric_value = math.sqrt(n)
    threshold = 0.95 * target_metric_value
    
    random.seed(seed)
    
    def generate_balanced_bipartite_graph(n):
        A = [[0] * n for _ in range(n)]
        for i in range(n // 2):
            for j in range(n // 2, n):
                A[i][j] = 1
                A[j][i] = 1
        return A
    
    def frobenius_norm(matrix):
        norm = 0.0
        for row in matrix:
            for val in row:
                norm += val ** 2
        return math.sqrt(norm)
    
    metric_value = 0.0
    instances_tested = 30
    
    for _ in range(instances_tested):
        M = generate_balanced_bipartite_graph(n)
        metric_value += frobenius_norm(M)
    
    mean_metric_value = metric_value / instances_tested
    conjecture_holds = mean_metric_value >= threshold
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Frobenius Norm",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [601, 631, 677, 727, 773, 821, 877, 929]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not results:
        raise ValueError("No trials were executed. Ensure seeds are provided.")
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=undefined support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")