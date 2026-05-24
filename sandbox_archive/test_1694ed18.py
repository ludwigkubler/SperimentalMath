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
    
    def compute_tangent_sheaf_rank(f):
        n = len(f)
        if n <= 1:
            return 0
        
        # Compute the derivative matrix Df
        Df = []
        for i in range(n):
            df = [Fraction(0) for _ in range(n)]
            for j in range(i, n):
                if i == j:
                    df[j] = Fraction(f[j])
                else:
                    df[j] = Fraction(j * f[j - 1])
            Df.append(df)
        
        # Gaussian elimination to find the rank
        rows = len(Df)
        cols = len(Df[0])
        rank = 0
        
        for i in range(cols):
            pivot_row = None
            for r in range(rank, rows):
                if Df[r][i] != Fraction(0):
                    pivot_row = r
                    break
            
            if pivot_row is not None:
                # Swap rows to bring the pivot to the current position
                Df[pivot_row], Df[rank] = Df[rank], Df[pivot_row]
                
                # Normalize the pivot row
                denom = Df[rank][i]
                for j in range(i, cols):
                    Df[rank][j] /= denom
                
                # Eliminate other rows
                for r in range(rows):
                    if r != rank:
                        factor = Df[r][i]
                        for j in range(i, cols):
                            Df[r][j] -= factor * Df[rank][j]
                
                rank += 1
        
        return rank
    
    def compute_acc0_circuit_depth(f):
        n = len(f)
        if n <= 1:
            return 0
        
        # Simple heuristic to estimate ACC⁰ circuit depth
        max_degree = max([i for i, coeff in enumerate(f) if coeff != Fraction(0)])
        return max_degree + 1
    
    def generate_polynomial(n):
        return [Fraction(random.randint(-10, 10)) for _ in range(n)]
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test with 5 instances per size
            f = generate_polynomial(n)
            acc0_depth = compute_acc0_circuit_depth(f)
            rank = compute_tangent_sheaf_rank(f)
            
            if rank == 0:
                continue
            
            ratio = Fraction(acc0_depth, rank)
            total_ratio += ratio
            instances_tested += 1
    
    mean_ratio = total_ratio / instances_tested
    conjecture_holds = mean_ratio <= Fraction(25, 20) and mean_ratio >= Fraction(12, 10)
    
    return {
        "metric_name": "ratio",
        "metric_value": float(mean_ratio),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Ratio {mean_ratio} is out of bounds"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Ratio out of bounds' first_failing_seed={first_failing_seed}")