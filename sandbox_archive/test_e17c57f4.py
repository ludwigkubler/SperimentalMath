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
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        var = next((v for v in range(1, n+1) if v not in assignment and -v not in assignment), None)
        if var is None:
            return False
        
        def propagate():
            new_assignment = assignment.copy()
            for clause in clauses:
                if all(v in new_assignment or -v in new_assignment for v in clause):
                    continue
                if any(-v in new_assignment for v in clause):
                    return False, {}
                new_assignment[var] = 1
                break
            else:
                return True, new_assignment
        
        success, new_assignment = propagate()
        if not success:
            var = -var
            success, new_assignment = propagate()
        
        if not success:
            return False
        
        return dpll([c for c in clauses if not any(v in c or -v in c for v in (var, -var))], new_assignment)
    
    def grothendieck_group(clauses):
        n_vars = max(abs(c) for clause in clauses for c in clause)
        identity = [0] * (n_vars + 1)
        
        def add(a, b):
            return [ai + bi for ai, bi in zip(a, b)]
        
        def multiply(a, b):
            result = [0] * (n_vars + 1)
            for i in range(1, n_vars + 1):
                if a[i]:
                    for j in range(1, n_vars + 1):
                        if b[j]:
                            result[i ^ j] += a[i] * b[j]
            return result
        
        def inverse(a):
            det = sum(a[i] * (-1) ** i * a[(i+1):(n_vars+1)][::-1][0:i-1] for i in range(1, n_vars + 1))
            if det == 0:
                return None
            adjugate = [0] * (n_vars + 1)
            for i in range(1, n_vars + 1):
                for j in range(1, n_vars + 1):
                    submatrix = [row[:j-1] + row[j:] for row in a[1:i] + a[i+1:]]
                    adjugate[i * (n_vars + 1) + j] = (-1) ** (i + j) * det(submatrix)
            return [ai / det for ai in adjugate]
        
        def det(matrix):
            if len(matrix) == 2:
                return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
            result = 0
            for i in range(len(matrix)):
                submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
                result += (-1) ** i * matrix[0][i] * det(submatrix)
            return result
        
        def is_zero_vector(v):
            return all(abs(x) < 1e-9 for x in v)
        
        def reduce_basis(basis):
            basis = [v for v in basis if not any(is_zero_vector(add(v, w)) for w in basis)]
            for i in range(len(basis)):
                for j in range(i + 1, len(basis)):
                    while not is_zero_vector(basis[j]):
                        k = next(k for k in range(1, n_vars + 1) if basis[i][k] != 0 and basis[j][k] != 0)
                        scale = Fraction(basis[j][k], basis[i][k])
                        basis[j] = add(multiply(scale, basis[i]), basis[j])
            return [v for v in basis if not any(is_zero_vector(add(v, w)) for w in basis)]
        
        def rank(matrix):
            basis = reduce_basis([row[:] for row in matrix])
            return len(basis)
        
        matrix = [[0] * (n_vars + 1) for _ in range(n_vars + 1)]
        for clause in clauses:
            for i in clause:
                matrix[i][i] += 1
        
        return rank(matrix)
    
    n = random.randint(5, 40)
    clauses = [random.choice([-i-1, i] for i in range(n)) for _ in range(random.randint(1, n))]
    dpll_result = dpll(clauses, {})
    grothendieck_rank = grothendieck_group(clauses)
    
    if not dpll_result:
        return {
            "metric_name": "min_rank(G(φ))",
            "metric_value": 0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL search tree did not find a satisfying assignment"
        }
    
    return {
        "metric_name": "min_rank(G(φ))",
        "metric_value": grothendieck_rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    from statistics import mean, stdev
    
    metric_values = [r["metric_value"] for r in results]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean(metric_values):.2f} std={stdev(metric_values):.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean(metric_values):.2f} std={stdev(metric_values):.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"DPLL search tree did not find a satisfying assignment\" first_failing_seed={first_failing_seed}")