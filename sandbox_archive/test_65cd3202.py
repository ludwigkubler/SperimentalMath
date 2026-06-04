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
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def communication_complexity_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[j][i] == 1 for j in range(n)):
                rank += 1
        return rank
    
    def minimal_local_indeterminacy(matrix):
        n = len(matrix)
        indeterminacy = 0
        for i in range(n):
            for j in range(i + 1, n):
                if matrix[i][j] == 1 and matrix[j][i] == 1:
                    indeterminacy += 1
        return indeterminacy
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_indeterminacy = 0
    total_rank = 0
    
    for n in n_values:
        for _ in range(5):
            matrix = generate_boolean_function(n)
            indeterminacy = minimal_local_indeterminacy(matrix)
            rank = communication_complexity_rank(matrix)
            instances_tested += 1
            total_indeterminacy += indeterminacy
            total_rank += rank
    
    mean_indeterminacy = total_indeterminacy / instances_tested
    mean_rank = total_rank / instances_tested
    
    correlation_coefficient = (instances_tested * sum(ind * r for ind, r in zip(total_indeterminacy, total_rank)) -
                               total_indeterminacy * total_rank) / math.sqrt(
        (instances_tested * sum(ind**2 for ind in total_indeterminacy) - total_indeterminacy**2) *
        (instances_tested * sum(r**2 for r in total_rank) - total_rank**2))
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.4f}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_dev:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")