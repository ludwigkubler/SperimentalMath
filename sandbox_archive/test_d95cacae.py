# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def rank(matrix):
        n = len(matrix)
        rref = gaussian_elimination(matrix)
        rank = 0
        for row in rref:
            if any(row):
                rank += 1
        return rank
    
    def matrix_multiplication(A, B):
        m = len(A)
        p = len(B[0])
        result = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(len(B)):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def generate_communication_complexity_instance(n, m):
        phi = [[random.randint(0, 1) for _ in range(m)] for _ in range(n)]
        return phi

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_min_order_KM = 0
        total_O_phi = 0
        
        for _ in range(5):  # Ensure at least 30 instances per seed
            phi = generate_communication_complexity_instance(n, n)
            O_phi = sum(sum(row) for row in phi)
            min_order_KM = rank(phi)
            
            total_min_order_KM += min_order_KM
            total_O_phi += O_phi
            instances_tested += 1
        
        if instances_tested < 30:
            return {
                "metric_name": "min_order_KM vs O_phi",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "insufficient_instances"
            }
        
        mean_min_order_KM = total_min_order_KM / instances_tested
        mean_O_phi = total_O_phi / instances_tested
        
        results.append({
            "n": n,
            "mean_min_order_KM": mean_min_order_KM,
            "mean_O_phi": mean_O_phi
        })
    
    correlation_coefficient = 0
    for result in results:
        correlation_coefficient += (result["mean_min_order_KM"] - mean_min_order_KM) * (result["mean_O_phi"] - mean_O_phi)
    correlation_coefficient /= len(results) * math.sqrt(sum((x["mean_min_order_KM"] - mean_min_order_KM) ** 2 for x in results)) * math.sqrt(sum((x["mean_O_phi"] - mean_O_phi) ** 2 for x in results))
    
    return {
        "metric_name": "min_order_KM vs O_phi",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(correlation_coefficient) > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(x["metric_value"] for x in results) / len(results)
    std_metric_value = math.sqrt(sum((x["metric_value"] - mean_metric_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")