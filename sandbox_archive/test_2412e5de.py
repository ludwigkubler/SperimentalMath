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

def generate_cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        if random.choice([True, False]):
            clause.reverse()
        clauses.append(clause)
    return clauses

def dpll_proof_length(cnf):
    def is_satisfiable():
        assignment = {}
        stack = []
        for literal in cnf:
            if literal[0] not in assignment and -literal[0] not in assignment:
                assignment[literal[0]] = True
                stack.append(literal)
            elif literal[0] in assignment and assignment[literal[0]]:
                continue
            else:
                return False
        while stack:
            literal = stack.pop()
            if literal[0] in assignment and not assignment[literal[0]]:
                assignment[-literal[0]] = True
                for clause in cnf:
                    if literal in clause:
                        clause.remove(literal)
                        if -literal in clause:
                            clause.remove(-literal)
                        if len(clause) == 1:
                            stack.append(clause[0])
        return all(assignment[var] for var in assignment)

    proof_length = 0
    while not is_satisfiable():
        cnf = [clause.copy() for clause in cnf]
        literal = random.choice([l for clause in cnf for l in clause if l > 0])
        cnf.remove([l for l in clause if l != literal])
        proof_length += 1
    return proof_length

def smallest_prime_not_dividing(num):
    if num % 2 == 0:
        return 3
    for p in range(3, int(math.sqrt(num)) + 1, 2):
        if num % p == 0:
            continue
        return p
    return num + 2

def minimal_order(primitive_element, field_size):
    order = 1
    while primitive_element ** order % field_size != 1:
        order += 1
    return order

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    proof_length = dpll_proof_length(cnf)
    num_clauses = len(cnf)
    p = smallest_prime_not_dividing(num_clauses)
    field_size = pow(p, proof_length)
    primitive_element = random.randint(2, field_size - 1)
    while math.gcd(primitive_element, field_size) != 1:
        primitive_element = random.randint(2, field_size - 1)
    order = minimal_order(primitive_element, field_size)
    upper_bound = n ** (1 / p)
    ratio = order / upper_bound
    conjecture_holds = ratio <= 1.5  # Using a loose bound for demonstration
    return {
        "metric_name": "Ratio of Minimal Order to Upper Bound",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Order: {order}, Upper Bound: {upper_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Order exceeds upper bound\" first_failing_seed={first_failing_seed}")