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
            submatrix = [[matrix[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += (-1) ** j * matrix[0][j] * matrix_det(submatrix)
        return det
    
    def free_entropy(P):
        n = len(P)
        eigenvalues = [matrix_det([[P[i][j] if (i != k and j != l) else 1 - P[i][j] for j in range(n)] for k in range(n)]) for i in range(n)]
        return sum(math.log(abs(eig)) for eig in eigenvalues)
    
    n = 40
    P = [[random.random() for _ in range(n)] for _ in range(n)]
    chi_P = free_entropy(P)
    
    metric_name = "free_entropy"
    metric_value = chi_P
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if n == 40:
        expected_range = (math.sqrt(n) * math.log(n), math.sqrt(n) * math.log(n))
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
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        counterexample = "free_entropy_not_in_range"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")