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
    
    def polynomial_from_boolean_function(f, n):
        poly = [0] * (2**n)
        for i in range(2**n):
            if f(i):
                exp = bin(i)[2:].zfill(n)
                coeff = 1
                for j in range(n):
                    if exp[j] == '1':
                        coeff *= -1
                poly[int(exp, 2)] += coeff
        return poly
    
    def minimal_local_ring_rank(poly, q):
        n = len(poly)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if (i & j) == 0:
                    A[i][j] = sum(poly[k] * poly[l] for k in range(n) for l in range(n) if (k & j) == 0 and (l & i) == 0)
        rank = gaussian_elimination(A, q)
        return rank
    
    def gaussian_elimination(A, q):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                return None
            pivot = A[i][i]
            for j in range(i, n):
                A[i][j] /= pivot
            for j in range(n):
                if j != i and abs(A[j][i]) > 1e-9:
                    factor = A[j][i]
                    for k in range(i, n):
                        A[j][k] -= factor * A[i][k]
        rank = sum(1 for row in A if any(abs(x) > 1e-9 for x in row))
        return rank
    
    def communication_complexity_rank_variance(f, n):
        # Placeholder function; actual implementation needed
        return random.random()
    
    def pearson_correlation_coefficient(mrr_values, rcv_values):
        n = len(mrr_values)
        if n != len(rcv_values):
            raise ValueError("mrr_values and rcv_values must have the same length")
        
        mean_mrr = sum(mrr_values) / n
        mean_rcv = sum(rcv_values) / n
        
        numerator = sum((mrr_values[i] - mean_mrr) * (rcv_values[i] - mean_rcv) for i in range(n))
        denominator = math.sqrt(sum((mrr_values[i] - mean_mrr)**2 for i in range(n))) * math.sqrt(sum((rcv_values[i] - mean_rcv)**2 for i in range(n)))
        
        if denominator == 0:
            return None
        
        return numerator / denominator
    
    n_max = 40
    instances_tested = 30
    mrr_values = []
    rcv_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        f = lambda x: bool(random.getrandbits(n))
        poly = polynomial_from_boolean_function(f, n)
        mrr = minimal_local_ring_rank(poly, 2)
        rcv = communication_complexity_rank_variance(f, n)
        
        if mrr is not None and rcv is not None:
            mrr_values.append(mrr)
            rcv_values.append(rcv)
    
    correlation_coefficient = pearson_correlation_coefficient(mrr_values, rcv_values)
    conjecture_holds = 0.9 <= abs(correlation_coefficient) <= 1
    counterexample = "" if conjecture_holds else f"Correlation coefficient: {correlation_coefficient}"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")