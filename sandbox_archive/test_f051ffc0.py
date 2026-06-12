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
    
    def generate_instance(n):
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(literals, 2)
            clauses.append(f"({clause[0]} | {clause[1]})")
        return " & ".join(clauses)

    def dpll(instance):
        literals = set()
        for literal in instance.split():
            if literal.startswith('x'):
                literals.add(literal)
        
        def solve(model, clause):
            if not clause:
                return True
            literal = clause[0]
            if literal.startswith('~'):
                literal = literal[1:]
                if literal in model and model[literal]:
                    return solve(model, clause[2:])
                elif literal not in model:
                    model[literal] = False
                    if solve(model, clause[2:]):
                        return True
                    del model[literal]
            else:
                if literal in model and not model[literal]:
                    return solve(model, clause[2:])
                elif literal not in model:
                    model[literal] = True
                    if solve(model, clause[2:]):
                        return True
                    del model[literal]
            return False
        
        for literal in literals:
            model = {literal: True}
            if solve(model, instance):
                return len(model)
        
        return float('inf')

    def quasi_classical_function_order(instance):
        # Placeholder function to simulate the order of a quasi-classical function
        # This is a dummy implementation and should be replaced with actual computation
        n = len(instance.split())
        return n * (n - 1) // 2

    n_max = 40
    instances_tested = 30
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        instance = generate_instance(n)
        m_phi = quasi_classical_function_order(instance)
        w_phi = dpll(instance)
        
        if m_phi < n**3 or m_phi > 10 * n**(3/2):  # Placeholder constant c=10
            conjecture_holds = False
            counterexample = f"n={n}, m(φ)={m_phi}, w(φ)={w_phi}"
        
        total_metric_value += m_phi

    mean_metric_value = total_metric_value / instances_tested
    std_deviation = (sum((x - mean_metric_value)**2 for x in range(instances_tested)) / instances_tested)**0.5

    return {
        "metric_name": "quasi_classical_function_order",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_deviation = (sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_deviation} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")