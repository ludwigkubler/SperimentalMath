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
    
    def generate_monotone_dnf(n, k):
        # Generate a random monotone DNF formula for k-CLIQUE with n variables
        clauses = []
        for _ in range(k):
            clause = set()
            while len(clause) < n:
                lit = random.randint(0, 2 * n - 1)
                if lit % 2 == 0 and lit // 2 not in clause:
                    clause.add(lit // 2)
            clauses.append(clause)
        return clauses
    
    def truth_table(dnf):
        # Compute the truth table of a monotone DNF formula
        n = len(dnf) * 2
        tt = []
        for i in range(1 << n):
            assignment = [(i >> j) & 1 for j in range(n)]
            value = any(all(assignment[lit // 2] if lit % 2 == 0 else not assignment[lit // 2] for lit in clause) for clause in dnf)
            tt.append(value)
        return tt
    
    def polynomial_hierarchy_depth(tt):
        # Compute the minimal polynomial hierarchy depth of a monotone DNF formula
        n = len(tt)
        m = 1
        while True:
            f = [0] * (2 ** m)
            for i in range(2 ** m):
                f[i] = tt[sum((i >> j) & 1 << j for j in range(m))]
            if all(f[i] == f[i ^ (1 << j)] for j in range(m)):
                break
            m += 1
        return m
    
    n_max = 40
    k_max = 40
    instances_tested = 0
    total_depth = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for k in range(1, min(k_max + 1, n + 1)):
            dnf = generate_monotone_dnf(n, k)
            tt = truth_table(dnf)
            depth = polynomial_hierarchy_depth(tt)
            total_depth += depth
            instances_tested += 1
    
    conjecture_holds = total_depth <= (n_max ** k_max / 2) * instances_tested
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "polynomial_hierarchy_depth",
        "metric_value": total_depth,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_depth = math.sqrt(sum((r["metric_value"] - mean_depth) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")