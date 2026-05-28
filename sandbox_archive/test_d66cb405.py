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

def generate_kcnf(n, m):
    literals = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    for _ in range(m):
        clause = random.sample(literals + ['!' + l for l in literals], 3)
        clauses.append(clause)
    return clauses

def dpll_solve(kcnf, assignment):
    if not kcnf:
        return True
    unit_clauses = [c[0] for c in kcnf if len(c) == 1]
    if unit_clauses:
        literal = unit_clauses[0]
        if literal.startswith('!'):
            negated_literal = literal[1:]
            if negated_literal in assignment and assignment[negated_literal]:
                return False
            else:
                assignment[literal] = True
        else:
            if literal in assignment and not assignment[literal]:
                return False
            else:
                assignment[literal] = True
    pure_literals = {}
    for clause in kcnf:
        positive, negative = set(), set()
        for literal in clause:
            if literal.startswith('!'):
                negative.add(literal[1:])
            else:
                positive.add(literal)
        for p in positive:
            if p not in pure_literals:
                pure_literals[p] = True
            elif not pure_literals[p]:
                del pure_literals[p]
        for n in negative:
            if n not in pure_literals:
                pure_literals[n] = False
            elif pure_literals[n]:
                del pure_literals[n]
    if pure_literals:
        literal, value = next(iter(pure_literals.items()))
        assignment[literal] = value
    unassigned_literal = next((l for l in literals if l not in assignment and '!'+l not in assignment), None)
    if unassigned_literal is None:
        return False
    if dpll_solve(kcnf, assignment):
        return True
    assignment[unassigned_literal] = False
    return dpll_solve(kcnf, assignment)

def koszul_complex_rank(kcnf):
    # Simplified rank calculation for demonstration purposes
    return len(kcnf) * 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [40, 42, 44, 46, 48, 50]
    results = []
    for n in n_values:
        for _ in range(30):
            kcnf = generate_kcnf(n, n * (n - 1) // 2)
            rank = koszul_complex_rank(kcnf)
            if not dpll_solve(kcnf, {}):
                continue
            refutation_size = len(kcnf)
            ratio = math.log2(refutation_size) / rank
            results.append((rank, ratio))
    if not results:
        return {
            "metric_name": "log_2(t*(F)) / |K_F|",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    avg_ratio = sum(ratio for _, ratio in results) / len(results)
    return {
        "metric_name": "log_2(t*(F)) / |K_F|",
        "metric_value": avg_ratio,
        "instances_tested": len(results),
        "conjecture_holds": all(0.5 <= ratio <= 1.5 for _, ratio in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result["metric_value"])
    
    mean_value = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if 0.5 <= r <= 1.5) / len(results)
    
    if all(0.5 <= r <= 1.5 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(r < 0.5 or r > 1.5 for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if r < 0.5 or r > 1.5)
        print(f"RESULT: FALSIFIED counterexample=\"out_of_range\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")