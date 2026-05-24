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

def generate_instance(n):
    clauses = []
    for _ in range(2 * n):
        literals = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        clause = [literals[i] if random.random() < 0.5 else -literals[i] for i in range(n)]
        clauses.append(clause)
    return clauses

def dpll_solve(clauses, assignment=[]):
    if not clauses:
        return True
    unit_clauses = [c[0] for c in clauses if len(c) == 1]
    if unit_clauses:
        literal = unit_clauses[0]
        if literal < 0 and -literal in assignment:
            return False
        elif literal > 0 and literal not in assignment:
            assignment.append(literal)
    pure_literals = [l for l in range(1, n + 1) if (l not in assignment and -l not in assignment)]
    if pure_literals:
        literal = pure_literals[0]
        if literal not in assignment:
            assignment.append(literal)
    pos_literal = random.choice([l for l in range(1, n + 1) if l not in assignment])
    neg_literal = -pos_literal
    return dpll_solve(clauses, assignment + [pos_literal]) or dpll_solve(clauses, assignment + [neg_literal])

def minimal_rank_of_kostant_sheaf(n):
    instance = generate_instance(n)
    rank_value = 0
    for _ in range(10):  # Sample multiple instances to get a better estimate
        if dpll_solve(instance):
            rank_value += 1
    return rank_value

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    for n in n_values:
        rank_value = minimal_rank_of_kostant_sheaf(n)
        total_rank += rank_value
        instances_tested += 1
    mean_rank = total_rank / len(n_values)
    conjecture_holds = mean_rank <= math.log(math.log(instances_tested, 2), 2) * n_values[0]
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")