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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def smallest_prime_dividing(n):
        for i in range(2, n + 1):
            if n % i == 0 and is_prime(i):
                return i
        return n
    
    def generate_cnf(num_vars, num_clauses):
        cnf = []
        for _ in range(num_clauses):
            clause = [random.choice([-i, i]) for i in range(1, num_vars + 1)]
            random.shuffle(clause)
            cnf.append(tuple(clause))
        return cnf
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clauses = [c for c in cnf if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            return False
        pure_lits = {}
        for lit in set(lit for clause in cnf for lit in clause):
            pos_count, neg_count = sum(1 for c in cnf if lit in c), sum(1 for c in cnf if -lit in c)
            if pos_count == 0:
                pure_lits[lit] = True
            elif neg_count == 0:
                pure_lits[-lit] = True
        if pure_lits:
            literal = next(l for l, v in pure_lits.items() if v)
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            return False
        literals = list(set(lit for clause in cnf for lit in clause))
        literal = random.choice(literals)
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
            return True
        return False
    
    def log_q(num_vars):
        q = smallest_prime_dividing(num_vars)
        return math.log(q)
    
    n_max = 0
    instances_tested = 0
    total_length = 0
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(1, n * (n - 1) // 2))
            length = dpll(cnf)
            if length is None:
                counterexample = f"Failed to find DPLL proof for n={n}"
                break
            total_length += length
            instances_tested += 1
            n_max = max(n_max, n)
    
    metric_value = total_length / instances_tested if instances_tested > 0 else 0
    conjecture_holds = False
    
    return {
        "metric_name": "DPLL Proof Length",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(seeds) if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")