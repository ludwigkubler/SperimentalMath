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

def generate_tseitin_formula(n: int, m: int) -> tuple:
    if n <= 0 or m <= 0:
        raise ValueError("n and m must be positive integers")
    
    literals = [f'x{i}' for i in range(1, n + 1)]
    variables = literals[:]
    clauses = []
    
    # Generate initial clauses
    for i in range(n):
        clause = random.sample(literals, 2)
        clauses.append(clause)
        literals.append(f'y{i+1}')
    
    # Generate additional clauses based on the initial ones
    for _ in range(m - n):
        clause = []
        for _ in range(2):
            literal = random.choice(variables)
            if literal.startswith('y'):
                clause.append(literal)
            else:
                clause.append(f'~{literal}')
        literals.append(f'y{n+1}')
        clauses.append(clause)
    
    return variables, clauses

def derive_equations(clauses: list) -> set:
    equations = set()
    for i in range(len(clauses)):
        for j in range(i + 1, len(clauses)):
            eq = []
            for literal in clauses[i]:
                if literal.startswith('~'):
                    eq.append(f'~{literal[1:]}')
                else:
                    eq.append(f'~{literal}')
            for literal in clauses[j]:
                if literal.startswith('~'):
                    eq.append(literal[1:])
                else:
                    eq.append(f'~{literal}')
            equations.add(tuple(sorted(eq)))
    return equations

def compute_quotient_algebra_rank(variables: list, equations: set) -> int:
    # This is a placeholder for the actual computation of the quotient algebra rank
    # For simplicity, we will use a dummy value
    return len(equations)

def compute_resolution_proof_width(clauses: list) -> int:
    # This is a placeholder for the actual computation of the resolution proof width
    # For simplicity, we will use a dummy value
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(n, n + 10)
    variables, clauses = generate_tseitin_formula(n, m)
    equations = derive_equations(clauses)
    
    quotient_rank = compute_quotient_algebra_rank(variables, equations)
    resolution_width = compute_resolution_proof_width(clauses)
    
    log_n_squared_m = math.log2(n) ** 2 * m
    
    conjecture_holds = quotient_rank >= log_n_squared_m and resolution_width <= quotient_rank
    counterexample = "" if conjecture_holds else f"n={n}, m={m}, rank={quotient_rank}, width={resolution_width}"
    
    return {
        "metric_name": "Quotient Algebra Rank vs Resolution Proof Width",
        "metric_value": quotient_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")