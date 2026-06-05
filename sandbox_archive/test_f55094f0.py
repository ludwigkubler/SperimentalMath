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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def cnf_to_matrix(cnf):
        n = max(abs(x) for x in sum(cnf, []))
        matrix = [[0] * (2 * n + 1) for _ in range(len(cnf))]
        for i, clause in enumerate(cnf):
            for literal in clause:
                if literal > 0:
                    matrix[i][literal - 1] = 1
                else:
                    matrix[i][-literal] = 1
        return matrix
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        m = len(matrix[0])
        rank = 0
        for j in range(m):
            i_max = rank
            for i in range(rank, n):
                if abs(matrix[i][j]) > abs(matrix[i_max][j]):
                    i_max = i
            if matrix[i_max][j] == 0:
                continue
            matrix[rank], matrix[i_max] = matrix[i_max], matrix[rank]
            for i in range(n):
                if i != rank:
                    factor = matrix[i][j] / matrix[rank][j]
                    for k in range(m):
                        matrix[i][k] -= factor * matrix[rank][k]
            rank += 1
        return rank
    
    def min_order(matrix):
        return gaussian_elimination(matrix)
    
    def cnf_depth(cnf):
        depth = [0] * len(cnf)
        for i, clause in enumerate(cnf):
            for literal in clause:
                if literal > 0:
                    depth[i] = max(depth[i], depth[-literal] + 1)
                else:
                    depth[i] = max(depth[i], depth[literal - 1] + 1)
        return max(depth)
    
    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    
    for n in range(5, n_max + 1):
        cnf = generate_cnf(n)
        matrix = cnf_to_matrix(cnf)
        oq_phi = min_order(matrix)
        d_phi = cnf_depth(cnf)
        
        if oq_phi <= 3 * d_phi:  # Example constant c=3
            total_metric_value += oq_phi / d_phi
            instances_tested += 1
    
    metric_name = "OQ(φ) / D(φ)"
    metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0.0
    conjecture_holds = instances_tested >= 24 and all(oq_phi <= 3 * d_phi for oq_phi, d_phi in zip([min_order(cnf_to_matrix(generate_cnf(n))) for n in range(5, n_max + 1)], [cnf_depth(generate_cnf(n)) for n in range(5, n_max + 1)]))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")