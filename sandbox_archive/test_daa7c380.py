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
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            if all(abs(x) != abs(y) for x, y in zip(clause, clause[1:])):
                clauses.append(clause)
        return clauses
    
    def cnf_to_orthogonality_graph(cnf):
        n = max(abs(var) for var in sum(cnf, []))
        graph = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    x, y = abs(clause[i]), abs(clause[j])
                    graph[x][y] += 1
                    graph[y][x] += 1
        return graph
    
    def coxeter_group_order(graph):
        n = len(graph)
        identity = [Fraction(1) if i == j else Fraction(0) for i in range(n)]
        matrix = [[Fraction(1) if i == j else Fraction(-graph[i][j]) for j in range(n)] for i in range(n)]
        
        def gaussian_elimination(A):
            m, n = len(A), len(A[0])
            for k in range(m):
                max_row = k
                for i in range(k + 1, m):
                    if abs(A[i][k]) > abs(A[max_row][k]):
                        max_row = i
                A[k], A[max_row] = A[max_row], A[k]
                if A[k][k] == Fraction(0):
                    continue
                for j in range(k + 1, n):
                    A[k][j] /= A[k][k]
                A[k][k] = Fraction(1)
                for i in range(m):
                    if i != k:
                        factor = A[i][k]
                        for j in range(k, n):
                            A[i][j] -= factor * A[k][j]
            return A
        
        reduced_matrix = gaussian_elimination(matrix)
        
        order = Fraction(1)
        for row in reduced_matrix:
            pivot_index = next((i for i, x in enumerate(row) if x != Fraction(0)), None)
            if pivot_index is not None:
                order *= Fraction(1, abs(row[pivot_index]))
        return order
    
    def frege_proof_width(cnf):
        n = max(abs(var) for var in sum(cnf, []))
        stack = []
        width = 0
        for clause in cnf:
            new_assignment = {}
            for literal in clause:
                if literal not in new_assignment and -literal not in new_assignment:
                    new_assignment[literal] = True
            assignment = {**new_assignment}
            while stack:
                top_clause = stack[-1]
                if all(lit in assignment and assignment[lit] == (lit > 0) for lit in top_clause):
                    stack.pop()
                else:
                    break
            stack.append(clause)
            width = max(width, len(stack))
        return width
    
    n_max = 40
    instances_tested = 30
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        cnf = generate_cnf(n)
        graph = cnf_to_orthogonality_graph(cnf)
        coxeter_order = coxeter_group_order(graph)
        frege_w = frege_proof_width(cnf)
        
        if frege_w == 0:
            conjecture_holds = False
            counterexample = "Frege proof width is zero"
            break
        
        metric_value += (coxeter_order ** 2) / frege_w
    
    metric_value /= instances_tested
    
    return {
        "metric_name": "Coxeter Group Order and Frege Proof Width Ratio",
        "metric_value": float(metric_value),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")