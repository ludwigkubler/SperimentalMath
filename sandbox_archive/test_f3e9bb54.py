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
    
    def generate_formula(n):
        # Generate a random Boolean formula with n variables
        literals = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(literals + [f"~{lit}" for lit in literals], 2)
            clauses.append(" & ".join(clause))
        return " | ".join(clauses)

    def is_satisfiable(formula):
        # Check if the formula is satisfiable
        stack = []
        symbols = set()
        for token in formula.split():
            if token.startswith("~"):
                symbol = token[1:]
            else:
                symbol = token
            symbols.add(symbol)
            if len(stack) >= 2 and stack[-1] == "&" and stack[-3] == "~":
                if stack[-2] == symbol:
                    return True
                stack.pop()
                stack.pop()
                stack.pop()
        return False

    def compute_automorphism_group(formula):
        # Compute the automorphism group of the formula (simplified for demonstration)
        # This is a placeholder function; actual computation would be complex and not shown here
        return 1  # Placeholder value

    def prove_formula(formula):
        # Simulate proof length (placeholder function)
        # This is a placeholder function; actual proof system would be complex and not shown here
        return len(formula.split()) * 2  # Placeholder value

    if not is_satisfiable(generate_formula(5)):
        return {
            "metric_name": "proof_length",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable_formula"
        }

    results = []
    for _ in range(30):
        formula = generate_formula(5)
        aut_group = compute_automorphism_group(formula)
        proof_length = prove_formula(formula)
        results.append((aut_group, proof_length))

    mean_aut_group = sum(x[0] for x in results) / len(results)
    mean_proof_length = sum(x[1] for x in results) / len(results)

    correlation_coefficient = 0
    if mean_aut_group != 0 and mean_proof_length != 0:
        numerator = sum((x[0] - mean_aut_group) * (x[1] - mean_proof_length) for x in results)
        denominator = math.sqrt(sum((x[0] - mean_aut_group)**2 for x in results)) * math.sqrt(sum((x[1] - mean_proof_length)**2 for x in results))
        correlation_coefficient = numerator / denominator

    return {
        "metric_name": "proof_length",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": 5,
        "conjecture_holds": abs(correlation_coefficient) > 0.9 and all(abs(x[0] / x[1] - mean_aut_group / mean_proof_length) <= 5 for x in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")