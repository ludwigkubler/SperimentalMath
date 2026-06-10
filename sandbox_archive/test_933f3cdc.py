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
    
    def dpll_solve(instance):
        n = len(instance)
        assignment = [False] * n
        
        def solve(lit_index):
            if lit_index == n:
                return True
            literal = instance[lit_index]
            pos_lit, neg_lit = abs(literal) - 1, abs(literal) - 1
            if literal > 0:
                pos_lit = literal - 1
            else:
                neg_lit = literal - 1
            
            if assignment[pos_lit]:
                return solve(lit_index + 1)
            elif not assignment[neg_lit]:
                assignment[pos_lit] = True
                if solve(lit_index + 1):
                    return True
                assignment[pos_lit] = False
                assignment[neg_lit] = True
                if solve(lit_index + 1):
                    return True
                assignment[neg_lit] = False
            else:
                return False
        
        return solve(0)
    
    def construct_vector_space(instance):
        n = len(instance)
        vector_space = []
        for i in range(n):
            vector = [0] * n
            if instance[i] > 0:
                vector[instance[i] - 1] = 1
            else:
                vector[-instance[i] - 1] = 1
            vector_space.append(vector)
        return vector_space
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return None
            for j in range(i + 1, n):
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def rank(vector_space):
        m = len(vector_space)
        n = len(vector_space[0])
        augmented_matrix = [row + [1 if i == j else 0 for j in range(m)] for i, row in enumerate(vector_space)]
        reduced_matrix = gaussian_elimination(augmented_matrix)
        if reduced_matrix is None:
            return m
        rank = sum(1 for row in reduced_matrix if any(x != 0 for x in row))
        return rank
    
    def k_group_order(vector_space):
        r = rank(vector_space)
        order = 2 ** (n - r)
        return order
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        instance = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        vector_space = construct_vector_space(instance)
        if not dpll_solve(instance):
            continue
        order = k_group_order(vector_space)
        metric_values.append(order)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    conjecture_holds = all(0.5 * mean_value <= val <= 2 * mean_value for val in metric_values)
    
    return {
        "metric_name": "K-group order",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")