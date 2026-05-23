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
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def is_satisfiable(cnf):
        # Simple backtracking SAT solver
        assignment = [False] * (n + 1)
        
        def backtrack(i):
            if i > n:
                return True
            for val in [True, False]:
                assignment[i] = val
                if all(any(not (j < 0 and not assignment[-j]) for j in clause) for clause in cnf):
                    if backtrack(i + 1):
                        return True
            return False
        
        return backtrack(1)
    
    def quasi_plurality_matrix(cnf):
        n = len(cnf[0])
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    matrix[lit][lit] += 1
                else:
                    matrix[-lit][-lit] += 1
        
        return matrix
    
    def min_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if any(matrix[i][j] != 0 for j in range(n)):
                rank += 1
                for j in range(n):
                    matrix[i][j] /= matrix[i][i]
                for k in range(m):
                    if k != i:
                        factor = matrix[k][i]
                        for j in range(n):
                            matrix[k][j] -= factor * matrix[i][j]
        return rank
    
    n = random.randint(5, 40)
    m = random.randint(10, 2 * n)
    
    cnf = generate_cnf(n, m)
    sat = is_satisfiable(cnf)
    
    if not sat:
        d = Fraction(1, 2)  # Example constant for unsatisfiable case
        min_rank_value = d ** n
    else:
        c = Fraction(1, 2)  # Example constant for satisfiable case
        min_rank_value = c * n
    
    matrix = quasi_plurality_matrix(cnf)
    rank = min_rank(matrix)
    
    return {
        "metric_name": "min_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": sat and rank <= c * n or not sat and rank >= d ** n,
        "counterexample": "" if sat and rank <= c * n or not sat and rank >= d ** n else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_rank = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}"
    
    print(result)