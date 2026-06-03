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

def generate_tseitin_formula(n):
    if n == 1:
        return "A"
    else:
        A = "A" + str(n)
        B = "B" + str(n)
        C = "C" + str(n)
        formula = f"(~{A} & {B}) | (~{B} & {C})"
        for i in range(1, n):
            sub_formula = generate_tseitin_formula(i)
            formula = f"({formula} & ~{sub_formula})"
        return formula

def frege_proof_depth(formula):
    if formula == "A":
        return 1
    elif formula.startswith("(") and formula.endswith(")"):
        parts = formula[1:-1].split("&")
        max_depth = 0
        for part in parts:
            depth = frege_proof_depth(part)
            if depth > max_depth:
                max_depth = depth
        return 1 + max_depth
    else:
        return float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            formula = generate_tseitin_formula(n)
            depth = frege_proof_depth(formula)
            L_pi = len(formula.split("&"))
            if depth > L_pi:
                conjecture_holds = False
                counterexample = f"Formula: {formula}, Depth: {depth}, L(pi): {L_pi}"
                break
            total_metric_value += depth
            instances_tested += 1
        n_max = max(n_max, n)

    return {
        "metric_name": "Frege Proof Depth",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")