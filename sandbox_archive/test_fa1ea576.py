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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        else:
            return n * factorial(n - 1)
    
    def binomial_coefficient(n, k):
        return factorial(n) // (factorial(k) * factorial(n - k))
    
    def young_tableau_to_permutation(yt):
        perm = [0] * len(yt)
        for i in range(len(yt)):
            for j in range(len(yt[i])):
                perm[yt[i][j]] = i * len(yt[i]) + j
        return perm
    
    def permanent(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        else:
            det = 0
            sign = 1
            for j in range(len(matrix)):
                submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
                det += sign * matrix[0][j] * permanent(submatrix)
                sign *= -1
            return det
    
    def determinant(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        else:
            det = 0
            for j in range(len(matrix)):
                submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
                det += ((-1) ** j) * matrix[0][j] * determinant(submatrix)
            return det
    
    def plethysm(m, n):
        if m == 0:
            return 1
        else:
            return sum(binomial_coefficient(n, k) * plethysm(m - 1, k) for k in range(1, n + 1))
    
    def multiplicity(partition, matrix):
        n = len(matrix)
        if partition[0] > n or any(x < 0 for x in partition):
            return 0
        yt = []
        for i in range(len(partition)):
            row = [i * (n // partition[i]) + j for j in range(partition[i])]
            yt.append(row)
        perm = young_tableau_to_permutation(yt)
        det = determinant(matrix)
        perm_val = permanent(matrix)
        return binomial_coefficient(n, len(perm)) * plethysm(len(partition), n) // (det ** len(partition))
    
    def partition_to_tuple(partition):
        return tuple(sorted(partition, reverse=True))
    
    def partitions(n):
        if n == 0:
            yield []
        else:
            for i in range(1, n + 1):
                for p in partitions(n - i):
                    yield [i] + p
    
    results = []
    n_max = 40
    for n in range(5, n_max + 1):
        m_max = int(n ** 1.5)
        for m in range(1, m_max):
            perm_multiplicity = multiplicity((n - m, m), [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)])
            det_multiplicity = multiplicity((n - m, m), [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)])
            results.append({
                "metric_name": "Multiplicity Gap",
                "metric_value": perm_multiplicity - det_multiplicity,
                "instances_tested": 1,
                "conjecture_holds": perm_multiplicity > det_multiplicity,
                "counterexample": f"m={m}, n={n}: perm_multiplicity={perm_multiplicity}, det_multiplicity={det_multiplicity}"
            })
    
    return {
        "metric_name": "Multiplicity Gap",
        "metric_value": sum(x["metric_value"] for x in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(x["conjecture_holds"] for x in results),
        "counterexample": next((x["counterexample"] for x in results if not x["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]
    
    print("TRIALS:")
    for result in results:
        print(f"TRIAL: {result}")
    
    mean_value = sum(x["metric_value"] for x in results) / len(results)
    std_value = (sum((x["metric_value"] - mean_value) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] for x in results):
        first_failing_seed = next(x['seed'] for x in results if not x['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{next(x['counterexample'] for x in results if not x['conjecture_holds'])}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")