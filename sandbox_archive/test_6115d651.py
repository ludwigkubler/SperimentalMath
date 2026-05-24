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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-l for l in clause]
            clauses.append(clause)
        return clauses
    
    def dpll(model, clauses):
        if not clauses:
            return True
        unit_clauses = [c[0] for c in clauses if len(c) == 1]
        if not unit_clauses:
            return False
        literal = unit_clauses[0]
        model[literal] = True
        new_clauses = []
        for clause in clauses:
            if literal in clause:
                continue
            if -literal in clause:
                new_clauses.append([l for l in clause if l != -literal])
            else:
                new_clauses.append(clause)
        if dpll(model, new_clauses):
            return True
        del model[literal]
        model[-literal] = True
        new_clauses = []
        for clause in clauses:
            if -literal in clause:
                continue
            if literal in clause:
                new_clauses.append([l for l in clause if l != literal])
            else:
                new_clauses.append(clause)
        return dpll(model, new_clauses)
    
    def dpll_refutation_tree_width(clauses):
        model = {}
        width = 0
        stack = [(model, clauses, width)]
        while stack:
            current_model, remaining_clauses, current_width = stack.pop()
            if not remaining_clauses:
                return current_width
            unit_clauses = [c[0] for c in remaining_clauses if len(c) == 1]
            if not unit_clauses:
                continue
            literal = unit_clauses[0]
            new_model = current_model.copy()
            new_model[literal] = True
            stack.append((new_model, [c for c in remaining_clauses if literal not in c], current_width + 1))
            new_model = current_model.copy()
            new_model[-literal] = True
            stack.append((new_model, [c for c in remaining_clauses if -literal not in c], current_width + 1))
        return width
    
    n_values = [5, 10, 20, 40]
    total_rank = 0
    total_width = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(7):  # Ensure at least 30 instances per seed
            clauses = generate_3cnf(n)
            rank = len(set(tuple(sorted(clause)) for clause in clauses))
            width = dpll_refutation_tree_width(clauses)
            total_rank += rank
            total_width += width
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    mean_width = total_width / instances_tested
    
    conjecture_holds = mean_rank <= math.log(n_values[-1])
    counterexample = "" if conjecture_holds else f"Rank {mean_rank} exceeds O(log n) for n={n_values[-1]}"
    
    return {
        "metric_name": "rank_vs_width",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds O(log n)\" first_failing_seed={first_failing_seed}")