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
    
    def matrix_det(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * matrix_det(submatrix)
        return det
    
    def free_entropy(P):
        n = len(P)
        eigenvalues = [matrix_det([[P[i][j] if (i != k and j != l) else 1 - P[i][j] for j in range(n)] for k in range(n)]) for i in range(n)]
        chi_P = sum(math.log(abs(eig)) for eig in eigenvalues)
        return chi_P
    
    n = 40
    P = [[random.random() for _ in range(n)] for _ in range(n)]
    
    chi_P = free_entropy(P)
    
    metric_name = "free_entropy"
    metric_value = chi_P
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if n == 40:
        expected_range = (math.sqrt(40) * math.log(40), 2 * math.sqrt(40) * math.log(40))
        if expected_range[0] <= chi_P <= expected_range[1]:
            conjecture_holds = True
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = f"first failing seed {first_failing_seed}"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\"")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support_fraction")