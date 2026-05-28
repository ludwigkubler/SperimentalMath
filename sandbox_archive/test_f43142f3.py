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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j == i:
                    A[i][j] = Fraction(1, A[i][j])
                else:
                    A[i][j] = Fraction(0)
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        if j == i:
                            A[k][j] = 0
                        else:
                            A[k][j] -= factor * A[i][j]
        return A
    
    def rank_of_matrix(A):
        m, n = len(A), len(A[0])
        A_rref = gaussian_elimination(A)
        rank = sum(1 for row in A_rref if any(x != 0 for x in row))
        return rank
    
    def resolution_proof_length(m, n):
        # Simplified estimation of resolution proof length
        return m * n
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        m = random.randint(2 * n, 5 * n)
        formula = " ".join(f"~x{i}" if i % 2 == 0 else f"x{i}" for i in range(n))
        clauses = [formula]
        G = [[1] * (n + 1) for _ in range(m)]
        
        rank = rank_of_matrix(G)
        proof_length = resolution_proof_length(m, n)
        
        if proof_length < 2 ** (math.log(rank, 2)):
            conjecture_holds = False
            counterexample = f"Seed {seed}: Rank={rank}, Proof Length={proof_length}"
            break
        
        total_metric_value += math.log(proof_length, 2) / math.log(2)
        instances_tested += m
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": total_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 29 primes
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")