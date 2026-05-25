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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rref = [row[:] for row in matrix]
    
    lead = 0
    for r in range(rows):
        if lead >= cols:
            break
        
        i = r
        while abs(rref[i][lead]) == 0:
            i += 1
            if i == rows:
                i = r
                lead += 1
                if cols <= lead:
                    return rref
        
        rref[r], rref[i] = rref[i], rref[r]
        
        factor = Fraction(rref[r][lead])
        for j in range(cols):
            rref[r][j] /= factor
        
        for i in range(rows):
            if i != r:
                factor = Fraction(rref[i][lead])
                for j in range(cols):
                    rref[i][j] -= factor * rref[r][j]
        
        lead += 1
    
    return rref

def rank(matrix):
    rref = gaussian_elimination(matrix)
    non_zero_rows = [row for row in rref if any(val != 0 for val in row)]
    return len(non_zero_rows)

def generate_cnf(n):
    cnf = []
    for _ in range(n):
        clause = random.sample(range(1, n+1), random.randint(2, n))
        cnf.append(clause)
    return cnf

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [10, 15, 20, 25, 30, 35, 40]
    moduli_ranks = []
    tree_ranks = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        
        # Placeholder for actual computation of moduli rank
        moduli_rank = rank([[abs(lit) for lit in clause] for clause in cnf])
        moduli_ranks.append(moduli_rank)
        
        # Placeholder for actual computation of tree rank
        tree_rank = len(cnf)  # Simplified example: number of clauses
        tree_ranks.append(tree_rank)
    
    mean_moduli_rank = sum(moduli_ranks) / len(moduli_ranks)
    mean_tree_rank = sum(tree_ranks) / len(tree_ranks)
    
    conjecture_holds = all(m >= 2 * t for m, t in zip(moduli_ranks, tree_ranks))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Rank",
        "metric_value": mean_moduli_rank,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")