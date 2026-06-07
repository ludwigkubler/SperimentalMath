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
    
    def matrix_representation(f, n):
        S = [(i,) for i in range(2**n)]
        M = [[f(S[i]) == f(S[j]) for j in range(2**n)] for i in range(2**n)]
        return M
    
    def geometric_fluctuation(M):
        n = int(math.log2(len(M)))
        if len(M) != 2**n:
            raise ValueError("Matrix must be square")
        
        # Calculate the number of edges
        num_edges = 0
        for i in range(2**n):
            for j in range(i+1, 2**n):
                if M[i][j] != M[j][i]:
                    num_edges += 1
        
        # Calculate the total number of possible edges
        total_edges = (2**n) * (2**n - 1) // 2
        
        return num_edges / total_edges
    
    def rank(matrix):
        n = len(matrix)
        A = [row[:] for row in matrix]
        
        # Gaussian elimination
        for i in range(n):
            if A[i][i] == 0:
                for j in range(i+1, n):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]
                        break
                else:
                    return sum(1 for row in A if any(x != 0 for x in row))
            
            for j in range(n):
                if j == i:
                    continue
                factor = -A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
        
        return sum(1 for row in A if any(x != 0 for x in row))
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_gf = 0.0
    total_rank = 0.0
    
    for n in n_values:
        for _ in range(5):
            f = lambda x: random.choice([0, 1])
            M = matrix_representation(f, n)
            gf = geometric_fluctuation(M)
            r = rank(M)
            
            instances_tested += 1
            total_gf += gf
            total_rank += r
    
    mean_gf = total_gf / instances_tested
    mean_rank = total_rank / instances_tested
    correlation_coefficient = (instances_tested * total_gf * total_rank - sum(gf * r for gf, r in zip([mean_gf] * instances_tested, [mean_rank] * instances_tested))) / math.sqrt((instances_tested * total_gf**2 - mean_gf**2) * (instances_tested * total_rank**2 - mean_rank**2))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.9,
        "counterexample": "" if correlation_coefficient > 0.9 else "correlation_coefficient < 0.9"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and any(result["metric_value"] < 0.5 or result["counterexample"] == "correlation_coefficient < 0.9" for result in results):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.9\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_or_other_reasons")