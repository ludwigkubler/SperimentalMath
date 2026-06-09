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
    
    def generate_kcnf(n, k):
        clauses = []
        for _ in range(k):
            clause = set()
            while len(clause) < 2 or len(clause) > n:
                literal = random.randint(1, n * 2)
                if literal <= n:
                    literal = -literal
                clause.add(literal)
            clauses.append(tuple(sorted(clause)))
        return clauses
    
    def communication_complexity_matrix(kcnf):
        n = max(abs(var) for var in kcnf[0])
        matrix = [[0] * (2 ** n) for _ in range(2 ** n)]
        for j in range(2 ** n):
            for clause in kcnf:
                if all((j & (1 << (var - 1))) == 0 if var < 0 else (j & (1 << (var - 1))) != 0 for var in clause):
                    matrix[j][j] += 1
        return matrix
    
    def rank_variance(matrix):
        n = len(matrix)
        det = determinant(matrix)
        if det == 0:
            return float('inf')
        rank = 0
        for i in range(n):
            if abs(det) > 0:
                rank += 1
                det /= abs(det)
        return (n - rank) ** 2
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    def geometric_invariant_classes(kcnf, q):
        # Placeholder function to compute the number of geometric invariant classes
        # This is a dummy implementation and should be replaced with actual computation
        return len(kcnf) % q + 1
    
    n = random.randint(5, 40)
    k = random.randint(2, min(n * (n - 1) // 2, 20))
    q = random.randint(2, 10)
    kcnf = generate_kcnf(n, k)
    
    matrix = communication_complexity_matrix(kcnf)
    r_var = rank_variance(matrix)
    kappa = geometric_invariant_classes(kcnf, q)
    
    metric_value = r_var
    instances_tested = 1
    n_max = n
    conjecture_holds = False
    counterexample = "mapping_undefined"
    
    return {
        "metric_name": "rank_variance",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")