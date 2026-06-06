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
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_matrix(f, n):
        matrix = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i ^ j] == f[i]:
                    matrix[i][j] = 1
        return matrix
    
    def rank_variance(matrix):
        n = len(matrix)
        total = sum(sum(row) for row in matrix)
        mean = total / (n * n)
        variance = sum((sum(row) - mean)**2 for row in matrix) / (n * n)
        return variance
    
    def formal_group_order(f, n):
        # Simplified version of computing the order of a formal group
        # This is a placeholder and should be replaced with actual computation
        return len(f)

    instances_tested = 0
    total_correlation = 0.0
    max_n = 0

    for n in [5, 10, 15, 20, 30, 40]:
        if n > max_n:
            max_n = n
        
        for _ in range(5):  # Sample 5 instances per size
            f = generate_boolean_function(n)
            matrix = communication_matrix(f, n)
            variance = rank_variance(matrix)
            order = formal_group_order(f, n)
            
            if variance == 0:
                continue
            
            correlation = abs(order / math.sqrt(variance))
            total_correlation += correlation
            instances_tested += 1

    mean_correlation = total_correlation / instances_tested if instances_tested > 0 else 0.0
    
    conjecture_holds = mean_correlation >= 0.8 and all(correlation >= -0.8 for _, correlation in zip(range(instances_tested), [abs(order / math.sqrt(variance)) for f, matrix, variance, order in [(generate_boolean_function(n), communication_matrix(generate_boolean_function(n), n), rank_variance(communication_matrix(generate_boolean_function(n), n)), formal_group_order(generate_boolean_function(n), n)) for _ in range(5) for n in [5, 10, 15, 20, 30, 40]]]))
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    
    return {
        "metric_name": "correlation",
        "metric_value": mean_correlation,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] and r["metric_value"] < 0.8 or not r["conjecture_holds"] and r["metric_value"] > -0.8 for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if r['conjecture_holds'] and r['metric_value'] < 0.8 or not r['conjecture_holds'] and r['metric_value'] > -0.8)}\" first_failing_seed={results.index(next(r for r in results if r['conjecture_holds'] and r['metric_value'] < 0.8 or not r['conjecture_holds'] and r['metric_value'] > -0.8))}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")