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
        for _ in range(2**n - 1):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) == 0:
                continue
            clauses.append(clause)
        return clauses
    
    def boolean_algebra_quasi_group(cnf):
        n = len(cnf[0])
        quasi_group = {}
        for clause in cnf:
            for x in range(1 << n):
                if all((x & (1 << abs(l) - 1)) == l * sign for l, sign in enumerate(clause)):
                    for y in range(1 << n):
                        if all((y & (1 << abs(l) - 1)) == l * sign for l, sign in enumerate(clause)):
                            result = x ^ y
                            if result not in quasi_group:
                                quasi_group[result] = set()
                            quasi_group[result].add(x)
                            quasi_group[result].add(y)
        return quasi_group
    
    def min_rank(quasi_group):
        n = len(quasi_group)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for i, x in enumerate(quasi_group):
            for y in quasi_group:
                if y in quasi_group[x]:
                    adjacency_matrix[i][quasi_group.index(y)] = 1
        
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            rank = 0
            for i in range(cols):
                pivot_row = -1
                for j in range(rank, rows):
                    if matrix[j][i] != 0:
                        pivot_row = j
                        break
                if pivot_row == -1:
                    continue
                
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                rank += 1
                
                for j in range(rows):
                    if j != rank - 1:
                        factor = matrix[j][i] / matrix[rank - 1][i]
                        for k in range(cols):
                            matrix[j][k] -= factor * matrix[rank - 1][k]
            return rank
        
        return gaussian_elimination(adjacency_matrix)
    
    def circuit_weight(cnf):
        return len(cnf) + sum(len(clause) - 1 for clause in cnf if len(set(abs(l) for l in clause)) > 1)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        quasi_group = boolean_algebra_quasi_group(cnf)
        min_rank_value = min_rank(quasi_group)
        circuit_weight_value = circuit_weight(cnf)
        results.append((min_rank_value, circuit_weight_value))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    min_rank_values, circuit_weight_values = zip(*results)
    mean_min_rank = sum(min_rank_values) / len(min_rank_values)
    mean_circuit_weight = sum(circuit_weight_values) / len(circuit_weight_values)
    correlation_coefficient = (sum((x - mean_min_rank) * (y - mean_circuit_weight) for x, y in zip(min_rank_values, circuit_weight_values)) /
                               math.sqrt(sum((x - mean_min_rank)**2 for x in min_rank_values) *
                                         sum((y - mean_circuit_weight)**2 for y in circuit_weight_values)))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_less_than_0.8\" first_failing_seed={seeds[first_failing_seed]}")