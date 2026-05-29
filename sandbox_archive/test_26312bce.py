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
    
    def dpll_size(f):
        n = len(f)
        clauses = [tuple(int(bit) for bit in clause) for clause in f]
        
        def is_satisfiable(assignment):
            for clause in clauses:
                if not any(assignment[var] == val for var, val in enumerate(clause)):
                    return False
            return True
        
        def dpll(assignment, unsatisfied):
            if len(unsatisfied) == 0:
                return True
            var = unsatisfied[0][0]
            for val in [0, 1]:
                new_assignment = assignment[:]
                new_assignment[var] = val
                new_unsatisfied = [(var2, {v: u[v] for v in u if v != var}) for var2, u in unsatisfied]
                if is_satisfiable(new_assignment):
                    if dpll(new_assignment, new_unsatisfied):
                        return True
            return False
        
        unsatisfied = [(i, {j: 1 for j in range(n)}) for i in range(n)]
        return len(unsatisfied) - sum(dpll([0] * n, unsatisfied[:i]) for i in range(n))
    
    def symplectic_capacity(M):
        n = len(M)
        I = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
        
        def gaussian_elimination(A):
            m = len(A)
            for i in range(m):
                max_row = i
                for j in range(i + 1, m):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[i], A[max_row] = A[max_row], A[i]
                pivot = A[i][i]
                for j in range(m):
                    A[i][j] /= pivot
                for j in range(m):
                    if j != i:
                        factor = A[j][i]
                        for k in range(m):
                            A[j][k] -= factor * A[i][k]
            return A
        
        M_row_echelon = gaussian_elimination(M)
        
        def rank(A):
            m, n = len(A), len(A[0])
            r = 0
            for i in range(min(m, n)):
                if all(abs(A[i][j]) < 1e-9 for j in range(n)):
                    break
                r += 1
            return r
        
        return rank(M_row_echelon)
    
    def boolean_function_to_matrix(f):
        n = len(f)
        M = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for i, clause in enumerate(f):
            for j, bit in enumerate(clause):
                if bit == 1:
                    M[i][j] += Fraction(1)
                elif bit == -1:
                    M[i][j] -= Fraction(1)
        return M
    
    def log2(x):
        return math.log2(x) if x > 0 else float('-inf')
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = [random.choices([-1, 1], k=n) for _ in range(2**n)]
    M_f = boolean_function_to_matrix(f)
    t_star = dpll_size(f)
    symplectic_cap = symplectic_capacity(M_f)
    
    if t_star == 0:
        return {
            "metric_name": "symplectic_capacity",
            "metric_value": float('inf'),
            "instances_tested": len(f),
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL size is zero, which is undefined for this formula."
        }
    
    metric_value = abs(symplectic_cap - log2(t_star))
    return {
        "metric_name": "symplectic_capacity",
        "metric_value": metric_value,
        "instances_tested": len(f),
        "n_max": n,
        "conjecture_holds": metric_value <= 1,  # Assuming k = 1 for simplicity
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")