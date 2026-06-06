# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_matrix(f):
        n = len(f)
        matrix = [[0] * (2**(n-1)) for _ in range(2**(n-1))]
        for i in range(2**(n-1)):
            for j in range(2**(n-1)):
                input1 = [i >> k & 1 for k in range(n)]
                input2 = [j >> k & 1 for k in range(n)]
                output1 = f[input1.index(0) * 2 + input1.index(1)]
                output2 = f[input2.index(0) * 2 + input2.index(1)]
                matrix[i][j] = (output1, output2)
        return matrix
    
    def rank_variance(matrix):
        n = len(matrix)
        total = sum(sum(row) for row in matrix)
        mean = Fraction(total, n**2)
        variance = sum((sum(row) - mean)**2 for row in matrix) / n
        return variance
    
    def formal_group_order(f):
        # Placeholder for actual implementation of formal group order calculation
        return len(f)

    instances_tested = 0
    total_correlation = 0.0
    max_n = 1

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            f = generate_boolean_function(n)
            matrix = communication_matrix(f)
            variance = rank_variance(matrix)
            order = formal_group_order(f)
            if order == 0:
                continue
            correlation = Fraction(variance * order).limit_denominator()
            total_correlation += correlation
            instances_tested += 1
            max_n = max(max_n, n)

    mean_correlation = total_correlation / instances_tested if instances_tested > 0 else 0
    conjecture_holds = -0.8 <= mean_correlation <= 0.8

    return {
        "metric_name": "correlation",
        "metric_value": float(mean_correlation),
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results)).sqrt() if len(results) > 1 else 0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] < -0.8 or r["metric_value"] > 0.8 for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not (-0.8 <= r["metric_value"] <= 0.8))
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")