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
    
    n = random.randint(2, 40)
    k = random.randint(1, min(n // 2, 30))
    
    def generate_permutation_matrix(n):
        perm = list(range(n))
        random.shuffle(perm)
        return [[int(i == j) for j in range(n)] for i in perm]
    
    def generate_determinant_matrix(n):
        det = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                det[i][j] = random.choice([-1, 1])
                det[j][i] = -det[i][j]
        return det
    
    def symmetric_power(matrix, k):
        result = matrix
        for _ in range(k - 1):
            result = [[sum(result[i][k] * matrix[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
        return result
    
    def multiplicity_of_trivial_representation(matrix):
        eigenvalues = []
        for _ in range(20):  # Power iteration method
            v = [random.random() for _ in range(n)]
            v /= math.sqrt(sum(x * x for x in v))
            for _ in range(100):
                v = [sum(matrix[i][j] * v[j] for j in range(n)) for i in range(n)]
                v /= math.sqrt(sum(x * x for x in v))
            eigenvalues.append(v[0])
        return sum(1 for e in eigenvalues if abs(e) < 1e-6)
    
    perm_matrix = generate_permutation_matrix(n)
    det_matrix = generate_determinant_matrix(n)
    
    perm_multiplicity = multiplicity_of_trivial_representation(symmetric_power(perm_matrix, k))
    det_multiplicity = multiplicity_of_trivial_representation(symmetric_power(det_matrix, k))
    
    metric_value = perm_multiplicity - det_multiplicity
    conjecture_holds = metric_value > math.sqrt(n) / 2
    
    return {
        "metric_name": "Multiplicity Gap",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "n={}, k={}".format(n, k)
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, std_metric_value, support_fraction))
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(results[first_failing_seed]["counterexample"], first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")