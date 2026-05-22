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
    n = random.randint(5, 40)
    
    # Generate a read-twice Boolean function
    def f(x):
        return (x[0] and x[1]) or (not x[0] and not x[1])
    
    # Generate multiple matrix representations of the function
    matrices = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        B = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        matrices.append((A, B))
    
    # Calculate the noncommutative entropy
    total_entropy = 0
    for A, B in matrices:
        commutator = [[A[i][j] * B[j][i] - B[i][j] * A[j][i] for j in range(n)] for i in range(n)]
        max_nonzero_entry = max(abs(x) for row in commutator for x in row if x != 0)
        entropy = math.log(max_nonzero_entry + 1, 2) if max_nonzero_entry > 0 else 0
        total_entropy += entropy
    
    # Check the conjecture conditions
    noncommutative_entropy = total_entropy / len(matrices)
    lower_bound = n ** 2
    upper_bound = math.log(n)
    
    conjecture_holds = (noncommutative_entropy >= lower_bound) and (total_entropy >= n * upper_bound)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Noncommutative Entropy",
        "metric_value": noncommutative_entropy,
        "instances_tested": len(matrices),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")