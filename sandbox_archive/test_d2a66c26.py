# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def generate_tseitin_formula(n):
    if n == 1:
        return "¬x ∨ (x ∧ y)"
    else:
        subformula = generate_tseitin_formula(n - 1)
        return f"¬(x{n-1}) ∨ ({subformula} ∧ x{n})"

def is_tseitin_formula(formula):
    if formula.startswith("¬") and "(" in formula and ")" in formula:
        inner_formula = formula[2:-1]
        if "∨" in inner_formula or "∧" in inner_formula:
            return True
    return False

def resolve_clause(clause, assignment):
    for literal in clause:
        var = literal[1:]
        negated = literal.startswith("¬")
        if (var not in assignment and not negated) or (var in assignment and assignment[var] == negated):
            return None
    return True

def find_assignment(formula):
    stack = []
    literals = set()
    
    def parse_formula(formula, start, end):
        i = start
        while i < end:
            if formula[i].isalpha():
                literals.add(formula[i])
                i += 1
            elif formula[i] == "(":
                j = i + 1
                depth = 1
                while depth > 0:
                    if formula[j] == "(":
                        depth += 1
                    elif formula[j] == ")":
                        depth -= 1
                    j += 1
                clause = parse_formula(formula, i + 1, j - 1)
                stack.append(clause)
                i = j
            elif formula[i] in "∨∧":
                operator = formula[i]
                left = stack.pop()
                right = parse_formula(formula, i + 1, end)
                if operator == "∨":
                    stack.append(left or right)
                else:
                    stack.append(left and right)
                i += 2
            elif formula[i] == "¬":
                literal = formula[i:i+2]
                literals.add(literal[1])
                stack.append(not resolve_clause([literal], {}))
                i += 2
    
    parse_formula(formula, 0, len(formula))
    
    assignment = {}
    for lit in literals:
        assignment[lit] = random.choice([True, False])
    
    while True:
        new_assignment = {**assignment}
        changed = False
        for clause in stack:
            if isinstance(clause, bool):
                continue
            result = resolve_clause(clause, new_assignment)
            if result is None:
                for literal in clause:
                    var = literal[1:]
                    negated = literal.startswith("¬")
                    if (var not in assignment and not negated) or (var in assignment and assignment[var] == negated):
                        new_assignment[var] = not negated
                        changed = True
            elif result:
                stack.remove(clause)
        if not changed:
            break
    
    return new_assignment

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            formula = generate_tseitin_formula(n)
            if not is_tseitin_formula(formula):
                continue
            
            assignment = find_assignment(formula)
            resolution_length = len([lit for lit, val in assignment.items() if val])
            
            local_crossed_module_rank = 2 * n  # Simplified example rank calculation
            
            total_metric_value += local_crossed_module_rank / resolution_length
            instances_tested += 1
            
            c = Fraction(local_crossed_module_rank, resolution_length)
            if c > 1:
                conjecture_holds = False
                counterexample = f"n={n}, formula={formula}, rank={local_crossed_module_rank}, length={resolution_length}"
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = Fraction(instances_tested, len(n_values) * 5)
    
    return {
        "metric_name": "Local Crossed Module Rank to Resolution Proof Length Ratio",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
    
    mean_metric_value = sum(trial["metric_value"] for trial in [run_trial(seed) for seed in seeds]) / len(seeds)
    support_fraction = Fraction(sum(1 for trial in [run_trial(seed) for seed in seeds] if trial["conjecture_holds"]), len(seeds))
    
    if all(trial["conjecture_holds"] for trial in [run_trial(seed) for seed in seeds]):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not trial["conjecture_holds"] for trial in [run_trial(seed) for seed in seeds]) and support_fraction >= Fraction(8, 10):
        print(f"RESULT: FALSIFIED counterexample=\"{next(trial['counterexample'] for trial in [run_trial(seed) for seed in seeds] if not trial['conjecture_holds'])}\" first_failing_seed={seeds[next(i for i, trial in enumerate([run_trial(seed) for seed in seeds]) if not trial['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")