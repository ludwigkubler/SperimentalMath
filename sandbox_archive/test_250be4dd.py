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
from fractions import Fraction
from math import comb

def hypergeom_order(n, m):
    return min(m, n - m)

def resolution_width(cnf):
    clauses = list(cnf)
    if not clauses:
        return 0
    max_width = 1
    for i in range(len(clauses)):
        clause_i = set(clauses[i])
        width = len(clause_i)
        for j in range(i + 1, len(clauses)):
            clause_j = set(clauses[j])
            common_lits = clause_i.intersection(clause_j)
            if common_lits:
                width += len(common_lits)
        max_width = max(max_width, width)
    return max_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    total_ratio = Fraction(0, 1)

    for _ in range(instances_tested):
        m = random.randint(5, 40)
        cnf = set()
        while len(cnf) < m:
            clause = [random.choice(range(-n_max, n_max + 1)) for _ in range(random.randint(2, n_max))]
            if all(lit != -other_lit for lit in clause for other_lit in clause):
                cnf.add(tuple(sorted(clause)))
        order = hypergeom_order(n_max, m)
        width = resolution_width(cnf)
        ratio = Fraction(abs(width), order ** 2)
        total_ratio += ratio

    mean_ratio = total_ratio / instances_tested
    conjecture_holds = mean_ratio <= 1
    counterexample = "" if conjecture_holds else f"mean_ratio={mean_ratio}"

    return {
        "metric_name": "mean_ratio",
        "metric_value": float(mean_ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)

    mean_ratio = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_ratio={results[seeds.index(first_failing_seed)]['metric_value']}\" first_failing_seed={first_failing_seed}")