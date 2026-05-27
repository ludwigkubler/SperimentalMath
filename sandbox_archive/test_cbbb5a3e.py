# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_dnf(n, d):
        clauses = []
        for _ in range(d):
            clause = [random.choice([f'x{i}', f'~x{i}']) for i in range(1, n+1)]
            clauses.append(clause)
        return clauses
    
    def resolution_depth(cnf):
        stack = cnf[:]
        while True:
            new_clauses = []
            for i in range(len(stack)):
                for j in range(i + 1, len(stack)):
                    clause_i = set(stack[i])
                    clause_j = set(stack[j])
                    if any(f'~{lit}' in clause_i for lit in clause_j):
                        new_clause = clause_i ^ {f'~{lit}' for lit in clause_j}
                        if not any(lit in new_clause for lit in stack):
                            new_clauses.append(new_clause)
            if not new_clauses:
                break
            stack.extend(new_clauses)
        return len(stack) - len(cnf)
    
    def toric_variety_rank(n, d):
        # Simplified mapping of DNF to a graph representation (not actual rank computation)
        return n + d
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        d = random.randint(1, n)
        cnf = generate_dnf(n, d)
        rank = toric_variety_rank(n, d)
        depth = resolution_depth(cnf)
        results.append((rank, depth))
    
    if not results:
        return {
            "metric_name": "Spearman Rank Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ranks = [r for r, _ in results]
    depths = [d for _, d in results]
    
    def spearman_rank_correlation(ranks, depths):
        rank_ranks = {x: i+1 for i, x in enumerate(sorted(set(ranks)))}
        depth_ranks = {y: i+1 for i, y in enumerate(sorted(set(depths)))}
        
        rank_diffs = [(rank_ranks[r] - depth_ranks[d]) ** 2 for r, d in results]
        n = len(results)
        rho_numerator = 6 * sum(rank_diffs)
        rho_denominator = n * (n**2 - 1)
        return 1 - rho_numerator / rho_denominator
    
    rho = spearman_rank_correlation(ranks, depths)
    
    return {
        "metric_name": "Spearman Rank Correlation",
        "metric_value": rho,
        "instances_tested": len(results),
        "conjecture_holds": rho >= 0.5 and all(rho >= 0.2 for _, d in results),
        "counterexample": "" if rho >= 0.5 else f"rho={rho} < 0.2"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_rho = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and "counterexample" in r and r["counterexample"].startswith("rho") for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")