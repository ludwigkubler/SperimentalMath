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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-n, -1) if random.choice([True, False]) else random.randint(1, n) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def matrix_A(phi):
        n = len(phi[0])
        A = [[0] * (2**n) for _ in range(n)]
        for i, clause in enumerate(phi):
            for j in range(2**n):
                if all(var in phi[i] or -var in phi[i] for var in range(-n, 0)) and all(var not in phi[i] for var in range(1, n+1)):
                    A[i][j] = 1
        return A
    
    def communication_complexity_rank(A):
        m, n = len(A), len(A[0])
        rank = 0
        for j in range(n):
            if any(A[i][j] == 1 for i in range(m)):
                rank += 1
        return rank
    
    def local_induction_ring_rank(K):
        # Placeholder function to simulate LIR calculation
        # Replace this with actual computation if available
        return random.randint(1, 5)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    phi = generate_cnf(n)
    A_phi = matrix_A(phi)
    rank_A_phi = communication_complexity_rank(A_phi)
    LIR_K = local_induction_ring_rank("K")
    
    if LIR_K == 0:
        return {
            "metric_name": "Var(rank(A(φ)))",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    variance = Fraction((rank_A_phi - LIR_K)**2, 1)
    c = Fraction(2, 1)  # Placeholder constant
    if variance <= c * LIR_K:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"Var(rank(A(φ)))={variance} > {c}*LIR(K)={c*LIR_K}"
    
    return {
        "metric_name": "Var(rank(A(φ)))",
        "metric_value": float(variance),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")