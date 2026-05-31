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
        clause = [random.randint(1, n), -random.randint(1, n)]
        if random.choice([True, False]):
            clause[0] *= -1
        if random.choice([True, False]):
            clause[1] *= -1
        cnf.append(clause)
    return cnf

def resolution_width(cnf):
    clauses = set(tuple(sorted(clause)) for clause in cnf)
    width = 0
    while True:
        new_clauses = []
        added = False
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                if -clauses[i][0] in clauses[j]:
                    new_clause = tuple(sorted(set(clauses[i]) | set(clauses[j]) - {-clauses[i][0]}))
                    if new_clause not in clauses:
                        new_clauses.append(new_clause)
                        added = True
        if not added:
            break
        clauses.update(new_clauses)
        width += 1
    return width

def hyperbolic_metric_entropy(cnf):
    n = len(set(abs(lit) for clause in cnf for lit in clause))
    m = len(cnf)
    if n <= 1 or m == 0:
        return Fraction(0, 1)
    entropy = -m * math.log2(m / (n * (n - 1))) - (n - 1) * math.log2((n - 1) / (n * (n - 1)))
    return Fraction(entropy).limit_denominator()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        instances_tested = 0
        total_entropy = Fraction(0, 1)
        total_width = 0
        for _ in range(5):  # 5 instances per size
            cnf = generate_cnf(n, random.randint(2 * n, 3 * n))
            entropy = hyperbolic_metric_entropy(cnf)
            width = resolution_width(cnf)
            if width == 0:
                continue
            total_entropy += entropy / width
            total_width += width
            instances_tested += 1
        if instances_tested > 0:
            avg_entropy_per_width = total_entropy / instances_tested
            results.append(avg_entropy_per_width)
    metric_value = sum(results) / len(results) if results else Fraction(0, 1)
    conjecture_holds = all(x >= Fraction(1, 2) for x in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "H(G(φ)) / w(φ)",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= Fraction(1, 2)) / len(results)
    if all(r >= Fraction(1, 2) for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r < Fraction(1, 2) for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if r < Fraction(1, 2)))]
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")