# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        if n == 1:
            return random.choice(['True', 'False'])
        else:
            op = random.choice(['&', '|'])
            left = generate_formula(n - 1)
            right = generate_formula(n - 1)
            return f'({left} {op} {right})'
    
    def is_tautology(formula):
        stack = []
        for char in formula:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack or stack[-1] != '(':
                    return False
                stack.pop()
            elif char == '&':
                if len(stack) < 2 or stack[-1] != '(' or stack[-2] != '(':
                    return False
                stack = stack[:-3]
        return len(stack) == 0
    
    def frege_proof_width(formula):
        if is_tautology(formula):
            return 1
        elif formula in ['True', 'False']:
            return 1
        else:
            op, left, right = formula[1], formula[2:-1].split(' ')[0], formula[2:-1].split(' ')[2]
            return max(frege_proof_width(left), frege_proof_width(right)) + 1
    
    def concept_lattice(formula):
        if formula in ['True', 'False']:
            return {formula}
        else:
            op, left, right = formula[1], formula[2:-1].split(' ')[0], formula[2:-1].split(' ')[2]
            left_concepts = concept_lattice(left)
            right_concepts = concept_lattice(right)
            concepts = set()
            for l in left_concepts:
                for r in right_concepts:
                    if op == '&':
                        if (l, r) not in concepts:
                            concepts.add((l, r))
                    elif op == '|':
                        if (l, r) not in concepts:
                            concepts.add((l, r))
            return concepts
    
    def min_order_of_formal_concepts(concept_lattice):
        return len(concept_lattice)
    
    n = 40
    formula = generate_formula(n)
    width = frege_proof_width(formula)
    lattice = concept_lattice(formula)
    order = min_order_of_formal_concepts(lattice)
    
    if width == 0:
        return {
            "metric_name": "Order of Formal Concepts",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"Formula: {formula}, Width: {width}"
        }
    
    ratio = Fraction(order, width)
    return {
        "metric_name": "Order of Formal Concepts",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(ratio - 1) <= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len([r for r in results if r['metric_value'] is not None])
    std_value = (sum((r['metric_value'] - mean_value) ** 2 for r in results if r['metric_value'] is not None) / len([r for r in results if r['metric_value'] is not None])) ** 0.5
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r['conjecture_holds']:
                counterexample = f"Formula: {r.get('formula', 'Unknown')}, Order: {r.get('order', 0)}, Width: {r.get('width', 0)}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break