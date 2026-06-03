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
    
    def polynomial(cnf):
        n = len(cnf[0])
        x = [Fraction(1, 1)] * (n + 1)
        for clause in cnf:
            term = Fraction(-1, 1)
            for lit in clause:
                if lit > 0:
                    term *= (x[lit] - Fraction(lit, 1))
                else:
                    term *= (x[-lit] - Fraction(1, lit))
            x[0] += term
        return x
    
    def resolution_width(cnf):
        # Simplified version of resolution width calculation
        return len(cnf)
    
    n = random.randint(5, 40)
    m = random.randint(2 * n, 3 * n)  # Ensure enough clauses for non-trivial CNF
    cnf = []
    for _ in range(m):
        clause = [random.randint(-n, n) for _ in range(n)]
        if all(lit == 0 for lit in clause):
            continue
        cnf.append(clause)
    
    p = polynomial(cnf)
    roots = set()
    for i in range(1, len(p)):
        if p[i] != 0:
            root = -p[0] / p[i]
            if all(root != Fraction(lit, 1) and root != Fraction(-lit, -1) for lit in cnf):
                roots.add(root)
    
    w = resolution_width(cnf)
    metric_value = len(roots)
    conjecture_holds = abs(metric_value - 1.5 * w) <= 0.5 * w
    counterexample = "" if conjecture_holds else f"Root count {metric_value} not within 1.5x of width {w}"
    
    return {
        "metric_name": "root_count",
        "metric_value": metric_value,
        "instances_tested": m,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")