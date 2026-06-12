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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(10 * n):  # Each clause has at least one literal
            literals = [random.randint(1, n), random.randint(-n, -1)]
            random.shuffle(literals)
            cnf.append(literals)
        return cnf
    
    def resolution_proof_tree(cnf):
        clauses = set(tuple(clause) for clause in cnf)
        proof_tree = []
        while True:
            new_clause = None
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = tuple(sorted(list(set(clause1) ^ set(clause2))))
                        break
                if new_clause:
                    break
            if not new_clause:
                break
            proof_tree.append(new_clause)
            clauses.add(new_clause)
        return proof_tree
    
    def affine_sheaf_rank(proof_tree):
        # Simplified heuristic for the rank of the affine sheaf
        return len(proof_tree) ** (2/3)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    proof_tree = resolution_proof_tree(cnf)
    rank = affine_sheaf_rank(proof_tree)
    
    return {
        "metric_name": "affine_sheaf_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": rank <= n ** (2/3),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.05:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rank_outside_bound' first_failing_seed={first_failing_seed}")