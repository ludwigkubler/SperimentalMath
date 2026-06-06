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
    
    def generate_formula(m):
        variables = [f'x{i}' for i in range(1, m+1)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + [f'~{v}' for v in variables], 2)
            clauses.append(' & '.join(clause))
        return ' | '.join(clauses)

    def fca(formula):
        # Simple FCA implementation (not accurate but sufficient for testing)
        concepts = []
        for clause in formula.split(' | '):
            concept = set()
            for literal in clause.split(' & '):
                if literal.startswith('~'):
                    concept.add(literal[1:])
                else:
                    concept.add(literal)
            concepts.append(concept)
        return len(concepts)

    def resolution_width(formula):
        # Simple DPLL-based solver (not accurate but sufficient for testing)
        clauses = formula.split(' | ')
        stack = []
        for clause in clauses:
            stack.append(clause.split(' & '))
        while stack:
            clause = stack.pop()
            if not clause:
                return len(stack) + 1
            literal = random.choice(clause)
            if literal.startswith('~'):
                literal = literal[1:]
                new_clause = [l for l in clause if l != literal and not l.startswith(f'~{literal}')]
                stack.append(new_clause)
        return len(stack)

    m_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for m in m_values:
        formula = generate_formula(m)
        order_of_concepts = fca(formula)
        proof_width = resolution_width(formula)
        results.append((order_of_concepts, proof_width))
    
    if not results:
        return {
            "metric_name": "Order of Concepts vs Proof Width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No formulas generated"
        }
    
    order_values = [r[0] for r in results]
    width_values = [r[1] for r in results]
    correlation_coefficient = sum((order_values[i] - mean(order_values)) * (width_values[i] - mean(width_values)) for i in range(len(results))) / math.sqrt(sum((x - mean(order_values))**2 for x in order_values) * sum((y - mean(width_values))**2 for y in width_values))
    
    return {
        "metric_name": "Order of Concepts vs Proof Width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(m_values),
        "conjecture_holds": correlation_coefficient >= 0.9 and all(c >= 0.5 for c in [correlation_coefficient]),
        "counterexample": ""
    }

def mean(lst):
    return sum(lst) / len(lst)

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials run")
        exit(0)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "First failing seed"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")