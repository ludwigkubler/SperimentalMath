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
    
    def generate_boolean_function(n):
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def compute_minimal_rank(f):
        n = len(f)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            A[i][i] = 1
            A[n][i] = f[i]
        
        rank = 0
        for j in range(n + 1):
            if all(A[j][k] == 0 for k in range(j, n + 1)):
                continue
            pivot_col = next(k for k in range(j, n + 1) if A[j][k] != 0)
            rank += 1
            for i in range(n + 1):
                if i == j:
                    continue
                factor = -A[i][pivot_col] / A[j][pivot_col]
                for k in range(n + 1):
                    A[i][k] += factor * A[j][k]
        
        return rank
    
    def communication_complexity_XOR(f):
        n = len(f)
        count = sum(1 for i in range(2**n) if f[i ^ (i >> 1)] == 0)
        return Fraction(count, 2**(n - 1))
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    complexities = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        rank = compute_minimal_rank(f)
        complexity = communication_complexity_XOR(f)
        
        ranks.append(rank)
        complexities.append(complexity)
    
    correlation_coefficient = sum((ranks[i] - sum(ranks) / len(ranks)) * (complexities[i] - sum(complexities) / len(complexities)) for i in range(len(ranks))) / (len(ranks) * math.sqrt(sum((ranks[i] - sum(ranks) / len(ranks))**2 for i in range(len(ranks)))) * math.sqrt(sum((complexities[i] - sum(complexities) / len(complexities))**2 for i in range(len(complexities)))))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient >= 0.7 else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 29 primes
    
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
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")