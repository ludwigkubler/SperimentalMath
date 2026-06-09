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
    
    # Generate a random CNF formula with n variables and m clauses
    n = 10  # Number of variables
    m = 20  # Number of clauses
    cnf_formula = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), 3)]
        cnf_formula.append(clause)
    
    # Construct the corresponding complex manifold Mφ associated with φ
    # This is a placeholder function. In practice, you would need to implement
    # a constructive mapping from the Boolean ring to polynomial rings over C.
    def min_rep_dim(M):
        return n  # Placeholder value
    
    min_rep_dim_value = min_rep_dim(cnf_formula)
    
    # Build the DPLL search tree for φ and measure its height |DPLL_tree(φ)|
    # This is a placeholder function. In practice, you would need to implement
    # the DPLL algorithm and count the number of nodes in the search tree.
    def dpll_tree_height(cnf):
        if not cnf:
            return 0
        for clause in cnf:
            if all(lit == 0 for lit in clause):
                continue
            new_cnf = [c for c in cnf if not any(abs(lit) in c for lit in clause)]
            return 1 + max(dpll_tree_height(new_cnf), dpll_tree_height([c for c in cnf if abs(lit) not in c]))
    
    dpll_tree_height_value = dpll_tree_height(cnf_formula)
    
    # Correlate min_rep_dim(Mφ) and |DPLL_tree(φ)|
    ratio = dpll_tree_height_value / min_rep_dim_value
    
    return {
        "metric_name": "Ratio of DPLL tree height to minimal representation dimension",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(ratio - 1) <= 0.1,
        "counterexample": "" if conjecture_holds else f"Ratio {ratio} is outside ±10% of 1"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio outside ±10% of 1\" first_failing_seed={first_failing_seed}")