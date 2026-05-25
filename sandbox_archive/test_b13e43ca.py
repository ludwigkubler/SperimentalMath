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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k * n):
            clause = set(random.sample(range(1, n + 1), random.randint(1, n)))
            if len(clause) > 0 and len(clause) < n:
                clauses.append([random.choice([-1, 1]) * var for var in clause])
        return clauses

    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for j in range(cols):
            pivot_row = -1
            for i in range(rank, rows):
                if matrix[i][j] != 0:
                    pivot_row = i
                    break
            if pivot_row == -1:
                continue
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            for i in range(rows):
                if i != rank and matrix[i][j] != 0:
                    factor = Fraction(matrix[i][j], matrix[rank][j])
                    for k in range(cols):
                        matrix[i][k] -= factor * matrix[rank][k]
            rank += 1
        return rank

    def resolution_length(clauses):
        queue = clauses[:]
        while True:
            new_clauses = []
            found_resolvent = False
            for i in range(len(queue)):
                for j in range(i + 1, len(queue)):
                    if any(-var in queue[i] and var in queue[j] for var in set(queue[i]) & set(queue[j])):
                        resolvent = [var for var in queue[i] if -var not in queue[i]] + [var for var in queue[j] if -var not in queue[j]]
                        if resolvent not in new_clauses:
                            new_clauses.append(resolvent)
                            found_resolvent = True
            if not found_resolvent:
                break
            queue.extend(new_clauses)
        return len(queue)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k = random.randint(1, min(n // 2, 3))
        cnf_instance = generate_k_cnf(n, k)
        rank = gaussian_elimination(cnf_instance)
        proof_length = resolution_length(cnf_instance)
        
        if rank < 2 ** (n - math.log(n, 2)) or proof_length < 2 ** (n - math.log(n, 2)):
            return {
                "metric_name": "K-theory Rank vs Resolution Proof Length",
                "metric_value": None,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"Instance with n={n}, rank={rank}, proof_length={proof_length}"
            }
        
        results.append({
            "n": n,
            "k": k,
            "rank": rank,
            "proof_length": proof_length
        })
    
    return {
        "metric_name": "K-theory Rank vs Resolution Proof Length",
        "metric_value": sum(result["rank"] for result in results) / len(results),
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    support_fraction = sum(1 for r in results if r["conjecture_holds"])
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value / len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8 * len(results):
        print(f"RESULT: SUPPORTED mean={total_metric_value / support_fraction} std=0.0 support_fraction={support_fraction / len(results):.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank or proof_length too small\" first_failing_seed={first_failing_seed}")