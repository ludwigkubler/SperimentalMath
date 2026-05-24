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
    
    def generate_xor_tautology(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tropical_derivative(tau):
        n = len(tau)
        D = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(i + 1, n + 1):
                if tau[i] == 1 and tau[j - 1] == 1:
                    D[i][j] = 1
                elif tau[i] == 0 and tau[j - 1] == 0:
                    D[i][j] = 1
        return D
    
    def resolution_length(tau):
        n = len(tau)
        clauses = [tau[:i] + [1] + tau[i+1:] for i in range(n)]
        length = 0
        while True:
            new_clauses = []
            added_clause = False
            for c1 in clauses:
                for c2 in clauses:
                    if len(set(c1) & set(c2)) == n - 1:
                        new_clause = [x for x in c1 + c2 if x not in (0, 1)]
                        if new_clause not in new_clauses and new_clause not in clauses:
                            new_clauses.append(new_clause)
                            added_clause = True
            if not added_clause:
                break
            clauses.extend(new_clauses)
            length += len(new_clauses)
        return length
    
    def spearman_rank_correlation(D, r):
        n = len(D)
        rank_D = [0] * n
        rank_r = [0] * n
        for i in range(n):
            rank_D[i] = sorted(range(n), key=lambda j: D[j][i])[-1]
            rank_r[i] = sorted(range(n), key=lambda j: r[j])[-1]
        return sum((rank_D[i] - rank_r[i])**2 for i in range(n)) / (n * (n**2 - 1))
    
    def polynomial_regression(x, y):
        n = len(x)
        Sx, Sy, Sxx, Sxy = 0, 0, 0, 0
        for i in range(n):
            Sx += x[i]
            Sy += y[i]
            Sxx += x[i]**2
            Sxy += x[i] * y[i]
        a = (n * Sxy - Sx * Sy) / (n * Sxx - Sx**2)
        b = (Sy - a * Sx) / n
        return a, b
    
    def log_bound(n):
        return math.log(n)
    
    results = []
    for _ in range(30):
        tau = generate_xor_tautology(random.randint(4, 40))
        D = tropical_derivative(tau)
        r = resolution_length(tau)
        results.append((D, r))
    
    ranks = [spearman_rank_correlation(D, r) for D, r in results]
    a, b = polynomial_regression(range(len(ranks)), ranks)
    mean_rank = sum(ranks) / len(ranks)
    std_rank = math.sqrt(sum((r - mean_rank)**2 for r in ranks) / len(ranks))
    
    if all(rank > 0.7 for rank in ranks):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "Spearman rank correlation < 0.7"
    
    return {
        "metric_name": "Spearman Rank Correlation",
        "metric_value": mean_rank,
        "instances_tested": len(ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Spearman rank correlation < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")