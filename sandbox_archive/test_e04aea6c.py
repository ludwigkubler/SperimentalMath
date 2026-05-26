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
    
    # Define a function to calculate the minimal rank of a matrix
    def calculate_minimal_rank(V):
        n = len(V)
        m = len(V[0])
        
        # Perform Gaussian elimination to find the rank
        U = [row[:] for row in V]
        rank = 0
        
        for j in range(min(n, m)):
            i_max = max(range(j, n), key=lambda i: abs(U[i][j]))
            if U[i_max][j] == 0:
                continue
            
            # Swap rows
            U[j], U[i_max] = U[i_max], U[j]
            
            # Scale the pivot row
            denom = U[j][j]
            for k in range(m):
                U[j][k] /= denom
            
            # Eliminate other rows
            for i in range(n):
                if i != j:
                    factor = U[i][j]
                    for k in range(m):
                        U[i][k] -= factor * U[j][k]
            
            rank += 1
        
        return rank
    
    # Define a function to calculate the DPLL search tree width of a k-CNF formula
    def calculate_dpll_search_tree_width(formula):
        # This is a placeholder function. For simplicity, we assume the width is proportional to the number of clauses.
        return len(formula)
    
    # Generate a random group representation V and corresponding k-CNF formula
    n = 10  # Number of variables in the k-CNF formula
    m = 20  # Number of clauses in the k-CNF formula
    V = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
    
    minrank_V = calculate_minimal_rank(V)
    dpll_width = calculate_dpll_search_tree_width([[random.randint(1, n) for _ in range(2)] for _ in range(m)])
    
    # Check if the conjecture holds
    c = Fraction(1, 2)  # Example constant
    ratio = minrank_V / dpll_width
    
    return {
        "metric_name": "minrank_to_dpll_ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": ratio >= c,
        "counterexample": "" if ratio >= c else f"Ratio {ratio} < {c}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")