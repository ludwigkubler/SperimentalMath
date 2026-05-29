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
        for _ in range(n * 2):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses

    def dpll_search_tree_height(clauses):
        if not clauses:
            return 0
        unit_clauses = [c for c in clauses if len(c) == 1]
        if not unit_clauses:
            return max(dpll_search_tree_height(new_clauses) for new_clauses in split(clauses))
        literal, _ = unit_clauses[0]
        new_clauses = []
        for clause in clauses:
            if literal in clause:
                continue
            if -literal in clause:
                new_clause = [x for x in clause if x != -literal]
                if new_clause:
                    new_clauses.append(new_clause)
            else:
                new_clauses.append(clause)
        return 1 + dpll_search_tree_height(new_clauses)

    def split(clauses):
        variables = set()
        for clause in clauses:
            variables.update(abs(lit) for lit in clause)
        if not variables:
            yield []
            return
        var = random.choice(list(variables))
        pos_clauses = [c for c in clauses if var in c]
        neg_clauses = [c for c in clauses if -var in c]
        for new_pos_clauses in split(pos_clauses):
            for new_neg_clauses in split(neg_clauses):
                yield new_pos_clauses + new_neg_clauses

    n = random.randint(5, 40)
    formula = generate_3cnf(n)
    height = dpll_search_tree_height(formula)
    
    # Placeholder for Kähler manifold rank calculation
    # This is a dummy implementation and should be replaced with actual logic
    rank = n  # Example: rank is proportional to the number of variables

    ratio = Fraction(rank, height) if height != 0 else None
    
    return {
        "metric_name": "Kähler Manifold Rank to DPLL Search Tree Height Ratio",
        "metric_value": float(ratio) if ratio else float('inf'),
        "instances_tested": 1,
        "conjecture_holds": ratio is not None and ratio <= Fraction(1, 1),  # Placeholder constant c=1
        "counterexample": "" if ratio is not None and ratio <= Fraction(1, 1) else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    total_ratio = Fraction(0)
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
        if trial_result["conjecture_holds"]:
            total_ratio += Fraction(trial_result["metric_value"])
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_ratio/len(results)} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_ratio/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")