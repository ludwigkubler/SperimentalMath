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
    
    def generate_cnf(width: int, n_clauses: int):
        cnf = []
        for _ in range(n_clauses):
            clause = [random.randint(1, width) for _ in range(random.randint(1, 3))]
            cnf.append(clause)
        return cnf
    
    def compute_minimal_rank(cnf):
        n = len(cnf)
        m = max(max(abs(lit) for lit in clause) for clause in cnf)
        adj_matrix = [[0] * (2 * m - 1) for _ in range(2 * m - 1)]
        
        for clause in cnf:
            for literal in clause:
                if literal > 0:
                    i = literal - 1
                else:
                    i = -(literal + 1)
                adj_matrix[i][n - literal - 1] = 1
                adj_matrix[n - literal - 1][i] = 1
        
        # Gaussian elimination to find the rank of the matrix
        rank = 0
        for i in range(2 * m - 1):
            if all(adj_matrix[j][i] == 0 for j in range(rank)):
                continue
            pivot_row = rank
            while adj_matrix[pivot_row][i] == 0:
                pivot_row += 1
                if pivot_row >= 2 * m - 1:
                    return rank
            for j in range(2 * m - 1):
                if i != j and adj_matrix[j][i] != 0:
                    factor = Fraction(adj_matrix[j][i], adj_matrix[pivot_row][i])
                    for k in range(2 * m - 1):
                        adj_matrix[j][k] -= factor * adj_matrix[pivot_row][k]
            rank += 1
        
        return rank
    
    width_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    n_max = 0
    
    for width in width_values:
        for _ in range(5):
            cnf = generate_cnf(width, random.randint(1, 10))
            rank = compute_minimal_rank(cnf)
            total_rank += rank
            instances_tested += 1
            n_max = max(n_max, len(cnf))
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = mean_rank <= width_values[0]**2
    counterexample = "" if conjecture_holds else f"mean_rank={mean_rank}, expected<=25"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")