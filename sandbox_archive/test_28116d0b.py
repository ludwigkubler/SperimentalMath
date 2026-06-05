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
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        unit_clauses = [c for c in cnf if len(c) == 1]
        while unit_clauses:
            literal = unit_clauses.pop()
            value = literal[0] > 0
            assignment[-literal[0]] = not value
            new_assignment = {x: assignment[x] for x in assignment}
            new_assignment[literal[0]] = value
            cnf = [[x for x in c if x != literal[0] and -x not in new_assignment] for c in cnf]
            unit_clauses.extend([c for c in cnf if len(c) == 1])
        return assignment
    
    def min_order_of_generators(cnf):
        n = len(cnf)
        G = [[0] * (n + 1) for _ in range(n + 1)]
        for i, clause in enumerate(cnf):
            for literal in clause:
                if literal > 0:
                    G[i][literal] += 1
                else:
                    G[literal][i] += 1
        # Gaussian elimination to find the rank of the matrix
        def gaussian_elimination(A):
            m, n = len(A), len(A[0])
            for i in range(m):
                if A[i][i] == 0:
                    for j in range(i + 1, m):
                        if A[j][i] != 0:
                            A[i], A[j] = A[j], A[i]
                            break
                    else:
                        return n  # Matrix is singular
                for j in range(n):
                    if i == j:
                        continue
                    factor = -A[j][i] / A[i][i]
                    for k in range(m):
                        A[k][j] += factor * A[k][i]
            rank = sum(1 for row in A if any(row))
            return rank
        return gaussian_elimination(G)
    
    def dpll_tree_width(cnf, assignment={}):
        n = len(cnf)
        queue = [(cnf, assignment)]
        max_width = 0
        while queue:
            cnf, assignment = queue.pop()
            unit_clauses = [c for c in cnf if len(c) == 1]
            if not unit_clauses:
                continue
            literal = unit_clauses[0][0]
            value = literal > 0
            new_assignment = {x: assignment[x] for x in assignment}
            new_assignment[literal] = value
            queue.append(([[x for x in c if x != literal and -x not in new_assignment] for c in cnf], new_assignment))
        return max_width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        min_order = min_order_of_generators(cnf)
        if min_order > 10:
            return {"metric_name": "min_order", "metric_value": min_order, "instances_tested": 1, "n_max": n, "conjecture_holds": False, "counterexample": "generator_order_metric_too_high"}
        dpll_width = dpll_tree_width(cnf)
        results.append((min_order, dpll_width))
    
    mean_min_order = sum(x[0] for x in results) / len(results)
    mean_dpll_width = sum(x[1] for x in results) / len(results)
    correlation_coefficient = 0
    if mean_min_order != 0 and mean_dpll_width != 0:
        correlation_coefficient = (sum((x[0] - mean_min_order) * (x[1] - mean_dpll_width) for x in results) /
                                  math.sqrt(sum((x[0] - mean_min_order) ** 2 for x in results) *
                                            sum((x[1] - mean_dpll_width) ** 2 for x in results)))
    
    return {"metric_name": "min_order", "metric_value": mean_min_order, "instances_tested": len(results), "n_max": max(n_values), "conjecture_holds": correlation_coefficient >= 0.7, "counterexample": ""}

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(x["metric_value"] for x in results) / len(results)
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={result['seed']}")
                break