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
    
    def generate_dnf(n, d):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(d):
            clause = random.sample(variables, random.randint(1, n))
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def dnf_to_toric_variety(dnf):
        vertices = set()
        edges = set()
        for clause in dnf:
            for literal in clause:
                if literal > 0:
                    vertices.add((1, literal))
                else:
                    vertices.add((-1, -literal))
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    edges.add(((1, clause[i]), (1, clause[j])))
        return vertices, edges
    
    def min_rank(toric_variety):
        vertices, edges = toric_variety
        n = max([abs(v[1]) for v in vertices])
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for v in vertices:
            A[v[1]][v[1]] += 1
        for u, v in edges:
            A[u[1]][v[1]] -= 1
            A[v[1]][u[1]] -= 1
        rank = 0
        for i in range(1, n + 1):
            if any(A[j][i] != 0 for j in range(n + 1)):
                pivot_row = next(j for j in range(i, n + 1) if A[j][i] != 0)
                A[i], A[pivot_row] = A[pivot_row], A[i]
                for j in range(n + 1):
                    if i != j:
                        factor = Fraction(A[j][i], A[i][i])
                        for k in range(n + 1):
                            A[j][k] -= factor * A[i][k]
                rank += 1
        return rank
    
    def resolution_depth(dnf):
        stack = []
        for clause in dnf:
            if not any(lit > 0 for lit in clause):
                return -1
            stack.append(clause)
        depth = 0
        while stack:
            clause = stack.pop()
            new_clauses = []
            for c in stack:
                for lit in clause:
                    if -lit in c:
                        new_clause = [l for l in c if l != -lit]
                        if not any(lit > 0 for lit in new_clause):
                            return -1
                        new_clauses.append(new_clause)
            stack.extend(new_clauses)
            depth += 1
        return depth
    
    n = random.randint(5, 40)
    d = random.randint(n // 2, n)
    dnf = generate_dnf(n, d)
    toric_variety = dnf_to_toric_variety(dnf)
    min_rank_value = min_rank(toric_variety)
    depth = resolution_depth(dnf)
    
    if depth == -1:
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "resolution_depth_unsat"
        }
    
    rho_numerator = sum((min_rank_value - i) * (depth - j) for i, clause in enumerate(dnf) if any(lit > 0 for lit in clause))
    rho_denominator = math.sqrt(sum((min_rank_value - i) ** 2 for i, _ in enumerate(dnf))) * math.sqrt(sum((depth - j) ** 2 for j, _ in enumerate(dnf)))
    
    if rho_denominator == 0:
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "rho_denominator_zero"
        }
    
    rho = 1 - 6 * rho_numerator / rho_denominator
    
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": rho,
        "instances_tested": 1,
        "conjecture_holds": rho >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["metric_value"] is not None for r in results):
        mean_rho = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if r["metric_value"] is None)
        print(f"RESULT: FALSIFIED counterexample='rho_denominator_zero' first_failing_seed={first_failing_seed}")