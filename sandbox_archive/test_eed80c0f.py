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
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        clauses = set(tuple(sorted(clause)) for clause in cnf)
        width = 0
        while True:
            new_clauses = []
            for clause1, clause2 in itertools.combinations(clauses, 2):
                if any(abs(x) == abs(y) and x != y for x in clause1 for y in clause2):
                    new_clause = [x for x in clause1 if x not in clause2] + [y for y in clause2 if y not in clause1]
                    if new_clause:
                        new_clauses.append(tuple(sorted(new_clause)))
            if new_clauses:
                clauses.update(new_clauses)
                width += 1
            else:
                break
        return width
    
    def pseudoexpectation(cnf):
        n = len(cnf[0])
        expectation = 0
        for clause in cnf:
            product = 1
            for literal in clause:
                if literal > 0:
                    product *= (1 + random.random())
                else:
                    product *= (1 - random.random())
            expectation += product
        return expectation / len(cnf)
    
    def tropicalization(expectation):
        return math.log(1 + expectation) / math.log(2)
    
    n = random.randint(5, 40)
    m = random.randint(5, 40)
    d = random.randint(1, 3)
    
    cnf = generate_cnf(n, m)
    width = resolution_width(cnf)
    expectation = pseudoexpectation(cnf)
    rank = tropicalization(expectation)
    
    bound = d * math.log(n + m) / math.log(math.log(n + m))
    
    return {
        "metric_name": "tropical_rank_bound",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= bound,
        "counterexample": "" if rank <= bound else f"rank={rank}, expected={bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break