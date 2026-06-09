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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            max_row = None
            for j in range(rank, m):
                if A[j][i] != 0:
                    max_row = j
                    break
            if max_row is None:
                continue
            A[rank], A[max_row] = A[max_row], A[rank]
            pivot = A[rank][i]
            for j in range(i, n):
                A[rank][j] /= pivot
            for j in range(m):
                if j != rank and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(i, n):
                        A[j][k] -= factor * A[rank][k]
            rank += 1
        return rank
    
    def circuit_complexity(cnf):
        stack = []
        for clause in cnf:
            if all(x not in stack for x in clause) and all(-x not in stack for x in clause):
                stack.extend(clause)
            else:
                for var in clause:
                    if -var in stack:
                        stack.remove(-var)
        return len(stack)
    
    def chvatal_greedy(matroid):
        rank = 0
        independent_set = []
        for i in range(len(matroid)):
            if all(sum(matroid[i][j] * matroid[j][k] for j in range(len(matroid))) == 0 for k in range(rank) if independent_set[k]):
                independent_set.append(i)
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(1, n * (n - 1) // 2)
        cnf = generate_cnf(n, m)
        matroid = [[int(x == y or x == -y) for y in range(1, n + 1)] for x in range(1, n + 1)]
        rank = chvatal_greedy(matroid)
        circuit_comp = circuit_complexity(cnf)
        results.append((n, rank, circuit_comp))
    
    if not results:
        return {
            "metric_name": "rank_circuit_diff",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    rank_sum = sum(r for _, r, _ in results)
    circuit_sum = sum(c for _, _, c in results)
    n_total = len(results)
    n_max = max(n for n, _, _ in results)
    
    if n_max < 16:
        return {
            "metric_name": "rank_circuit_diff",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "n_max_too_small"
        }
    
    rank_mean = rank_sum / n_total
    circuit_mean = circuit_sum / n_total
    diff_mean = abs(rank_mean - circuit_mean)
    
    return {
        "metric_name": "rank_circuit_diff",
        "metric_value": diff_mean,
        "instances_tested": n_total,
        "n_max": n_max,
        "conjecture_holds": diff_mean <= 0.1 * n_max,  # Assuming ε = 0.1 for simplicity
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3**j for i in range(5) for j in range(5)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
        sys.exit(0)
    
    rank_diffs = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = len(rank_diffs) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(rank_diffs)/len(rank_diffs):.2f} std={math.sqrt(sum((x - sum(rank_diffs)/len(rank_diffs))**2 for x in rank_diffs) / len(rank_diffs)):.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r for r in results if not r["conjecture_holds"])["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={next(seed for seed, result in enumerate(results) if not result['conjecture_holds'])}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")