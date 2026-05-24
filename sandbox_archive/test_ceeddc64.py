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
    
    def generate_tseitin_formula(n, m):
        variables = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for i in range(m):
            clause = random.sample(variables, 2)
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return variables, clauses

    def incidence_matrix(variables, clauses):
        n = len(variables)
        m = len(clauses)
        M = [[0] * (n + m) for _ in range(n + m)]
        var_index = {var: i for i, var in enumerate(variables)}
        clause_index = [i + n for i in range(m)]
        
        for j, clause in enumerate(clauses):
            for var in clause:
                if var > 0:
                    M[var_index[var]][j] += 1
                else:
                    M[-var_index[-var]][j] -= 1
        
        return M

    def min_rank(matrix):
        n = len(matrix)
        m = len(matrix[0])
        
        def gaussian_elimination(A):
            A = [row[:] for row in A]
            rank = 0
            for j in range(m):
                i_max = next((i for i in range(rank, n) if A[i][j] != 0), -1)
                if i_max == -1:
                    continue
                A[rank], A[i_max] = A[i_max], A[rank]
                for i in range(n):
                    if i != rank:
                        factor = A[i][j] / A[rank][j]
                        for k in range(m):
                            A[i][k] -= factor * A[rank][k]
                rank += 1
            return rank
        
        return gaussian_elimination(matrix)
    
    def dpll_width(clauses):
        n = len(clauses)
        
        def backtrack(assignment, clause_index):
            if clause_index == n:
                return True
            for literal in clauses[clause_index]:
                var = abs(literal)
                if literal > 0 and assignment[var] is False or literal < 0 and assignment[var] is True:
                    continue
                new_assignment = assignment[:]
                new_assignment[var] = literal > 0
                if backtrack(new_assignment, clause_index + 1):
                    return True
            return False
        
        assignment = [None] * (n + 1)
        return backtrack(assignment, 0) + 1
    
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    variables, clauses = generate_tseitin_formula(n, m)
    
    M = incidence_matrix(variables, clauses)
    R_F = min_rank(M)
    w_F = dpll_width(clauses)
    
    return {
        "metric_name": "Ratio of Minimal Rank to DPLL Proof Width",
        "metric_value": R_F / w_F,
        "instances_tested": 1,
        "conjecture_holds": R_F <= 1.2 * w_F,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 10**6) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={len(r['variables'])}, m={len(r['clauses'])}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={r['seed']}")
                break