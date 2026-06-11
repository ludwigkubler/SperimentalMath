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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(random.randint(5, 10)):
            clause = [random.choice([-i, i]) for i in range(1, n+1)]
            cnf.append(clause)
        return cnf
    
    def evaluate_assignment(cnf, assignment):
        return all(any(l in assignment and assignment[l] for l in c) for c in cnf)
    
    def dpll_search_tree_width(cnf):
        def search(assignment, clauses_left):
            if not clauses_left:
                return 0
            clause = clauses_left[0]
            literals = [l for l in clause if abs(l) not in assignment]
            if not literals:
                return float('inf')
            literal = literals[0]
            new_assignment1 = assignment.copy()
            new_assignment1[literal] = True
            width1 = search(new_assignment1, clauses_left[1:])
            new_assignment2 = assignment.copy()
            new_assignment2[literal] = False
            width2 = search(new_assignment2, clauses_left[1:])
            return 1 + max(width1, width2)
        return search({}, cnf)
    
    def frobenius_coincidence_index(f):
        n = len(f)
        mci = float('inf')
        for i in range(1 << n):
            assignment = {j+1: (i >> j) & 1 for j in range(n)}
            if evaluate_assignment(cnf, assignment):
                count = sum(assignment[l] for l in f[i])
                mci = min(mci, abs(count - n / 2))
        return mci
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        cnf = generate_cnf(n)
        f = [[any(l in assignment and assignment[l] for l in c) for c in cnf] for _ in range(2 ** n)]
        mci = frobenius_coincidence_index(f)
        w = dpll_search_tree_width(cnf)
        results.append((mci, w))
    
    if not results:
        return {
            "metric_name": "Frobenius Coincidence Index vs DPLL Width",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No results generated"
        }
    
    mci_values, w_values = zip(*results)
    correlation_coefficient = sum((m - m_avg) * (w - w_avg) for m, w in zip(mci_values, w_values)) / math.sqrt(sum((m - m_avg) ** 2 for m in mci_values) * sum((w - w_avg) ** 2 for w in w_values))
    m_avg = sum(mci_values) / len(mci_values)
    w_avg = sum(w_values) / len(w_values)
    
    return {
        "metric_name": "Frobenius Coincidence Index vs DPLL Width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": abs(correlation_coefficient) > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "First failing seed"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")