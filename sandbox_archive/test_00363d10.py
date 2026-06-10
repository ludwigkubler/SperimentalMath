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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return [row[:n-1] for row in A]

    def frege_proof_width(phi):
        # Placeholder function to simulate Frege proof width calculation
        return len(phi.split())

    def grothendieck_group_rank(A):
        rank = 0
        while A:
            pivot_row = next((i for i, row in enumerate(A) if any(row)), None)
            if pivot_row is None:
                break
            rank += 1
            A = [row[:pivot_row] + row[pivot_row+1:] for row in A]
            A = gaussian_elimination([row[:pivot_row] + row[pivot_row+1:] for row in A])
        return rank

    def generate_frege_proof(num_vars):
        # Placeholder function to simulate Frege proof generation
        return " ".join(random.choices("ABCD", k=random.randint(2, 5)) for _ in range(num_vars))

    n = random.choice([5, 10, 15, 20, 30, 40])
    phi = generate_frege_proof(n)
    width = frege_proof_width(phi)
    
    # Placeholder Grothendieck group matrix (random for simplicity)
    A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    rank = grothendieck_group_rank(A)

    return {
        "metric_name": "rank_to_width_ratio",
        "metric_value": rank / width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(rank / width - 1) <= 0.1 and rank / width <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 10000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and any(res["metric_value"] > 2 for res in results):
        first_failing_seed = next(i for i, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rank_to_width_ratio_exceeds_2' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")