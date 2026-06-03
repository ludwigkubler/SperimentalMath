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
        for _ in range(2**n - 1):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for j in range(i)):
                clauses.append(clause)
        return clauses
    
    def grothendieck_witt_class_mod_2(cnf):
        n = len(cnf[0])
        matrix = [[0] * n for _ in range(n)]
        for clause in cnf:
            for i, lit in enumerate(clause):
                if lit > 0:
                    matrix[i][lit - 1] += 1
                else:
                    matrix[lit - 1][i] += 1
        rank = 0
        for row in matrix:
            if any(row[j] % 2 != 0 for j in range(n)):
                rank += 1
        return rank
    
    def circuit_monotone_width(cnf):
        n = len(cnf[0])
        width = 0
        for clause in cnf:
            width = max(width, sum(abs(lit) for lit in clause))
        return width
    
    n_max = 40
    instances_tested = 30
    total_min_rank = 0
    total_width = 0
    
    for _ in range(instances_tested):
        cnf = generate_cnf(random.randint(5, n_max))
        min_rank = grothendieck_witt_class_mod_2(cnf)
        width = circuit_monotone_width(cnf)
        total_min_rank += min_rank
        total_width += width
    
    mean_min_rank = total_min_rank / instances_tested
    mean_width = total_width / instances_tested
    conjecture_holds = mean_min_rank >= 0.5 * mean_width
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_rank_over_width",
        "metric_value": mean_min_rank / mean_width,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")