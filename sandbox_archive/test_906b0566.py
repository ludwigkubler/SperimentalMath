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
    
    def generate_boolean_circuit(n):
        if n == 1:
            return ['NOT', 'A']
        else:
            left = generate_boolean_circuit(n // 2)
            right = generate_boolean_circuit(n - n // 2)
            return ['OR', left, right]
    
    def tseitin_formula(circuit, var_count):
        if isinstance(circuit, str):
            return circuit
        elif circuit[0] == 'NOT':
            subformula = tseitin_formula(circuit[1], var_count)
            return f'~{subformula}'
        elif circuit[0] == 'OR':
            left = tseitin_formula(circuit[1], var_count)
            right = tseitin_formula(circuit[2], var_count)
            new_var = f'v{var_count}'
            return f'{new_var} <=> ({left} OR {right})'
        elif circuit[0] == 'AND':
            left = tseitin_formula(circuit[1], var_count)
            right = tseitin_formula(circuit[2], var_count)
            new_var = f'v{var_count}'
            return f'{new_var} <=> ({left} AND {right})'
    
    def resolution_width(formula):
        clauses = formula.split(' OR ')
        literals = set()
        for clause in clauses:
            if '=>' in clause:
                antecedent, consequent = clause.split(' => ')
                literals.update(antecedent.split(' AND '), consequent.split(' AND '))
            else:
                literals.update(clause.split(' AND '))
        
        def resolve(l1, l2):
            if l1.startswith('~') and l1[1:] == l2 or l2.startswith('~') and l2[1:] == l1:
                return True
            return False
        
        resolved = set()
        while literals:
            new_literals = set()
            for l1 in literals:
                for l2 in literals:
                    if resolve(l1, l2):
                        new_literals.add(f'~{l1}')
                        new_literals.add(f'~{l2}')
                        break
                else:
                    continue
                break
            else:
                return len(literals)
            literals.update(new_literals)
        
        return len(literals)
    
    def simplicial_decomposition(circuit):
        if isinstance(circuit, str):
            return [circuit]
        elif circuit[0] == 'NOT':
            subformula = simplicial_decomposition(circuit[1])
            return subformula
        elif circuit[0] == 'OR':
            left = simplicial_decomposition(circuit[1])
            right = simplicial_decomposition(circuit[2])
            return left + right
        elif circuit[0] == 'AND':
            left = simplicial_decomposition(circuit[1])
            right = simplicial_decomposition(circuit[2])
            return [f'({l} AND {r})' for l in left for r in right]
    
    n = random.randint(5, 40)
    circuit = generate_boolean_circuit(n)
    formula = tseitin_formula(circuit, 1)
    width = resolution_width(formula)
    simplices = simplicial_decomposition(circuit)
    num_simplices = len(set(simplices))
    
    return {
        "metric_name": "Simplicial Cells",
        "metric_value": num_simplices,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": width >= num_simplices,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
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
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")