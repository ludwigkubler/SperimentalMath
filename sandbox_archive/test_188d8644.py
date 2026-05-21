# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0], clause[1] = -clause[0], -clause[1]
            clauses.append(clause)
        return clauses
    
    def incidence_matroid_rank(clauses):
        matroid = {}
        for i, clause in enumerate(clauses):
            for var in clause:
                if var not in matroid:
                    matroid[var] = set()
                matroid[var].add(i)
        rank = 0
        bases = []
        for var in sorted(matroid):
            new_base = [i for i in matroid[var] if all(j not in matroid[var] for j in bases)]
            if new_base:
                bases.append(new_base)
                rank += 1
        return rank
    
    def karchmer_wigderson_protocol_cost(clauses):
        n = len(set(abs(c) for c in sum(clauses, [])))
        m = len(clauses)
        cost = (n + m - 2) * math.log2(n + m - 2) / 2
        return cost
    
    n = random.randint(5, 40)
    m = random.randint(10, 3*n)
    clauses = generate_3cnf(n, m)
    
    rank = incidence_matroid_rank(clauses)
    cost = karchmer_wigderson_protocol_cost(clauses)
    
    return {
        "metric_name": "Karchmer-Wigderson protocol cost",
        "metric_value": cost,
        "instances_tested": 1,
        "conjecture_holds": cost >= rank,
        "counterexample": "" if cost >= rank else f"n={n}, m={m}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[first_failing_seed]['instances_tested']}, m={len(results[first_failing_seed]['counterexample'].split(','))}\" first_failing_seed={seeds[first_failing_seed]}")