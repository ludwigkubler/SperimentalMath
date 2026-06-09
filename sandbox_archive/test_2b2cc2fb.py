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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf):
        def solve(literals):
            if not cnf:
                return literals
            unit_clauses = [c for c in cnf if len(c) == 1]
            if unit_clauses:
                literal = unit_clauses[0][0]
                new_cnf = [c for c in cnf if literal not in c and -literal not in c]
                return solve(literals + [literal] if literal > 0 else literals + [-literal])
            pure_literals = []
            for var in range(1, max(abs(lit) for lit in literals) + 1):
                pos_count = sum(1 for lit in literals if lit == var)
                neg_count = sum(1 for lit in literals if lit == -var)
                if pos_count == 0:
                    pure_literals.append(-var)
                elif neg_count == 0:
                    pure_literals.append(var)
            if not pure_literals:
                return None
            literal = pure_literals[0]
            new_cnf = [c for c in cnf if literal not in c and -literal not in c]
            return solve(literals + [literal] if literal > 0 else literals + [-literal])
        return solve([])
    
    def zeta_rank(cnf):
        n = max(abs(lit) for lit in sum(cnf, []))
        lattice = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for i in clause:
                for j in clause:
                    if i != j:
                        lattice[abs(i)][abs(j)] += 1
        rank = 0
        for row in lattice:
            non_zero_cols = [col for col, val in enumerate(row) if val > 0]
            if non_zero_cols:
                pivot_col = min(non_zero_cols)
                pivot_row = next(r for r in range(len(lattice)) if lattice[r][pivot_col] > 0)
                rank += 1
                for j in range(n + 1):
                    lattice[pivot_row][j] //= lattice[pivot_row][pivot_col]
                for i in range(n + 1):
                    if i != pivot_row:
                        factor = lattice[i][pivot_col]
                        for j in range(n + 1):
                            lattice[i][j] -= factor * lattice[pivot_row][j]
        return rank
    
    n_max = 40
    instances_tested = 0
    metric_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            m = random.randint(n // 2, n)
            cnf = generate_cnf(n, m)
            depth = dpll(cnf)
            if depth is None:
                continue
            zeta_rk = zeta_rank(cnf)
            instances_tested += 1
            metric_values.append((zeta_rk, depth))
    
    if not metric_values:
        return {
            "metric_name": "zeta_rank",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    zeta_rks, depths = zip(*metric_values)
    correlation_coefficient = sum((z - z_mean) * (d - d_mean) for z, d in zip(zeta_rks, depths)) / math.sqrt(sum((z - z_mean) ** 2 for z in zeta_rks) * sum((d - d_mean) ** 2 for d in depths))
    z_mean = sum(zeta_rks) / len(zeta_rks)
    d_mean = sum(depths) / len(depths)
    
    return {
        "metric_name": "zeta_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": 0.5 < correlation_coefficient <= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] >= 0.5 for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_below_0.5\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")