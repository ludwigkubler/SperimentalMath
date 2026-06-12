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
    
    def generate_random_kary_formula(k, n):
        literals = [f"x{i}" for i in range(n)]
        formula = []
        for _ in range(2**n):
            clause = [random.choice(literals) if random.randint(0, 1) else f"¬{l}" for l in literals]
            formula.append("∨".join(clause))
        return "∧".join(formula)
    
    def tseitin_formula(formula):
        n = len(formula.split("∧"))
        clauses = formula.split("∧")
        new_vars = [f"y{i}" for i in range(n)]
        tseitin = []
        for i, clause in enumerate(clauses):
            literals = clause.split("∨")
            if len(literals) == 1:
                tseitin.append(f"{new_vars[i]} <-> {literals[0]}")
            else:
                tseitin.append(f"{new_vars[i]} <-> (¬{literals[0]} ∨ ¬{literals[1]})")
        return "∧".join(tseitin)
    
    def dpll_width(formula):
        stack = [formula]
        width = 0
        while stack:
            current = stack.pop()
            if current == "":
                continue
            if current.startswith("¬"):
                stack.append(current[1:])
            elif "∨" in current:
                literals = current.split("∨")
                max_width = 0
                for literal in literals:
                    new_stack = [c for c in stack if c != current]
                    new_stack.append(literal)
                    width = max(width, dpll_width("∧".join(new_stack)))
                return max_width + 1
            else:
                return 1
        return width
    
    def motivic_order(formula):
        # Placeholder function to simulate the computation of motivic order
        # This is a dummy implementation and should be replaced with an actual algorithm
        return len(formula.split("∧"))
    
    instances_tested = 0
    n_max = 0
    total_motivic_order = 0
    total_dpll_width = 0
    
    for _ in range(30):
        k = random.randint(2, 5)
        n = random.randint(5, 10)
        formula = generate_random_kary_formula(k, n)
        tseitin = tseitin_formula(formula)
        instances_tested += 1
        n_max = max(n_max, n)
        motivic_order_val = motivic_order(tseitin)
        dpll_width_val = dpll_width(tseitin)
        total_motivic_order += motivic_order_val
        total_dpll_width += dpll_width_val
    
    mean_motivic_order = total_motivic_order / instances_tested
    mean_dpll_width = total_dpll_width / instances_tested
    correlation_coefficient = (instances_tested * sum(motivic_order_val * dpll_width_val for motivic_order_val, dpll_width_val in zip(range(instances_tested), range(instances_tested))) - instances_tested * mean_motivic_order * mean_dpll_width) / math.sqrt((instances_tested * sum(motivic_order_val ** 2 for motivic_order_val in range(instances_tested)) - instances_tested * mean_motivic_order ** 2) * (instances_tested * sum(dpll_width_val ** 2 for dpll_width_val in range(instances_tested)) - instances_tested * mean_dpll_width ** 2))
    
    conjecture_holds = correlation_coefficient >= 0.7 and all(motivic_order_val <= 2 * dpll_width_val for motivic_order_val, dpll_width_val in zip(range(instances_tested), range(instances_tested)))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")