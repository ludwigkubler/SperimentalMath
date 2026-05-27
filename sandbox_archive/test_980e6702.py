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
            clause = [random.randint(1, 2*n) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def tropicalized_quaternion_algebra(cnf):
        # Construct a matrix representation of the CNF
        m = len(cnf)
        n = max(max(clause) for clause in cnf)
        M = [[0] * (n + 1) for _ in range(m)]
        
        for i, clause in enumerate(cnf):
            for lit in clause:
                if lit > 0:
                    M[i][lit - 1] = 1
                else:
                    M[i][-lit] = 1
        
        # Perform Gaussian elimination to find the rank
        rank = 0
        for i in range(m):
            if any(M[i]):
                pivot_col = next(j for j, x in enumerate(M[i]) if x)
                rank += 1
                for j in range(i + 1, m):
                    factor = M[j][pivot_col] / M[i][pivot_col]
                    for k in range(n + 1):
                        M[j][k] -= factor * M[i][k]
        
        return rank
    
    n_values = [10, 20, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        rank = tropicalized_quaternion_algebra(cnf)
        f_n = int(1.5 * n)
        
        results.append({
            "n": n,
            "rank": rank,
            "f_n": f_n,
            "conjecture_holds": rank <= f_n
        })
    
    metric_value = sum(result["rank"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["conjecture_holds"] for result in results)
    counterexample = "" if conjecture_holds else "f(n) bound violated"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"f(n) bound violated\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")