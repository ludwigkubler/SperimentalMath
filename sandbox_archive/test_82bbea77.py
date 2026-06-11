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
    
    def generate_k_cnf(n, k):
        literals = [f"v{i+1}" for i in range(n)]
        clauses = []
        for _ in range(k * n // 2):
            clause = random.sample(literals, random.randint(3, 5))
            if random.choice([True, False]):
                clause = [f"-{lit}" for lit in clause]
            clauses.append(clause)
        return clauses
    
    def incidence_matrix(clauses, literals):
        m = len(clauses)
        n = len(literals)
        A = [[0] * n for _ in range(m)]
        for i, clause in enumerate(clauses):
            for lit in clause:
                if lit.startswith('-'):
                    var = int(lit[1:]) - 1
                    A[i][var] = -1
                else:
                    var = int(lit) - 1
                    A[i][var] = 1
        return A
    
    def p_adic_order(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            for j in range(n):
                if matrix[i][j] != 0:
                    return math.log(abs(matrix[i][j]), 2)
        return 0
    
    def dpll_search_tree_height(clauses, literals):
        def solve(clause_set, assignment):
            if not clause_set:
                return True
            literal = random.choice(literals)
            if literal in assignment:
                continue
            for val in [True, False]:
                new_assignment = assignment.copy()
                new_assignment[literal] = val
                new_clauses = [c for c in clause_set if not any(lit in c and (new_assignment[lit] == (lit.startswith('-') != val)) for lit in c)]
                if solve(new_clauses, new_assignment):
                    return True
            return False
        return len(solve(clauses, {}))
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_p_adic_order = 0
    total_dpll_height = 0
    
    for n in n_values:
        for _ in range(5):
            clauses = generate_k_cnf(n, 3)
            literals = [f"v{i+1}" for i in range(n)]
            A = incidence_matrix(clauses, literals)
            p_adic = p_adic_order(A)
            dpll_height = dpll_search_tree_height(clauses, literals)
            
            if p_adic == 0 or dpll_height == 0:
                continue
            
            instances_tested += 1
            total_p_adic_order += p_adic
            total_dpll_height += dpll_height
    
    if instances_tested < 30:
        return {
            "metric_name": "p-adic Order vs DPLL Height",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Too few instances tested"
        }
    
    mean_p_adic_order = total_p_adic_order / instances_tested
    mean_dpll_height = total_dpll_height / instances_tested
    
    correlation_coefficient = (instances_tested * sum(p_adic * dpll for p_adic, dpll in zip(range(instances_tested), range(instances_tested))) - instances_tested * mean_p_adic_order * mean_dpll_height) / \
                              math.sqrt((instances_tested * sum(p_adic**2 for p_adic in range(instances_tested)) - instances_tested * mean_p_adic_order**2) *
                                        (instances_tested * sum(dpll**2 for dpll in range(instances_tested)) - instances_tested * mean_dpll_height**2))
    
    return {
        "metric_name": "p-adic Order vs DPLL Height",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {result}")
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['instances_tested']}, p-adic Order vs DPLL Height correlation coefficient={r['metric_value']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break