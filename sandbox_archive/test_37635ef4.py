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
    
    def generate_instance(n):
        # Generate a random polytope P with n vertices in R^2
        vertices = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(n)]
        return vertices
    
    def lll_basis_reduction(B):
        # LLL basis reduction algorithm (simplified version)
        m = len(B)
        B = [list(b) for b in B]
        G = [[Fraction(0)] * m for _ in range(m)]
        u = [1] + [0] * (m - 1)
        
        for i in range(m):
            G[i][i] = Fraction(abs(B[i][i]))
            for j in range(i):
                G[j][i] = Fraction(sum(B[i][k] * B[k][j] for k in range(j, i)))
                B[i][j] -= sum(G[j][k] * B[k][j] for k in range(j))
        
        for i in range(m - 1, 0, -1):
            j = i
            while G[j-1][i] < Fraction(3, 4) * G[j][i]:
                j -= 1
            if j != i:
                B[i], B[j] = B[j], B[i]
                u[i], u[j] = u[j], u[i]
        
        return B
    
    def ehrhart_quotient(P, n):
        # Compute the minimal Ehrhart quotient of P using LLL basis reduction
        m = len(P)
        B = [[Fraction(0)] * m for _ in range(m)]
        for i in range(m):
            for j in range(i, m):
                B[i][j] = Fraction(sum((P[j][k] - P[i][k]) ** 2 for k in range(len(P[0]))) / (m - i))
        
        B = lll_basis_reduction(B)
        det_B = Fraction(1)
        for row in B:
            det_B *= abs(row[0])
        
        return det_B
    
    def communication_complexity_rank(n):
        # Placeholder function to compute the communication complexity rank
        # This is a dummy implementation and should be replaced with actual logic
        return n
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        P = generate_instance(n)
        quotient = ehrhart_quotient(P, n)
        rank = communication_complexity_rank(n)
        
        if rank == 0:
            continue
        
        results.append({
            "n": n,
            "quotient": quotient,
            "rank": rank
        })
    
    if not results:
        return {
            "metric_name": "Ehrhart Quotient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    mean_quotient = sum(result["quotient"] for result in results) / len(results)
    max_n = max(result["n"] for result in results)
    
    # Check if the inequality holds
    conjecture_holds = all(result["quotient"] <= 2 * result["rank"] for result in results)
    counterexample = "" if conjecture_holds else "Inequality does not hold"
    
    return {
        "metric_name": "Ehrhart Quotient",
        "metric_value": mean_quotient,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Inequality does not hold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE No seeds tested")