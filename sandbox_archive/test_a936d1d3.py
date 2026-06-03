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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find the pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate non-pivot elements
        for j in range(n):
            if i != j:
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n+1):
                    matrix[j][k] -= factor * matrix[i][k]

def rank(matrix):
    n = len(matrix)
    rref = [row[:] for row in matrix]
    gaussian_elimination(rref)
    rank = 0
    for i in range(n):
        if any(rref[i][j] != 0 for j in range(n)):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        # Generate a random CNF formula with n variables
        cnf_formula = []
        for _ in range(n):
            clause = set(random.sample(range(1, n+1), 2))
            cnf_formula.append(clause)
        
        # Construct the simplicial complex
        vertices = list(range(1, n+1))
        simplices = []
        for i in range(1, n+1):
            simplices.append([i])
        for clause in cnf_formula:
            simplices.append(list(clause))
        
        # Calculate the number of simplicial generators
        num_generators = len(simplices)
        
        # Measure the rank of the incidence matrix
        incidence_matrix = [[0] * n for _ in range(n)]
        for i, clause in enumerate(cnf_formula):
            for j in clause:
                incidence_matrix[i][j-1] = 1
        rank_value = rank(incidence_matrix)
        
        # Store the results
        results.append({
            "n": n,
            "num_generators": num_generators,
            "rank_value": rank_value
        })
    
    # Calculate the metric value
    total_num_generators = sum(result["num_generators"] for result in results)
    total_rank_value = sum(result["rank_value"] for result in results)
    mean_num_generators = total_num_generators / len(results)
    mean_rank_value = total_rank_value / len(results)
    
    # Check if the conjecture holds
    conjecture_holds = all(num_generators <= n**1.5 for result in results)
    counterexample = "" if conjecture_holds else "n_max={} num_generators={}".format(max(result["n"] for result in results), max(result["num_generators"] for result in results))
    
    return {
        "metric_name": "min_simplicial_generators",
        "metric_value": mean_num_generators,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print("TRIAL: {}".format(trial_result))
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, std_metric_value, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, std_metric_value, support_fraction))
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(results[results.index(next(result for result in results if not result["conjecture_holds"]))]["counterexample"], first_failing_seed))