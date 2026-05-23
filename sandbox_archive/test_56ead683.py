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
    
    def generate_random_function(n):
        return {tuple(random.randint(0, 1) for _ in range(n)): random.choice([0, 1]) for _ in range(2**n)}
    
    def matrix_multiplication(A, B):
        result = [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
        return result
    
    def trace(matrix):
        return sum(matrix[i][i] for i in range(len(matrix)))
    
    def l_p_geometric_entropy(f, p):
        n = len(next(iter(f.keys())))
        matrix = [[0] * (2**n) for _ in range(2**n)]
        for x, y in f.items():
            index = sum(x[i] * (2 ** i) for i in range(n))
            matrix[index][index + y] += 1
        for row in matrix:
            total = sum(row)
            if total > 0:
                for j in range(len(row)):
                    row[j] /= total
        return trace(matrix) ** (1/p)
    
    def communication_complexity(f):
        n = len(next(iter(f.keys())))
        p_values = [i / 10.0 for i in range(1, 11)]
        entropies = [l_p_geometric_entropy(f, p) for p in p_values]
        return max(entropies)
    
    def check_disjointness(n):
        f = {}
        for x in range(2**n):
            y = random.randint(0, 1)
            f[tuple((x >> i) & 1 for i in range(n))] = y
        return communication_complexity(f)
    
    n_values = [5, 10, 15, 20, 30, 40]
    entropies = []
    instances_tested = 0
    
    for n in n_values:
        for _ in range(10):
            f = generate_random_function(n)
            entropy = communication_complexity(f)
            entropies.append((n, entropy))
            instances_tested += 1
    
    mean_entropy = sum(entropy for _, entropy in entropies) / len(entropies)
    std_entropy = math.sqrt(sum((entropy - mean_entropy) ** 2 for _, entropy in entropies) / len(entropies))
    
    conjecture_holds = all(n ** (1 - p / (p + 1)) <= entropy for n, entropy in entropies for p in [i / 10.0 for i in range(1, 11)])
    counterexample = "" if conjecture_holds else "disjointness"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_entropy,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_entropy = sum(result["metric_value"] for result in results) / len(results)
    std_entropy = math.sqrt(sum((result["metric_value"] - mean_entropy) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    elif any(result["counterexample"] == "disjointness" for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if result["counterexample"] == "disjointness")
        print(f"RESULT: FALSIFIED counterexample=\"disjointness\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")