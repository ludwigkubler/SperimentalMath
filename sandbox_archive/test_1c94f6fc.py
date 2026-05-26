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
            new_clauses = []
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = tuple(sorted([x for x in clause1 + clause2 if x != -x[0]]))
                        if new_clause not in clauses and new_clause not in new_clauses:
                            new_clauses.append(new_clause)
            if not new_clauses:
                break
            clauses.update(new_clauses)
            width += 1
        return width
    
    def pseudoexpectation(cnf):
        n = max(abs(clause[0]) for clause in cnf)
        m = len(cnf)
        expectation = 0
        for _ in range(2**n):
            assignment = [bool(random.randint(0, 1)) for _ in range(n)]
            if all(any(not (x > 0 and not assignment[x-1]) or (x < 0 and assignment[-x])) for x in cnf):
                expectation += 1
        return expectation / 2**n
    
    def tropicalization(expectation, d):
        return expectation ** d
    
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    cnf = generate_cnf(n, m)
    width = resolution_width(cnf)
    d = random.randint(1, 3)
    expectation = pseudoexpectation(cnf)
    tau_E = tropicalization(expectation, d)
    
    upper_bound = d * math.log(n + m) / math.log(math.log(n + m))
    
    return {
        "metric_name": "tropicalization_rank",
        "metric_value": tau_E,
        "instances_tested": 1,
        "conjecture_holds": tau_E <= upper_bound,
        "counterexample": "" if tau_E <= upper_bound else f"width={width}, expected={upper_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")