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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(-n, n) for _ in range(3)]
            if 0 not in clause:
                cnf.append(clause)
        return cnf

    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            lit = unit_clause[0]
            if lit in assignment and assignment[lit] != (lit > 0):
                return False
            new_assignment = assignment.copy()
            new_assignment[lit] = True
            return dpll([c for c in cnf if not any(l in c or -l in c for l in new_assignment)], new_assignment)
        pure_literal = next((l for l in range(1, n + 1) if all(l not in c and -l not in c for c in cnf)), None)
        if pure_literal is not None:
            return dpll([c for c in cnf if not any(pure_literal in c or -pure_literal in c for l in assignment)], assignment)
        p = random.choice(cnf)
        lit, other_lit = p[0], -p[0]
        return dpll(cnf + [[other_lit]], assignment) or dpll(cnf + [[lit]], assignment)

    def quasi_frobenius_rank(cnf):
        n = len(set(abs(lit) for lit in cnf))
        if n == 1:
            return 1
        rank = 0
        while True:
            new_cnf = []
            for c in cnf:
                if any(lit not in assignment and -lit not in assignment for lit in c):
                    new_cnf.append(c)
            if len(new_cnf) == len(cnf):
                return rank + 1
            cnf = new_cnf
            rank += 1

    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    widths = []

    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(2 * n, 3 * n))
            rank = quasi_frobenius_rank(cnf)
            width = dpll(cnf)
            min_ranks.append(rank)
            widths.append(width)

    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(min_ranks, widths)) / math.sqrt(sum((x - mean_x)**2 for x in min_ranks) * sum((y - mean_y)**2 for y in widths))
    p_value = 2 * (1 - math.erf(abs(correlation_coefficient) * math.sqrt(len(min_ranks) - 2) / math.sqrt(2)))

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(min_ranks),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.7 and p_value <= 0.05,
        "counterexample": "" if correlation_coefficient > 0.7 and p_value <= 0.05 else "correlation_coefficient < 0.7 or p_value > 0.05"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_x = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_x)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_x} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7 or p_value > 0.05\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")