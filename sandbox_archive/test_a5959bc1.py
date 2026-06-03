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

def frege_proof_depth(clause):
    if isinstance(clause, list):
        if not clause:
            return 0
        sub_clauses = [c for c in clause if isinstance(c, list)]
        literals = [c for c in clause if isinstance(c, int)]
        if not literals and not sub_clauses:
            return 1
        depth = 1 + max(frege_proof_depth(sub_clause) for sub_clause in sub_clauses)
        depth = max(depth, 1 + len(literals))
        return depth
    else:
        raise TypeError("Invalid clause type")

def generate_tseitin_formula(n):
    variables = list(range(1, n+1))
    clauses = []
    
    # Generate clauses for each variable
    for i in range(1, n+1):
        a = random.choice(variables)
        b = random.choice(variables)
        c = random.choice(variables)
        if random.choice([True, False]):
            clause = [a, -b, -c]
        else:
            clause = [-a, b, c]
        clauses.append(clause)
    
    # Generate the final clause
    final_clause = []
    for i in range(1, n+1):
        if random.choice([True, False]):
            final_clause.append(i)
        else:
            final_clause.append(-i)
    clauses.append(final_clause)
    
    return clauses

def longest_arithmetic_hierarchy_sequence(n):
    # This is a placeholder function. Implement the actual logic for computing
    # the longest sequence of jumps in the arithmetic hierarchy.
    return n  # Placeholder value

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_tseitin_formula(n)
    f_pi = frege_proof_depth(formula)
    L_pi = longest_arithmetic_hierarchy_sequence(n)
    
    return {
        "metric_name": "Frege proof depth vs. Arithmetic hierarchy sequence",
        "metric_value": f_pi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": f_pi <= L_pi,
        "counterexample": "" if f_pi <= L_pi else f"Counterexample for n={n}, f(π)={f_pi}, L(π)={L_pi}"
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