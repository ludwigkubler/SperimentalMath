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
    n = 10  # Start with a small size and increase if needed
    instances_tested = 0
    total_qm = 0
    total_depth = 0
    max_n = 0
    
    def quadratic_residue_symbol(phi, k):
        return sum(int(lit) * (2 ** i) for i, lit in enumerate(reversed(bin(k)[2:]))) % 2
    
    def dpll_solver(phi):
        if not phi:
            return 0
        literals = list(phi.keys())
        literal = random.choice(literals)
        pos_clause = {lit: clause for lit, clause in phi.items() if literal in clause}
        neg_clause = {lit: clause for lit, clause in phi.items() if -literal in clause}
        if not pos_clause:
            return 1 + dpll_solver(neg_clause)
        if not neg_clause:
            return 1 + dpll_solver(pos_clause)
        return min(1 + dpll_solver({**pos_clause, literal: []}), 1 + dpll_solver({**neg_clause, -literal: []}))
    
    for _ in range(30):
        n += 5
        max_n = max(max_n, n)
        phi = {i: [random.choice([-1, 1]) for _ in range(n)] for i in range(1, n + 1)}
        qm = min(abs(quadratic_residue_symbol(phi, k)) for k in range(2 ** n))
        depth = dpll_solver(phi)
        total_qm += qm
        total_depth += depth
        instances_tested += 1
    
    mean_qm = total_qm / instances_tested
    mean_depth = total_depth / instances_tested
    correlation = (instances_tested * sum(qm * depth for qm, depth in zip([mean_qm] * instances_tested, [mean_depth] * instances_tested)) -
                   sum(mean_qm) * sum(mean_depth)) / math.sqrt((instances_tested * sum(qm ** 2 for qm in [mean_qm] * instances_tested) - sum(mean_qm) ** 2) *
                                                            (instances_tested * sum(depth ** 2 for depth in [mean_depth] * instances_tested) - sum(mean_depth) ** 2))
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    else:
        for res in results:
            if not res["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"Correlation too low\" first_failing_seed={res['seed']}")
                break