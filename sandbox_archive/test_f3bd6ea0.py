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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        clauses = set(tuple(sorted(clause)) for clause in cnf)
        width = 0
        while True:
            new_clauses = set()
            removed = False
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = tuple(sorted(list(set(clause1) ^ set(clause2))))
                        if new_clause not in clauses and new_clause not in new_clauses:
                            new_clauses.add(new_clause)
                            removed = True
            if not removed:
                break
            clauses.update(new_clauses)
            width += 1
        return width
    
    def hyperbolic_metric_entropy(cnf):
        n = len(set(abs(lit) for lit in sum(cnf, [])))
        m = len(cnf)
        if n == 0 or m == 0:
            return Fraction(0, 1)
        entropy = -m * math.log2(m / (n * (n - 1))) - (n - 1) * math.log2((n - 1) / (n * (n - 1)))
        return Fraction(entropy).limit_denominator()
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(1, n * 3))
            width = resolution_width(cnf)
            entropy = hyperbolic_metric_entropy(cnf)
            if width == 0 or entropy == Fraction(0, 1):
                continue
            results.append((n, width, entropy))
    
    if not results:
        return {
            "metric_name": "H(G(φ)) / w(φ)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(result[2] / result[1] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result[2] / result[1] >= 0.5) / len(results)
    
    return {
        "metric_name": "H(G(φ)) / w(φ)",
        "metric_value": mean,
        "instances_tested": len(results),
        "n_max": max(result[0] for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "not_enough_support"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(mean_values) / len(mean_values)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")