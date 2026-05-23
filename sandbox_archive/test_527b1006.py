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
    
    def ramanujan_graph(n):
        if n <= 2:
            return []
        d = (n - 1) * 3
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.randint(0, d) == 0:
                    A[i][j] = A[j][i] = 1
        return A
    
    def euler_characteristic(A):
        n = len(A)
        trace = sum(A[i][i] for i in range(n))
        det = determinant(A)
        return trace - det
    
    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = 0
        for j in range(len(A)):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += ((-1) ** j) * A[0][j] * determinant(submatrix)
        return det
    
    def tseitin_formula(n):
        literals = list(range(1, n + 1))
        clauses = []
        for i in range(n):
            clauses.append([literals[i]])
            for j in range(i + 1, n):
                clauses.append([-literals[i], -literals[j]])
                clauses.append([literals[i], literals[j]])
        return clauses
    
    def resolution_length(clauses):
        stack = []
        while True:
            new_clause = None
            for i in range(len(stack)):
                for j in range(i + 1, len(stack)):
                    if set(stack[i]) & set(stack[j]):
                        common_lit = (set(stack[i]) & set(stack[j])).pop()
                        new_clause = [lit for lit in stack[i] if lit != -common_lit]
                        new_clause.extend([lit for lit in stack[j] if lit != common_lit])
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(stack)
            stack.append(new_clause)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = ramanujan_graph(n)
    euler_char = euler_characteristic(G)
    if euler_char == 0:
        return {
            "metric_name": "resolution_length",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    T = tseitin_formula(n)
    proof_length = resolution_length(T)
    
    if proof_length is not None:
        upper_bound = 1.5 ** n / euler_char ** 2
        return {
            "metric_name": "resolution_length",
            "metric_value": proof_length,
            "instances_tested": 1,
            "conjecture_holds": proof_length <= upper_bound,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "resolution_length",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")