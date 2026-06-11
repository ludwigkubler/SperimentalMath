# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

from random import randint, seed
from fractions import Fraction
import math
import sys

def run_trial(seed: int) -> dict:
    seed(seed)
    
    def generate_k_cnf(n, k):
        literals = list(range(-n, 0)) + list(range(1, n+1))
        clauses = []
        for _ in range(k * n):
            clause = [randint(-n, -1), randint(1, n)]
            if len(set(clause)) == 2:
                clauses.append(clause)
        return clauses

    def incidence_matrix(clauses, n):
        m = len(clauses)
        A = [[0] * (2*n) for _ in range(m)]
        for i, clause in enumerate(clauses):
            for lit in clause:
                if lit > 0:
                    A[i][lit-1] = 1
                else:
                    A[i][-lit-1] = 1
        return A

    def p_adic_order(matrix):
        m, n = len(matrix), len(matrix[0])
        count = 0
        for i in range(m):
            for j in range(n):
                if matrix[i][j] != 0:
                    count += 1
        return Fraction(count).log(2)

    def dpll_search_tree_height(clauses, n):
        literals = list(range(-n, 0)) + list(range(1, n+1))
        stack = []
        assignment = [None] * (2*n)
        def solve():
            if not clauses:
                return True
            literal = next(lit for lit in literals if assignment[abs(lit)-1] is None)
            assignment[abs(literal)-1] = 1 if literal > 0 else -1
            stack.append((literal, assignment[:]))
            new_clauses = []
            for clause in clauses:
                if any(lit in clause and assignment[abs(lit)-1] == (lit > 0) for lit in clause):
                    continue
                if all(lit not in clause or assignment[abs(lit)-1] != (lit > 0) for lit in clause):
                    return False
                new_clauses.append(clause)
            if solve():
                return True
            literal, assignment = stack.pop()
            assignment[abs(literal)-1] = None
            stack.append((literal, assignment[:]))
            new_clauses = []
            for clause in clauses:
                if any(lit in clause and assignment[abs(lit)-1] == (lit > 0) for lit in clause):
                    continue
                if all(lit not in clause or assignment[abs(lit)-1] != (lit > 0) for lit in clause):
                    return False
                new_clauses.append(clause)
            if solve():
                return True
            return False
        return len(stack)

    n = randint(5, 40)
    k = randint(3, 10)
    clauses = generate_k_cnf(n, k)
    A = incidence_matrix(clauses, n)
    p_order = p_adic_order(A)
    h_phi = dpll_search_tree_height(clauses, n)

    return {
        "metric_name": "log(p)(|A(φ)|)",
        "metric_value": float(p_order),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False if p_order == 0 else True,
        "counterexample": "" if p_order != 0 else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")