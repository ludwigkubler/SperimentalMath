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
        clauses = []
        for _ in range(2 * n):
            clause = set(random.sample(range(1, n + 1), 3))
            if random.choice([True, False]):
                clause = {x: -1 for x in clause}
            clauses.append(clause)
        return clauses

    def dpll(cnf, assignment={}):
        unassigned_vars = [v for v in range(1, len(cnf) + 1) if v not in assignment]
        if not unassigned_vars:
            return all([any([assignment.get(x, False) == (c[x] > 0) for c in clause]) for clause in cnf])
        var = random.choice(unassigned_vars)
        for val in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[var] = val
            if dpll(cnf, new_assignment):
                return True
        return False

    def quantum_invariant(cnf):
        n = len(cnf)
        q_inv = 0
        for clause in cnf:
            for var in clause:
                if var > 0:
                    q_inv += math.log(1 + abs(var))
        return q_inv / n

    def resolution_width(cnf):
        queue = [c for c in cnf]
        while queue:
            c1 = queue.pop()
            for c2 in cnf:
                if len(c1) == 1 and len(c2) == 1 and abs(c1[0]) == abs(c2[0]):
                    continue
                new_clause = [x for x in c1 if x not in c2] + [x for x in c2 if -x not in c1]
                if not new_clause:
                    return len(queue)
                queue.append(new_clause)
        return len(queue)

    n_max = 0
    instances_tested = 0
    total_q_inv = 0
    total_width = 0

    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        cnf = generate_cnf(n)
        q_inv = quantum_invariant(cnf)
        width = resolution_width(cnf)
        total_q_inv += q_inv
        total_width += width
        instances_tested += 1

    mean_q_inv = total_q_inv / instances_tested
    mean_width = total_width / instances_tested
    correlation_coefficient = (instances_tested * mean_q_inv * mean_width - 
                               sum(q_inv * width for q_inv, width in zip([mean_q_inv] * instances_tested, [mean_width] * instances_tested))) / \
                              math.sqrt((instances_tested * mean_q_inv**2 - sum(q_inv**2 for q_inv in [mean_q_inv] * instances_tested)) *
                                        (instances_tested * mean_width**2 - sum(width**2 for width in [mean_width] * instances_tested)))

    conjecture_holds = correlation_coefficient > 0.8 and all([q_inv / width >= 0.5 for q_inv, width in zip([mean_q_inv] * instances_tested, [mean_width] * instances_tested)])
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")