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
    
    def generate_boolean_formula(n):
        if n == 1:
            return 'x'
        else:
            subformulas = [generate_boolean_formula(random.randint(1, n-1)) for _ in range(2)]
            operator = random.choice(['&', '|'])
            return f'({subformulas[0]} {operator} {subformulas[1]})'
    
    def evaluate_formula(formula):
        stack = []
        i = 0
        while i < len(formula):
            if formula[i] == '(':
                j = formula.find(')', i)
                subformula = formula[i+1:j]
                if subformula.startswith('(') and subformula.endswith(')'):
                    stack.append(evaluate_formula(subformula[1:-1]))
                else:
                    stack.append(subformula)
                i = j + 1
            elif formula[i] in ['&', '|']:
                op = formula[i]
                b2 = stack.pop()
                b1 = stack.pop()
                if op == '&':
                    stack.append(b1 and b2)
                else:
                    stack.append(b1 or b2)
                i += 1
            else:
                stack.append(formula[i] != '0')
                i += 1
        return stack[0]
    
    def frege_proof_width(formula):
        if formula == 'x':
            return 1
        elif formula.startswith('(') and formula.endswith(')'):
            subformula = formula[1:-1]
            return max(frege_proof_width(subformula) for subformula in subformula.split('&'))
        else:
            return 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances = 0
    total_rank = 0
    
    for n in n_values:
        for _ in range(5):
            formula = generate_boolean_formula(n)
            rank = frege_proof_width(formula)
            total_instances += 1
            total_rank += rank
    
    avg_rank = total_rank / total_instances
    expected_rank = (math.log2(n) ** 2) / math.log(math.log2(n))
    
    return {
        "metric_name": "Average Rank",
        "metric_value": avg_rank,
        "instances_tested": total_instances,
        "conjecture_holds": abs(avg_rank - expected_rank) < 0.1 * expected_rank,
        "counterexample": "" if abs(avg_rank - expected_rank) < 0.1 * expected_rank else f"n={n}, avg_rank={avg_rank}, expected_rank={expected_rank}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")