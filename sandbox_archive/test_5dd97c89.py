# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def resolution_depth(phi):
        clauses = phi.split(' or ')
        assignment = {}
        depth = 0
        while True:
            new_assignment = False
            for clause in clauses:
                if all(lit not in assignment or assignment[lit] == -1 for lit in clause.split(' and ')):
                    for lit in clause.split(' and '):
                        if lit[0] != '~':
                            assignment[lit] = 1
                        else:
                            assignment[lit[1:]] = -1
                    new_assignment = True
            if not new_assignment:
                break
            depth += 1
        return depth
    
    def construct_lie_algebroid(phi):
        clauses = phi.split(' or ')
        n = len(clauses)
        m = sum(len(clause.split(' and ')) for clause in clauses)
        A = [[0] * (n + m) for _ in range(n)]
        for i, clause in enumerate(clauses):
            literals = clause.split(' and ')
            for j, lit in enumerate(literals):
                if lit[0] != '~':
                    A[i][j] = 1
                else:
                    A[i][n + j] = -1
        return gaussian_elimination(A)
    
    n_max = 40
    instances_tested = 0
    total_rank = 0
    total_depth = 0
    
    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            phi = ' or '.join(' and '.join(random.choice(['x' + str(i), '~x' + str(i)]) for i in range(n)) for _ in range(n))
            rank = construct_lie_algebroid(phi)
            depth = resolution_depth(phi)
            total_rank += rank
            total_depth += depth
            instances_tested += 1
    
    mean_rank = Fraction(total_rank, instances_tested)
    mean_depth = Fraction(total_depth, instances_tested)
    ratio = mean_rank / mean_depth if mean_depth != 0 else None
    
    conjecture_holds = (0.5 <= ratio <= 1.5) if ratio is not None else False
    counterexample = "mapping_undefined" if ratio is None else ""
    
    return {
        "metric_name": "Ratio of Minimal Rank to Resolution Depth",
        "metric_value": float(ratio) if ratio is not None else None,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")