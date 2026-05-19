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
    M_n = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def is_disjointness_matrix(M):
        for i in range(n):
            if not all(M[i][j] == M[j][i] or (M[i][j] + M[j][i] == 1) for j in range(i+1, n)):
                return False
        return True
    
    if not is_disjointness_matrix(M_n):
        return {
            "metric_name": "secant_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "not_a_disjointness_matrix"
        }
    
    def secant_rank(matrix):
        n = len(matrix)
        minors = []
        
        def determinant(submatrix):
            if len(submatrix) == 1:
                return submatrix[0][0]
            det = 0
            for j in range(len(submatrix)):
                minor = [row[:j] + row[j+1:] for row in submatrix[1:]]
                det += (-1)**j * submatrix[0][j] * determinant(minor)
            return det
        
        def get_minors(matrix, k):
            if k == 1:
                for i in range(n):
                    for j in range(n):
                        minors.append([[matrix[i][j]]])
            else:
                for i in range(n):
                    submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
                    get_minors(submatrix, k-1)
        
        get_minors(matrix, n)
        
        return len(minors) - sum(1 for minor in minors if determinant(minor) == 0)
    
    sr_M_n = secant_rank(M_n)
    
    return {
        "metric_name": "secant_rank",
        "metric_value": sr_M_n,
        "instances_tested": 1,
        "conjecture_holds": sr_M_n >= 0.8 * n,
        "counterexample": "" if sr_M_n >= 0.8 * n else f"sr(M_{n}) = {sr_M_n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_data")