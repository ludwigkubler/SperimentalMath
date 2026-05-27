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
    
    def xor_and_tree_width(clauses):
        if not clauses:
            return 0
        max_depth = 1
        for clause in clauses:
            depth = 1
            for var in clause:
                if isinstance(var, list):
                    depth += xor_and_tree_width([v for v in var if v != []])
            max_depth = max(max_depth, depth)
        return max_depth
    
    def construct_quotient_group(clauses):
        elements = set()
        for clause in clauses:
            element = 0
            for var in clause:
                if isinstance(var, list):
                    element ^= construct_quotient_group([v for v in var if v != []])
                else:
                    element ^= var
            elements.add(element)
        return len(elements)
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i + 1, rows):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def min_rank_of_quotient_group(clauses):
        n = len(clauses)
        variables = set()
        for clause in clauses:
            for var in clause:
                if isinstance(var, list):
                    variables.update(var)
                else:
                    variables.add(var)
        num_vars = len(variables)
        
        matrix = [[0] * (num_vars + 1) for _ in range(n)]
        for i, clause in enumerate(clauses):
            for var in clause:
                if isinstance(var, list):
                    for v in var:
                        if v in variables:
                            j = list(variables).index(v)
                            matrix[i][j] += 1
                else:
                    if var in variables:
                        j = list(variables).index(var)
                        matrix[i][j] += 1
        
        return gaussian_elimination(matrix)
    
    def generate_random_boolean_function(w):
        clauses = []
        for _ in range(2 ** w):
            clause = [random.choice([0, 1]) for _ in range(w)]
            if any(clause):
                clauses.append(clause)
        return clauses
    
    n_min = 5
    n_max = 40
    instances_per_seed = 30
    total_instances = (n_max - n_min + 1) * instances_per_seed
    
    ranks = []
    for w in range(n_min, n_max + 1):
        for _ in range(instances_per_seed):
            clauses = generate_random_boolean_function(w)
            rank = min_rank_of_quotient_group(clauses)
            ranks.append((w, rank))
    
    mean_rank = sum(rank for _, rank in ranks) / len(ranks)
    std_rank = math.sqrt(sum((rank - mean_rank) ** 2 for _, rank in ranks) / len(ranks))
    support_fraction = sum(1 for _, rank in ranks if rank <= w * w * math.log2(w)) / len(ranks)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_rank_of_quotient_group",
        "metric_value": mean_rank,
        "instances_tested": total_instances,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")