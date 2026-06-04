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
    
    def communication_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[i][j] != 0 for j in range(n)):
                rank += 1
                for j in range(n):
                    matrix[j][i] /= matrix[i][i]
                for k in range(n):
                    if k != i:
                        factor = matrix[k][i]
                        for j in range(n):
                            matrix[k][j] -= factor * matrix[i][j]
        return rank
    
    def minimal_local_indeterminacy(matrix):
        n = len(matrix)
        indeterminacy = 0
        for i in range(n):
            for j in range(i+1, n):
                if all(matrix[i][k] == matrix[j][k] for k in range(n)):
                    indeterminacy += 1
        return indeterminacy
    
    def generate_boolean_function(n):
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_indeterminacy = 0
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            matrix = generate_boolean_function(n)
            indeterminacy = minimal_local_indeterminacy(matrix)
            rank = communication_rank(matrix)
            total_indeterminacy += indeterminacy
            total_rank += rank
            instances_tested += 1
    
    mean_indeterminacy = total_indeterminacy / instances_tested
    mean_rank = total_rank / instances_tested
    
    correlation_coefficient = (instances_tested * mean_indeterminacy * mean_rank - 
                               sum(ind * rank for ind, rank in zip(range(instances_tested), range(instances_tested)))) / \
                              math.sqrt((instances_tested * mean_indeterminacy**2 - sum(ind**2 for ind in range(instances_tested))) *
                                        (instances_tested * mean_rank**2 - sum(rank**2 for rank in range(instances_tested))))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100, 2))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")