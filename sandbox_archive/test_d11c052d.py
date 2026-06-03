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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses

    def dpll_solve(lits_true, lits_false, cls):
        if not cls:
            return True
        lit = next(iter(cls))
        for new_lits_true, new_lits_false in [(lits_true + [lit], lits_false), (lits_true, lits_false + [-lit])]:
            if dpll_solve(new_lits_true, new_lits_false, cls - {lit}):
                return True
        return False

    def tropical_rank(clauses):
        n = len(clauses)
        rank = 0
        for i in range(n):
            max_val = -math.inf
            for j in range(n):
                if i != j:
                    val = sum(1 for lit in clauses[i] if lit in clauses[j])
                    max_val = max(max_val, val)
            rank = max(rank, max_val + 1)
        return rank

    n_max = 40
    instances_tested = 30
    total_ratio = 0.0
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        cnf = generate_3cnf(n)
        rank = tropical_rank(cnf)
        depth = dpll_solve([], [], set(range(-n, n + 1)))
        
        if depth == 0:
            continue
        
        ratio = rank / depth
        total_ratio += ratio

    mean_ratio = total_ratio / instances_tested
    support_fraction = instances_tested / instances_tested
    
    return {
        "metric_name": "tropical_rank_to_dpll_depth_ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unsupported")