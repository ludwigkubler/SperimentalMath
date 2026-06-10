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
    
    def frobenius_norm(matrix):
        sum_of_squares = 0
        for row in matrix:
            for elem in row:
                sum_of_squares += elem ** 2
        return math.sqrt(sum_of_squares)
    
    def generate_matrix(n):
        matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return matrix
    
    def rank_variance(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if sum(matrix[i]) > 0:
                rank += 1
        return rank / n
    
    instances_tested = 0
    total_frobenius_norm = 0.0
    total_rank_variance = 0.0
    n_max = 0
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        if n > n_max:
            n_max = n
        
        matrix = generate_matrix(n)
        rank_var = rank_variance(matrix)
        frob_norm = frobenius_norm(matrix)
        
        total_frobenius_norm += frob_norm
        total_rank_variance += rank_var
        instances_tested += 1
    
    mean_frob_norm = total_frobenius_norm / instances_tested
    mean_rank_variance = total_rank_variance / instances_tested
    ratio = mean_frob_norm / mean_rank_variance
    
    conjecture_holds = ratio > 0.9
    counterexample = "Frobenius norm not proportional to rank variance" if not conjecture_holds else ""
    
    return {
        "metric_name": "Ratio of Mean Frobenius Norm to Rank Variance",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_ratio) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")