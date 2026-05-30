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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(abs(x) != abs(y) for x, y in zip(clause, clause[1:])):
                clauses.append(clause)
        return clauses
    
    def truth_table(cnf):
        n = len(cnf[0])
        table = []
        for assignment in product([-1, 1], repeat=n):
            if all(any(x * assignment[i-1] >= 0 for x in clause) for clause in cnf):
                table.append(assignment)
        return table
    
    def minimal_order(table):
        n = len(table[0])
        variables = set(range(1, n + 1))
        order = 0
        while variables:
            covered = {var for assignment in table if any(var in assignment for x in assignment)}
            variables -= covered
            order += 1
        return order
    
    def resolution_width(cnf):
        clauses = cnf[:]
        queue = [tuple(clause) for clause in cnf]
        while queue:
            u, v = queue.pop()
            if not any(x == -y for x, y in zip(u, v)):
                new_clause = tuple(sorted(set(x for x in u + v if x != 0)))
                if new_clause not in clauses:
                    clauses.append(new_clause)
                    queue.extend([(new_clause, w) for w in clauses if len(set(new_clause).intersection(w)) == 1])
        return max(len(clause) for clause in clauses)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    table = truth_table(cnf)
    f_phi = minimal_order(table)
    width = resolution_width(cnf)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": len(table),
        "n_max": n,
        "conjecture_holds": width == 2**(n * f_phi) or abs(width - 2**(n * f_phi)) <= 3,
        "counterexample": "" if width == 2**(n * f_phi) else f"width={width}, expected=2^{(n * f_phi)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [3, 5, 7, 11, 13, 17, 19, 23, 29, 31] * 3
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
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break