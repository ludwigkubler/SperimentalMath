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
    
    def generate_tseitin_formula(n, m):
        variables = [f'x{i}' for i in range(1, n + 1)]
        clauses = []
        for i in range(m):
            clause = random.choice(variables)
            if random.choice([True, False]):
                clause += ' OR '
            else:
                clause += ' NOT '
            clause += random.choice(variables)
            clauses.append(clause)
        return variables, clauses
    
    def derive_equations(clauses):
        equations = set()
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                eq1 = clauses[i]
                eq2 = clauses[j]
                if ' OR ' in eq1 and ' OR ' in eq2:
                    new_eq = f'({eq1}) AND ({eq2})'
                    equations.add(new_eq)
        return equations
    
    def compute_quotient_algebra_rank(variables, derived_equations):
        # Simplified rank computation for demonstration
        return len(derived_equations) ** 0.5
    
    def resolution_proof_width(rank):
        # Simplified width computation for demonstration
        return rank
    
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    variables, clauses = generate_tseitin_formula(n, m)
    derived_equations = derive_equations(clauses)
    
    if not derived_equations:
        return {
            "metric_name": "Quotient Algebra Rank vs Resolution Proof Width",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    rank = compute_quotient_algebra_rank(variables, derived_equations)
    width = resolution_proof_width(rank)
    
    conjecture_holds = (rank >= math.log2(n) * m) and (width <= rank)
    counterexample = f"n={n}, m={m}, rank={int(rank)}, width={int(width)}"
    
    return {
        "metric_name": "Quotient Algebra Rank vs Resolution Proof Width",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result_str = f"SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result_str = f"FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}"
    
    print(result_str)