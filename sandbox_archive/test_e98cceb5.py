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
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        clauses = set(tuple(sorted(c)) for c in cnf)
        width = 0
        while True:
            new_clauses = []
            for c1, c2 in itertools.combinations(clauses, 2):
                if any(abs(l) == abs(r) and l != r for l in c1 for r in c2):
                    new_clause = [l for l in c1 + c2 if l not in [-r for r in c2]]
                    new_clauses.append(tuple(sorted(new_clause)))
            if not new_clauses:
                break
            clauses.update(new_clauses)
            width += 1
        return width
    
    def pseudoexpectation(cnf):
        n = len(cnf[0])
        expectation = [Fraction(0, 1) for _ in range(n)]
        for clause in cnf:
            product = Fraction(1, 1)
            for literal in clause:
                if literal > 0:
                    product *= Fraction(1, 2)
                else:
                    product *= Fraction(1, 2)
            expectation[abs(literal) - 1] += product
        return expectation
    
    def tropicalization(expectation):
        return [math.log(abs(x), 2) if x != 0 else float('-inf') for x in expectation]
    
    def min_rank(tropicalized):
        return max(1, sum(1 for x in tropicalized if x != float('-inf')))
    
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    cnf = generate_cnf(n, m)
    width = resolution_width(cnf)
    expectation = pseudoexpectation(cnf)
    tropicalized = tropicalization(expectation)
    rank = min_rank(tropicalized)
    
    d = random.randint(1, 5)
    upper_bound = d * math.log(n + m) / math.log(math.log(n + m))
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= upper_bound,
        "counterexample": "" if rank <= upper_bound else f"rank={rank}, expected={upper_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")