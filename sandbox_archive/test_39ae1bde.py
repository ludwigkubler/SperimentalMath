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
    
    n = 30  # Number of vertices in the graph
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            if A[i][i] == 0:
                pivot_found = False
                for j in range(i+1, m):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]
                        pivot_found = True
                        break
                if not pivot_found:
                    continue
            for j in range(m):
                if j == i:
                    continue
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return sum(1 for row in A if any(row))
    
    def tseitin_formula(G):
        variables = {f"x{i}{j}": (i, j) for i in range(n) for j in range(i+1, n)}
        clauses = []
        for i in range(n):
            clause = [f"~x{i}{j}" if G[i][j] == 0 else f"x{i}{j}" for j in range(i+1, n)]
            clauses.append("|".join(clause))
        for i in range(n):
            for j in range(i+1, n):
                clause = [f"~x{i}{k}" if G[i][k] == 0 else f"x{i}{k}" for k in range(j+1, n)]
                clause.append(f"~x{j}{k}" if G[j][k] == 0 else f"x{j}{k}")
                clauses.append("|".join(clause))
        return "&".join(clauses)
    
    def resolution_length(formula):
        clauses = formula.split("&")
        unit_clauses = [c for c in clauses if len(c) == 1]
        while unit_clauses:
            new_unit_clause = None
            for clause in unit_clauses:
                literal = clause[0] if clause[0] != "~" else clause[1:]
                for i, other_clause in enumerate(clauses):
                    if literal in other_clause or f"~{literal}" in other_clause:
                        new_clause = [l for l in other_clause.split("|") if l != literal and l != f"~{literal}"]
                        if len(new_clause) == 1:
                            new_unit_clause = new_clause[0]
                            break
                if new_unit_clause:
                    unit_clauses.append(new_unit_clause)
                    clauses[i] = "|".join(new_clause)
                    break
            else:
                return len(unit_clauses)
        return float('inf')
    
    cocomplex_rank = gaussian_elimination(G)
    tseitin_formula_str = tseitin_formula(G)
    resolution_length_value = resolution_length(tseitin_formula_str)
    
    return {
        "metric_name": "resolution_length",
        "metric_value": resolution_length_value,
        "instances_tested": 1,
        "conjecture_holds": cocomplex_rank >= math.log(n) ** 2,
        "counterexample": "" if cocomplex_rank >= math.log(n) ** 2 else f"Graph with rank {cocomplex_rank} and resolution length {resolution_length_value}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")