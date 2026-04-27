# auto-injected by SEC sandbox
import math
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random

def bin_n(k, n):
    return format(k, f'0{n}b')

def truth_table_to_dfa(truth_table, n):
    states = {0}
    transitions = {}
    accepting_states = set()
    
    for k in range(2**n):
        if truth_table[k]:
            accepting_states.add(k)
    
    def add_transition(state, bit):
        new_state = 0
        for i in range(n):
            if (state >> i) & 1:
                new_state |= (bit << i)
            else:
                new_state |= ((1 - bit) << i)
        return new_state
    
    for state in states:
        for bit in [0, 1]:
            next_state = add_transition(state, bit)
            if next_state not in states:
                states.add(next_state)
            transitions[(state, bit)] = next_state
    
    return states, transitions, accepting_states

def hopcroft_minimization(states, transitions, accepting_states):
    worklist = list(accepting_states)
    non_accepting_states = states - accepting_states
    equivalent_classes = {frozenset(accepting_states), frozenset(non_accepting_states)}
    
    while worklist:
        current_class = worklist.pop()
        for bit in [0, 1]:
            new_class = set()
            for state in current_class:
                new_state = transitions[(state, bit)]
                if new_state in accepting_states:
                    new_class.add(state)
                else:
                    new_class.add(new_state)
            
            if len(new_class) > 1:
                for eq_class in equivalent_classes:
                    if new_class.issubset(eq_class):
                        continue
                    if any(x in new_class and y not in new_class or x not in new_class and y in new_class for x, y in eq_class):
                        new_eq_class = frozenset(eq_class - new_class).union(new_class)
                        equivalent_classes.remove(eq_class)
                        equivalent_classes.add(new_eq_class)
                        if new_eq_class in worklist:
                            worklist.remove(new_eq_class)
                        worklist.append(new_eq_class)
    
    return len(equivalent_classes)

def exhaustive_bottom_up_dp(n):
    literals = [f'x{i}' for i in range(1, n+1)] + [f'¬x{i}' for i in range(1, n+1)]
    formulas = set(literals)
    
    def is_formula(formula):
        if formula[0] == 'AND':
            return all(is_formula(arg) for arg in formula[1:])
        elif formula[0] == 'OR':
            return any(is_formula(arg) for arg in formula[1:])
        elif formula[0] == 'NOT':
            return is_formula(formula[1])
        else:
            return formula in literals
    
    def evaluate(formula, assignment):
        if formula[0] == 'AND':
            return all(evaluate(arg, assignment) for arg in formula[1:])
        elif formula[0] == 'OR':
            return any(evaluate(arg, assignment) for arg in formula[1:])
        elif formula[0] == 'NOT':
            return not evaluate(formula[1], assignment)
        else:
            if formula.startswith('x'):
                return assignment[int(formula[1:]) - 1]
            else:
                return not assignment[int(formula[2:]) - 1]
    
    def count_leaves(formula):
        if formula[0] == 'AND':
            return sum(count_leaves(arg) for arg in formula[1:])
        elif formula[0] == 'OR':
            return sum(count_leaves(arg) for arg in formula[1:])
        elif formula[0] == 'NOT':
            return count_leaves(formula[1])
        else:
            return 1
    
    def generate_formulas(n, k):
        if k == 1:
            return literals
        formulas = set()
        for f1 in generate_formulas(n, k-1):
            for f2 in generate_formulas(n, k-1):
                formulas.add(('AND', f1, f2))
                formulas.add(('OR', f1, f2))
        for f in literals:
            formulas.add(('NOT', f))
        return formulas
    
    for k in range(1, 2**n + 1):
        formulas.update(generate_formulas(n, k))
    
    min_formula = None
    min_leaves = float('inf')
    
    for formula in formulas:
        if is_formula(formula):
            assignment = [random.choice([True, False]) for _ in range(n)]
            if evaluate(formula, assignment):
                leaves = count_leaves(formula)
                if leaves < min_leaves:
                    min_leaves = leaves
                    min_formula = formula
    
    return min_leaves

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [2, 3, 4] + list(range(5, 9))
    results = []
    
    for n in n_values:
        if n == 2 or n == 3 or n == 4:
            truth_tables = [(i >> j) & 1 for i in range(2**n) for j in range(n)]
        else:
            truth_tables = [random.getrandbits(2**n) for _ in range(200)] + [
                sum(bin_n(k, n).count('1') % 2 == i for k in range(2**n)) for i in range(2)
            ] + [
                any(bin_n(k, n)[i] == '1' for i in range(n) if bin_n(k, n)[i+1:] == '0'*i) for _ in range(50)
            ] + [
                all(bin_n(k, n)[i] == '1' or bin_n(k, n)[i+1:] == '0'*i for i in range(n)) for _ in range(50)
            ] + [
                any(all(bin_n(k, n)[i] == '1' for i in range(j)) and all(bin_n(k, n)[i] == '0' for i in range(j+1, n)) for j in range(n-1)) for _ in range(50)
            ] + [
                any(all(bin_n(k, n)[i] == '1' or bin_n(k, n)[i+1:] == '0'*i for i in range(j)) and all(bin_n(k, n)[i] == '0' or bin_n(k, n)[i+1:] == '0'*i for i in range(j+1, n)) for j in range(n-1)) for _ in range(50)
            ]
        
        max_ratio = 0
        for truth_table in truth_tables:
            A_f = hopcroft_minimization(set(range(2**n)), truth_table_to_dfa(truth_table, n)[1], set())
            L_f = exhaustive_bottom_up_dp(n)
            ratio = A_f / ((n + 2) * L_f + 2)
            max_ratio = max(max_ratio, ratio)
        
        results.append({
            "metric_name": "max_ratio",
            "metric_value": max_ratio,
            "instances_tested": len(truth_tables),
            "conjecture_holds": max_ratio <= 1,
            "counterexample": "" if max_ratio <= 1 else f"n={n}, A(f)={(n+2)*L_f+2}, L(f)={L_f}"
        })
    
    return {
        "seed": seed,
        **results[-1]
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = (sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")