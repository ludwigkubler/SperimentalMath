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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses

    def frege_proof_width(cnf):
        # Simplified DPLL-based solver to estimate proof width
        stack = []
        assignment = {}
        for clause in cnf:
            if all(l not in assignment and -l not in assignment for l in clause):
                stack.append(clause)
        while stack:
            clause = stack.pop()
            unassigned_var = next((var for var in clause if var not in assignment), None)
            if unassigned_var is None:
                return len(cnf)  # Simplified estimation
            assignment[unassigned_var] = True
            for other_clause in cnf:
                if any(var in other_clause and -var not in assignment for var in other_clause):
                    stack.append(other_clause)
        return len(cnf)

    def orthogonality_graph(cnf):
        n = max(abs(l) for l in cnf)
        graph = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for i, var1 in enumerate(clause):
                for j, var2 in enumerate(clause[i+1:], start=i+1):
                    if var1 != -var2 and var2 != -var1:
                        graph[abs(var1)][abs(var2)] = 1
                        graph[abs(var2)][abs(var1)] = 1
        return graph

    def coxeter_group_order(graph):
        n = len(graph)
        identity = [[Fraction(1) if i == j else Fraction(0) for i in range(n)] for j in range(n)]
        # Simplified Gaussian elimination to find the order of the Coxeter group
        for i in range(n):
            if graph[i][i] == 0:
                return None  # Singular matrix, invalid graph
            pivot = Fraction(1) / graph[i][i]
            for j in range(n):
                graph[i][j] *= pivot
            for k in range(n):
                if k != i:
                    factor = graph[k][i]
                    for j in range(n):
                        graph[k][j] -= factor * graph[i][j]
        order = 1
        for row in graph:
            if any(x != Fraction(0) for x in row):
                order += 1
        return order

    def is_valid_cnf(cnf, n):
        for clause in cnf:
            if len(clause) == 0 or not all(-n <= l <= n for l in clause):
                return False
        return True

    def random_cnf(n):
        while True:
            cnf = generate_cnf(n)
            if is_valid_cnf(cnf, n):
                return cnf

    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            cnf = random_cnf(n)
            graph = orthogonality_graph(cnf)
            coxeter_order = coxeter_group_order(graph)
            if coxeter_order is None or coxeter_order <= 0:
                continue
            proof_width = frege_proof_width(cnf)
            instances_tested += 1
            n_max = max(n_max, n)
            ratio = (coxeter_order ** 2) / proof_width
            if not (0.9 < ratio < 1.1):
                conjecture_holds = False
                counterexample = f"n={n}, cnf={cnf}, coxeter_order={coxeter_order}, proof_width={proof_width}"
                break

    return {
        "metric_name": "Coxeter Group Order vs Frege Proof Width Ratio",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else None,
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
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)

    total_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    instances_tested = sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value / instances_tested} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] != "" for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")