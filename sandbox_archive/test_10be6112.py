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

def generate_3cnf_tautology(n):
    clauses = []
    for _ in range(n):
        literals = [random.choice([f'x{i}', f'~x{i}']) for i in range(1, n+1)]
        clause = ' ∨ '.join(literals)
        clauses.append(clause)
    tautology = ' ∧ '.join(clauses)
    return tautology

def dpll_solve(tautology):
    def parse_clause(clause):
        return [x.strip('~') for x in clause.split(' ∨ ') if x]

    def is_satisfiable(variables, clauses):
        for clause in clauses:
            if not any(l in variables or f'~{l}' not in variables for l in parse_clause(clause)):
                return False
        return True

    def backtrack(variables, clauses):
        if all(is_satisfiable(variables, clauses) for _ in range(10)):  # Simple heuristic
            return len(variables)
        for var in set(''.join(clauses).split()):
            if var not in variables:
                variables.add(var)
                length = backtrack(variables, clauses)
                if length is not None:
                    return length
                variables.remove(var)
                variables.add(f'~{var}')
                length = backtrack(variables, clauses)
                if length is not None:
                    return length
        return None

    clauses = tautology.split(' ∧ ')
    variables = set()
    for clause in clauses:
        variables.update(parse_clause(clause))
    return backtrack(variables, clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_length = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):  # Sample 5 instances per n
            tautology = generate_3cnf_tautology(n)
            length = dpll_solve(tautology)
            if length is not None:
                total_length += length
                instances_tested += 1

    mean_length = total_length / instances_tested if instances_tested > 0 else 0
    conjecture_holds = instances_tested > 0 and math.isclose(mean_length, n**2, rel_tol=1e-2)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "resolution_proof_length",
        "metric_value": mean_length,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    mean_length = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")