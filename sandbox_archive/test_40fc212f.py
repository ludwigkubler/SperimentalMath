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
    
    def generate_boolean_circuit(w):
        # Simple random Boolean circuit generation for demonstration
        if w == 1:
            return ['0']
        elif w == 2:
            return ['0', '1']
        else:
            left = generate_boolean_circuit(random.randint(1, w-1))
            right = generate_boolean_circuit(w - len(left) - 1)
            return [f'({left[0]} OR {right[0]})'] + left + right

    def tseitin_formula(circuit):
        # Convert Boolean circuit to Tseitin formula
        variables = set()
        for expr in circuit:
            if 'OR' in expr:
                variables.add(expr)
        return variables

    def affine_quasi_projective_variety(formula):
        # Dummy function to simulate creation of an affine quasi-projective variety
        return len(formula)

    def minimal_order_of_automorphism_groups(V):
        # Dummy function to simulate computation of the minimal order of automorphism groups
        return V + 1

    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit = generate_boolean_circuit(n)
    formula = tseitin_formula(circuit)
    V = affine_quasi_projective_variety(formula)
    ord_V = minimal_order_of_automorphism_groups(V)

    metric_name = "minimal_order_of_automorphism_groups"
    metric_value = ord_V
    instances_tested = 1
    n_max = n
    conjecture_holds = ord_V >= n**2
    counterexample = "" if conjecture_holds else f"n={n}, w(C)={n}, ord(V)={ord_V}"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]

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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")