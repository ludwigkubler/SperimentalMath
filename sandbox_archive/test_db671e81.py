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
        cnf = []
        for _ in range(random.randint(10, 20)):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            cnf.append(clause)
        return cnf
    
    def is_power_of_two(x):
        return x > 0 and (x & (x - 1)) == 0
    
    def qcr_mod_2k(cnf, k):
        factors = [0] * len(cnf)
        for clause in cnf:
            for lit in clause:
                if abs(lit) <= 2**k:
                    factors[abs(lit) - 1] += 1
        return all(f % 2 == 0 for f in factors)
    
    def resolution_width(cnf):
        clauses = set(tuple(sorted(clause)) for clause in cnf)
        width = 0
        while len(clauses) > 1:
            new_clauses = []
            for c1, c2 in itertools.combinations(clauses, 2):
                resolvents = set()
                for lit in c1:
                    if -lit in c2:
                        resolvent = tuple(sorted(set(c1) ^ {lit} | set(c2) ^ {-lit}))
                        resolvents.add(resolvent)
                new_clauses.extend(resolvents)
            clauses.update(new_clauses)
            width += 1
        return width
    
    n_max = 0
    instances_tested = 0
    total_rpw = 0
    count_rpw_le_12n = 0
    count_rpw_ge_n = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        cnf = generate_cnf(n)
        if qcr_mod_2k(cnf, 10):  # Assuming k=10 is sufficient for our purposes
            rpw = resolution_width(cnf)
            instances_tested += 1
            n_max = max(n_max, n)
            total_rpw += rpw
            if rpw <= 1.2 * n:
                count_rpw_le_12n += 1
            if rpw >= n:
                count_rpw_ge_n += 1
    
    metric_value = total_rpw / instances_tested
    conjecture_holds = (count_rpw_le_12n >= 0.5 * instances_tested) and (rpw <= 1.5 * n)
    counterexample = "" if conjecture_holds else "resolution_width_too_large"
    
    return {
        "metric_name": "Resolution Proof Width",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rpw = sum(r["metric_value"] for r in results) / len(results)
    std_rpw = math.sqrt(sum((r["metric_value"] - mean_rpw) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rpw} std={std_rpw} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"resolution_width_too_large\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support_fraction")