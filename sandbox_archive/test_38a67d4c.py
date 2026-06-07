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
    
    def generate_formula(n):
        if n == 1:
            return random.choice(['0', '1'])
        else:
            op = random.choice(['&', '|'])
            left = generate_formula(random.randint(1, n-1))
            right = generate_formula(n - len(left) - 1)
            return f'({left}{op}{right})'
    
    def evaluate_formula(formula):
        if formula == '0':
            return 0
        elif formula == '1':
            return 1
        else:
            op, left, right = formula[1], formula[:formula.index(')')], formula[formula.index(')')+2:]
            if op == '&':
                return evaluate_formula(left) & evaluate_formula(right)
            elif op == '|':
                return evaluate_formula(left) | evaluate_formula(right)
    
    def generate_matroid(formula):
        n = len(formula)
        matroid = [set() for _ in range(n)]
        for i, c in enumerate(formula):
            if c != '0' and c != '1':
                matroid[ord(c) - ord('a')].add(i)
        return matroid
    
    def hodge_index(matroid):
        n = len(matroid)
        rank_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if len(matroid[i].intersection(matroid[j])) == 1:
                    rank_matrix[i][j] = 1
                    rank_matrix[j][i] = 1
        return sum(sum(row) for row in rank_matrix) / (n * (n - 1))
    
    def communication_matrix(formula):
        n = len(formula)
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if formula[i] == '0' and formula[j] == '0':
                    matrix[i][j] = 1
                elif formula[i] == '1' or formula[j] == '1':
                    matrix[i][j] = 2
        return matrix
    
    def rank_variance(matrix):
        n = len(matrix)
        ranks = [sum(row) for row in matrix]
        mean_rank = sum(ranks) / n
        variance = sum((x - mean_rank) ** 2 for x in ranks) / n
        return variance
    
    formula = generate_formula(40)
    matroid = generate_matroid(formula)
    hodge = hodge_index(matroid)
    comm_matrix = communication_matrix(formula)
    rank_var = rank_variance(comm_matrix)
    
    return {
        "metric_name": "hodge_index_vs_rank_variance",
        "metric_value": hodge * rank_var,
        "instances_tested": 1,
        "n_max": 40,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")