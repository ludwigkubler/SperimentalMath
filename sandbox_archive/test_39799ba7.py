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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clause = f'{variables[i]}'
            for j in range(i + 1, n):
                clause += f' | {variables[j]}'
            clauses.append(clause)
        return ' & '.join(clauses)

    def stabilizer_matrix(formula):
        # Simplified version of Tseitin formula to matrix
        n = len(formula.split(' & '))
        M = [[0] * (n + 1) for _ in range(n + 1)]
        for i, clause in enumerate(formula.split(' & ')):
            for var in clause.split(' | '):
                if var.startswith('x'):
                    j = int(var[1:])
                    M[i][j] = 1
                    M[j][i] = 1
        return M

    def quantum_entanglement_entropy(M):
        # Simplified version of entanglement entropy calculation
        n = len(M)
        rank = 0
        for i in range(n):
            if all(M[i][j] == 0 for j in range(i + 1, n)):
                rank += 1
        return rank

    def resolution_length(formula):
        # Simplified version of resolution length calculation
        n = len(formula.split(' & '))
        return n * (n - 1) // 2

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_tseitin_formula(n)
        M = stabilizer_matrix(formula)
        rank = quantum_entanglement_entropy(M)
        t_F = resolution_length(formula)
        results.append((n, rank, t_F))
    
    if len(results) < 30:
        return {
            "metric_name": "resolution_length",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    ranks = [r for _, r, _ in results]
    t_Fs = [t for _, _, t in results]
    
    def spearman_rank_correlation(ranks, t_Fs):
        n = len(ranks)
        rank_ranks = {v: i + 1 for i, v in enumerate(sorted(set(ranks)))}
        rank_t_Fs = {v: i + 1 for i, v in enumerate(sorted(set(t_Fs)))}
        sum_diff_squares = sum((rank_ranks[r] - rank_t_Fs[t])**2 for r, t in zip(ranks, t_Fs))
        return 1 - (6 * sum_diff_squares) / (n * (n**2 - 1))

    correlation = spearman_rank_correlation(ranks, t_Fs)
    
    return {
        "metric_name": "resolution_length",
        "metric_value": correlation,
        "instances_tested": len(results),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_d = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_d)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(r['conjecture_holds'] for r in results) else 'FALSIFIED'} mean={mean_d} std={std_dev} support_fraction={support_fraction}")