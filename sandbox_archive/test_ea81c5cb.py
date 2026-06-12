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
    
    def generate_boolean_function(n):
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def vector_space_representation(f):
        n = int(math.log2(len(f)))
        V_f = []
        for i in range(2**n):
            v = [f[i ^ (1 << j)] for j in range(n)]
            V_f.append(v)
        return V_f
    
    def symplectic_measure(V_f):
        n = len(V_f[0])
        B = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                sum_product = sum((V_f[k][i] * V_f[k][j]) for k in range(len(V_f)))
                B[i][j] = sum_product
                B[j][i] = sum_product
        det_B = determinant(B)
        return abs(det_B) ** (1 / n)
    
    def determinant(matrix):
        if len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        det = 0
        for j in range(len(matrix)):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += ((-1) ** j) * matrix[0][j] * determinant(submatrix)
        return det
    
    def circuit_size(f):
        n = int(math.log2(len(f)))
        dsop_form = []
        for i in range(n):
            for j in range(i, n):
                if f[i ^ (1 << j)] != f[i]:
                    dsop_form.append((i, j))
        return len(dsop_form)
    
    correlation_coefficient = 0
    instances_tested = 0
    n_max = 0
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        V_f = vector_space_representation(f)
        sigma_f = symplectic_measure(V_f)
        s_f = circuit_size(f)
        
        if n > n_max:
            n_max = n
        
        correlation_coefficient += sigma_f * s_f
        instances_tested += 1
    
    correlation_coefficient /= instances_tested
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient >= 0.7 else "low_correlation"
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='low_correlation' first_failing_seed={first_failing_seed}")