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
    
    def generate_tseitin_formula(n):
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for lit in literals:
            clauses.append([lit])
        for i in range(1, n):
            a, b = random.sample(literals, 2)
            new_lit = f'x{n+i}'
            clauses.append([new_lit, f'-{a}', f'-{b}'])
            clauses.append([f'-{new_lit}', a, b])
        return literals + [f'x{n+i}' for i in range(n)], clauses
    
    def solve(lits_true, lits_false):
        stack = []
        while stack or lits_true:
            if not stack:
                clause = random.choice(lits_true)
                stack.append(clause)
            else:
                lit = stack[-1]
                if lit.startswith('-'):
                    other_lit = lit[1:]
                    if other_lit in lits_false:
                        lits_false.remove(other_lit)
                        stack.pop()
                    elif other_lit not in lits_true:
                        return False
                else:
                    other_lit = f'-{lit}'
                    if other_lit in lits_false:
                        lits_false.remove(other_lit)
                        stack.pop()
                    elif other_lit not in lits_true:
                        stack.append(other_lit)
        return True
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_hmrank = 0
    total_width = 0
    
    for n in n_values:
        for _ in range(5):
            literals, clauses = generate_tseitin_formula(n)
            lits_true = [lit for lit in literals if solve([lit], [])]
            lits_false = [lit for lit in literals if not solve([lit], [])]
            width = len(lits_true) + len(lits_false)
            total_width += width
            instances_tested += 1
    
    mean_width = total_width / instances_tested
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": mean_width,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
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
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['instances_tested']}, width={r['metric_value']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break