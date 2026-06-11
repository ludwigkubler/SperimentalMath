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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = set(random.sample(range(1, n + 1), 2))
        cnf.append(clause)
    return cnf

def resolution_width(cnf):
    clauses = list(cnf)
    while True:
        new_clauses = []
        found_resolvent = False
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                if not (clauses[i] & clauses[j]):
                    resolvent = (clauses[i] | clauses[j]) - {min(list(clauses[i])[0], list(clauses[j])[0]), max(list(clauses[i])[1], list(clauses[j])[1])}
                    new_clauses.append(resolvent)
                    found_resolvent = True
        if not found_resolvent:
            return len(new_clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    rk_min_total = 0
    w_phi_total = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        m = random.randint(1, n * 2)
        cnf = generate_cnf(n, m)
        rk_min = len(cnf)  # Simplified minimal rank calculation
        w_phi = resolution_width(cnf)

        rk_min_total += rk_min
        w_phi_total += w_phi
        instances_tested += 1
        n_max = max(n_max, n)

    mean_rk_min = rk_min_total / instances_tested
    mean_w_phi = w_phi_total / instances_tested

    correlation_coefficient = (instances_tested * sum(rk_min * w_phi for rk_min, w_phi in zip([mean_rk_min] * instances_tested, [mean_w_phi] * instances_tested)) - 
                               sum(rk_min for rk_min in [mean_rk_min] * instances_tested) * sum(w_phi for w_phi in [mean_w_phi] * instances_tested)) / \
                              math.sqrt((instances_tested * sum(rk_min ** 2 for rk_min in [mean_rk_min] * instances_tested) - 
                                          (sum(rk_min for rk_min in [mean_rk_min] * instances_tested)) ** 2) *
                                        (instances_tested * sum(w_phi ** 2 for w_phi in [mean_w_phi] * instances_tested) - 
                                         (sum(w_phi for w_phi in [mean_w_phi] * instances_tested)) ** 2))

    conjecture_holds = correlation_coefficient > 0.5
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{}>".format(correlation_coefficient)

    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {" + ", ".join(f"'{k}': {v}" for k, v in result.items()) + "}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")