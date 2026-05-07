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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def dpll(cnf, assignment):
    for clause in cnf:
        if all(lit not in assignment or assignment[lit] != val for lit, val in clause):
            return False
    return True

def random_3cnf(n, m):
    cnf = []
    variables = list(range(1, n + 1))
    for _ in range(m):
        literals = random.sample(variables * 2, 3)
        literals[0] *= -1 if random.choice([True, False]) else 1
        literals[1] *= -1 if random.choice([True, False]) else 1
        literals[2] *= -1 if random.choice([True, False]) else 1
        cnf.append(literals)
    return cnf

def resolution(cnf):
    clauses = set(tuple(sorted(clause)) for clause in cnf)
    while True:
        new_clauses = []
        for (a, b) in combinations(clauses, 2):
            if len(a & b) == 1:
                lit = a ^ b
                new_clause = list((set(a) | set(b)) - {lit})
                if not dpll([new_clause], {}):
                    new_clauses.append(tuple(sorted(new_clause)))
        if not new_clauses:
            break
        clauses.update(new_clauses)
    return len(clauses)

def build_dag(cnf, assignment):
    dag = {}
    for clause in cnf:
        for lit in clause:
            if lit not in assignment or assignment[lit] != 1:
                continue
            for other_lit in clause:
                if other_lit == lit:
                    continue
                if other_lit not in dag:
                    dag[other_lit] = []
                dag[other_lit].append(lit)
    return dag

def greedy_morse_matching(dag):
    unmatched_edges = set()
    for node in sorted(dag, key=lambda x: len(dag[x]), reverse=True):
        for neighbor in dag[node]:
            if neighbor not in dag:
                unmatched_edges.add((node, neighbor))
                break
    return len(unmatched_edges)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [10, 15, 20, 25, 30, 40]
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        m = math.floor(4.5 * n)
        unsat_count = 0

        while unsat_count < 30:
            cnf = random_3cnf(n, m)
            assignment = {}
            if not dpll(cnf, assignment):
                dag = build_dag(cnf, assignment)
                d_pi = resolution(cnf)
                M_F = greedy_morse_matching(dag)
                instances_tested += 1
                total_metric_value += M_F

                if M_F < d_pi - math.ceil(math.log2(len(dag))):
                    conjecture_holds = False
                    counterexample = f"n={n}, M(F)={M_F}, d(π)={d_pi}"

                unsat_count += 1

    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0.0
    return {
        "metric_name": "M(F)",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_metric_value = sum(result["metric_value"] for result in results if "metric_value" in result) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all("conjecture_holds" in result and result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction=1")
    elif any("counterexample" in result for result in results):
        first_failing_seed = next(result["seed"] for result in results if "counterexample" in result)
        print(f"RESULT: FALSIFIED counterexample=\"{next(result['counterexample'] for result in results if 'counterexample' in result)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")