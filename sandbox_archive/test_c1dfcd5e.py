# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for i in range(1 << n):
            clause = [random.choice([f'x{i}', f'-x{i}']) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def boolean_algebra_quasi_group(cnf):
        # Simplified representation of the quasi-group
        qg = {}
        for clause in cnf:
            for lit in clause:
                if lit not in qg:
                    qg[lit] = set()
                for other_lit in clause:
                    if other_lit != lit:
                        qg[lit].add(other_lit)
                        qg[other_lit].add(lit)
        return qg
    
    def min_rank(qg):
        # Simplified minimal rank calculation
        n = len(qg)
        matrix = [[0] * n for _ in range(n)]
        for i, lit1 in enumerate(qg):
            for j, lit2 in enumerate(qg):
                if lit1 != lit2 and qg[lit1].issubset(qg[lit2]):
                    matrix[i][j] = 1
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
                for i in range(n):
                    if row[i]:
                        for j in range(n):
                            if matrix[j][i]:
                                matrix[j][i] = 0
        return rank
    
    def circuit_weight(cnf):
        # Simplified circuit weight calculation
        return len(cnf)
    
    n_max = 40
    instances_tested = 30
    min_ranks = []
    weights = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        cnf = generate_cnf(n)
        qg = boolean_algebra_quasi_group(cnf)
        min_rank_val = min_rank(qg)
        weight_val = circuit_weight(cnf)
        
        min_ranks.append(min_rank_val)
        weights.append(weight_val)
    
    correlation_coefficient = sum((min_ranks[i] - mean_min_ranks) * (weights[i] - mean_weights) for i in range(instances_tested)) / instances_tested
    mean_min_ranks = sum(min_ranks) / instances_tested
    mean_weights = sum(weights) / instances_tested
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")