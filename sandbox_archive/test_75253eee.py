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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if all(abs(c) != abs(clause[0]) for c in clause[1:]):
                clauses.append(clause)
        return clauses
    
    def incidence_matrix(clauses):
        m, n = len(clauses), len(clauses[0])
        matrix = [[0] * (n + 1) for _ in range(m)]
        for i, clause in enumerate(clauses):
            for literal in clause:
                if literal > 0:
                    matrix[i][literal - 1] = 1
                else:
                    matrix[i][-1] += 1
        return matrix
    
    def min_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(n):
            if any(matrix[j][i] != 0 for j in range(rank, m)):
                for j in range(rank, m):
                    if matrix[j][i] != 0:
                        matrix[j], matrix[rank] = matrix[rank], matrix[j]
                        break
                pivot = matrix[rank][i]
                for j in range(n):
                    matrix[rank][j] /= pivot
                for j in range(m):
                    if j != rank and matrix[j][i] != 0:
                        factor = matrix[j][i]
                        for k in range(n):
                            matrix[j][k] -= factor * matrix[rank][k]
                rank += 1
        return rank
    
    def dpll_refutation_size(clauses):
        def dpll(assignment, clauses):
            if not clauses:
                return True
            literal = next(lit for lit in range(-len(clauses), len(clauses) + 1) if lit not in assignment)
            if literal > 0:
                new_assignment = assignment | {literal: True}
                if dpll(new_assignment, [c for c in clauses if literal not in c]):
                    return True
                new_assignment = assignment | {literal: False}
                if dpll(new_assignment, [c for c in clauses if -literal not in c]):
                    return True
            else:
                new_assignment = assignment | {-literal: True}
                if dpll(new_assignment, [c for c in clauses if literal not in c]):
                    return True
                new_assignment = assignment | {-literal: False}
                if dpll(new_assignment, [c for c in clauses if -literal not in c]):
                    return True
            return False
        
        return len(next(assignment for assignment in itertools.product([False, True], repeat=len(clauses)) if dpll(assignment, clauses)))
    
    n = random.choice(range(10, 41))
    clauses = generate_3cnf(n)
    matrix = incidence_matrix(clauses)
    min_rank_value = min_rank(matrix)
    refutation_size = dpll_refutation_size(clauses)
    log2_refutation_size = math.log2(refutation_size) if refutation_size > 0 else float('-inf')
    
    alpha = random.random()
    C_alpha = 1.0 / (alpha + 0.5)  # Simplified for demonstration
    conjecture_holds = log2_refutation_size <= C_alpha * math.sqrt(min_rank_value) ** (1/2 + alpha)
    counterexample = "" if conjecture_holds else f"n={n}, refutation_size={refutation_size}, min_rank_value={min_rank_value}"
    
    return {
        "metric_name": "log2_refutation_size",
        "metric_value": log2_refutation_size,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")