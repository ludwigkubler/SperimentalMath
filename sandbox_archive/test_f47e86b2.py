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
        for _ in range(2**n // 3):
            clause = [random.randint(-1, n-1) for _ in range(random.randint(1, n))]
            if all(abs(lit) != abs(clause[0]) for lit in clause[1:]):
                clauses.append(clause)
        return clauses
    
    def p_adic_valuation(clauses):
        valuations = {}
        for assignment in product([-1, 1], repeat=n):
            valuation = [sum(assignment[i] if lit > 0 else -assignment[i] for i in clause) % p for clause in clauses]
            valuations[tuple(valuation)] = True
        return list(valuations.keys())
    
    def resolution_width(clauses):
        # Simplified DPLL solver to estimate width
        queue = [clauses]
        while queue:
            clause = queue.pop()
            if not clause:
                continue
            unit_clause = next((lit for lit in clause if abs(lit) == 1), None)
            if unit_clause is not None:
                polarity = unit_clause > 0
                new_clauses = [c for c in queue if (polarity and all(lit != -unit_clause for lit in c)) or (not polarity and all(lit != unit_clause for lit in c))]
                queue.extend(new_clauses)
            else:
                return len(clause)
        return 0
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(n):
            if any(matrix[j][i] != 0 for j in range(rank, m)):
                rank += 1
                for j in range(m):
                    if j >= rank:
                        matrix[j][i], matrix[rank-1][i] = matrix[rank-1][i], matrix[j][i]
                    if matrix[j][i]:
                        factor = matrix[j][i] / matrix[rank-1][i]
                        for k in range(n):
                            matrix[j][k] -= factor * matrix[rank-1][k]
        return rank
    
    n = random.randint(5, 40)
    p = 2
    clauses = generate_cnf(n)
    valuations = p_adic_valuation(clauses)
    width = resolution_width(clauses)
    
    if not valuations:
        return {
            "metric_name": "rank",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    matrix = [[0] * len(valuations) for _ in range(len(clauses))]
    for i, clause in enumerate(clauses):
        for j, valuation in enumerate(valuations):
            if all((valuation[k] + clause[k]) % p == 0 for k in range(n)):
                matrix[i][j] = 1
    
    rank = matrix_rank(matrix)
    
    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if rank == width else False,
        "counterexample": "" if rank == width else f"Rank {rank} != Width {width}"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials run")
        sys.exit(1)
    
    rank_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    if not rank_values:
        print("RESULT: INCONCLUSIVE no valid ranks found")
        sys.exit(1)
    
    mean_rank = sum(rank_values) / len(rank_values)
    std_rank = math.sqrt(sum((x - mean_rank)**2 for x in rank_values) / len(rank_values))
    
    support_fraction = sum(r["conjecture_holds"] for r in results if r["metric_value"] is not None) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank:.2f} std={std_rank:.2f} support_fraction={support_fraction:.2f}")
    elif any(r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank does not match Width\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds support the conjecture")