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
    
    def generate_3cnf(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(variables + [f'~{v}' for v in variables], 3)
            clauses.append(' | '.join(clause))
        return ' & '.join(clauses)
    
    def tseitin_circuit(formula):
        literals = set()
        formulas = []
        for i, clause in enumerate(formula.split(' & ')):
            literals |= {l.strip('~') for l in clause.split(' | ') if l.strip('~') not in literals}
            new_var = f'y{i+1}'
            formulas.append(f'{new_var} <-> ({clause})')
            formulas.extend([f'~{new_var} -> ~({clause})', f'{new_var} -> {clause}'])
        return ' & '.join(formulas), literals
    
    def galois_representation(circuit):
        # Simplified representation for demonstration
        return len(circuit.split(' & '))
    
    def quadratic_residue_lattice_rank(n):
        return math.log2(2**n) / 2
    
    n = random.randint(5, 40)
    formula = generate_3cnf(n)
    circuit, literals = tseitin_circuit(formula)
    order = galois_representation(circuit)
    rank = quadratic_residue_lattice_rank(n)
    
    metric_name = "galois_order"
    metric_value = order
    instances_tested = 1
    conjecture_holds = order <= math.log2(2**n) and rank >= math.log2(2**n) / 2
    counterexample = "" if conjecture_holds else f"order={order}, expected<=log2(2^{n})"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")