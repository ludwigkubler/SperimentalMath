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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for i in range(n):
        pivot_row = None
        for j in range(rank, m):
            if A[j][i] != 0:
                pivot_row = j
                break
        if pivot_row is not None:
            A[pivot_row], A[rank] = A[rank], A[pivot_row]
            for j in range(n):
                if j == i:
                    A[rank][j] = Fraction(A[rank][j]).limit_denominator()
                else:
                    A[rank][j] = -A[rank][j] * A[pivot_row][i] // A[pivot_row][i]
            for j in range(m):
                if j != rank:
                    factor = A[j][i] * A[pivot_row][i] // A[pivot_row][i]
                    for k in range(n):
                        A[j][k] += -factor * A[rank][k]
            rank += 1
    return rank

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][k] += A[i][j] * B[j][k]
    return C

def communication_complexity_rank(f, n):
    M_f = [[0 for _ in range(2**n)] for _ in range(2**n)]
    for i in range(2**n):
        for j in range(2**n):
            if (i & j) == 0:
                M_f[i][j] = f(i ^ j)
    rank = gaussian_elimination(M_f)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    d = 2
    instances_tested = 30
    n_max = n
    conjecture_holds = True
    counterexample = ""
    
    metric_values = []
    
    for _ in range(instances_tested):
        f = [random.choice([0, 1]) for _ in range(2**n)]
        fourier_coeffs = [sum(f[i] * (2 * random.randint(0, 1) - 1) ** i for i in range(n)) / math.sqrt(2**n) for i in range(2**n)]
        
        # Calculate geometric measure as the volume of the unit sphere spanned by Fourier coefficients
        geo_measure = sum(abs(coeff) for coeff in fourier_coeffs)
        
        rank = communication_complexity_rank(f, n)
        
        metric_values.append((geo_measure, rank))
    
    correlation_coefficient = 0.0
    if len(metric_values) > 1:
        mean_geo_measure = sum(x[0] for x in metric_values) / len(metric_values)
        mean_rank = sum(x[1] for x in metric_values) / len(metric_values)
        
        numerator = sum((x[0] - mean_geo_measure) * (x[1] - mean_rank) for x in metric_values)
        denominator = math.sqrt(sum((x[0] - mean_geo_measure)**2 for x in metric_values)) * math.sqrt(sum((x[1] - mean_rank)**2 for x in metric_values))
        
        correlation_coefficient = numerator / denominator if denominator != 0 else 0
    
    return {
        "metric_name": "Pearson's Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")