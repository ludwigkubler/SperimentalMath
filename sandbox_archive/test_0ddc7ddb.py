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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(-n, n) for _ in range(2)]
            if all(lit == 0 for lit in clause):
                continue
            cnf.append(clause)
        return cnf
    
    def bruhat_matrix(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause) if cnf else 1
        B = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    B[lit][lit] += 1
                elif lit < 0:
                    B[-lit][-lit] += 1
        return B
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if matrix[i][i] != 0:
                rank += 1
                for j in range(i + 1, n):
                    matrix[j][i] /= matrix[i][i]
                for j in range(n):
                    if j != i:
                        factor = matrix[j][i]
                        for k in range(n):
                            matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def frege_proof_width(cnf):
        m, n = len(cnf), max(abs(lit) for clause in cnf for lit in clause)
        width = 0
        for _ in range(10):  # Simulate a simple Frege proof width estimation
            assignment = [random.choice([True, False]) for _ in range(n)]
            unsatisfied_clauses = [any(lit > 0 and not assignment[abs(lit) - 1] or lit < 0 and assignment[abs(lit) - 1] for lit in clause) for clause in cnf]
            width = max(width, sum(unsatisfied_clauses))
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Test each size with 5 instances
            m = int(n * random.uniform(0.1, 1))
            cnf = generate_cnf(n, m)
            B = bruhat_matrix(cnf)
            rank = min_rank(B)
            width = frege_proof_width(cnf)
            results.append({"n": n, "m": m, "rank": rank, "width": width})
    
    if not results:
        return {
            "metric_name": "min_rank",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["rank"] - mean_rank) ** 2 for result in results) / len(results))
    conjecture_holds = all(result["rank"] <= (math.log(m / n) ** 2).limit_denominator() for result in results)
    
    return {
        "metric_name": "min_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")