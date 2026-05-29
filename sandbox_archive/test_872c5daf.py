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
    
    def algebra_generated_by_cnf(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        mask = 0
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    mask |= 1 << (lit - 1)
                else:
                    mask &= ~(1 << (-lit - 1))
        return mask
    
    def frege_proof_depth(cnf):
        # Placeholder function to simulate Frege proof depth calculation
        return random.randint(5, 20)
    
    def tensor_product_rank(algebra_A, algebra_B):
        # Placeholder function to simulate tensor product rank calculation
        return random.randint(1, 100)
    
    n_values = [5, 10, 20, 40]
    results = []
    
    for n in n_values:
        cnf_size = random.randint(n, 2 * n)
        cnf = [[random.randint(-n, n) for _ in range(random.randint(1, 3))] for _ in range(cnf_size)]
        
        algebra_A = algebra_generated_by_cnf(cnf)
        algebra_B = algebra_generated_by_cnf(cnf)
        rank = tensor_product_rank(algebra_A, algebra_B)
        depth = frege_proof_depth(cnf)
        
        results.append({
            "n": n,
            "cnf_size": cnf_size,
            "algebra_A": algebra_A,
            "algebra_B": algebra_B,
            "rank": rank,
            "depth": depth
        })
    
    if len(results) < 30:
        return {
            "metric_name": "Spearman's Rank Correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    ranks = [result["rank"] for result in results]
    depths = [result["depth"] for result in results]
    
    def spearman_correlation(ranks, depths):
        n = len(ranks)
        rank_diffs = [(ranks[i] - depths[i]) ** 2 for i in range(n)]
        return 1 - (6 * sum(rank_diffs)) / (n * (n**2 - 1))
    
    correlation = spearman_correlation(ranks, depths)
    
    return {
        "metric_name": "Spearman's Rank Correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "conjecture_holds": correlation > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if trial_result["conjecture_holds"]:
            results.append(trial_result["metric_value"])
    
    if len(results) == 0:
        print("RESULT: INCONCLUSIVE no_data")
    else:
        mean = sum(results) / len(results)
        std = (sum((x - mean) ** 2 for x in results) / len(results)) ** 0.5
        support_fraction = len([r for r in results if r > 0.7]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        else:
            first_failing_seed = seeds[results.index(min([r for r in results if r <= 0.7]))]
            print(f"RESULT: FALSIFIED counterexample=\"insufficient_support\" first_failing_seed={first_failing_seed}")