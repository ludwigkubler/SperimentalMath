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
    
    def generate_tseitin_formula(n):
        variables = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clause = f"{variables[i-1]} | ~{variables[i-1]}"
            clauses.append(clause)
        return " & ".join(clauses)

    def compute_hodge_rank(width):
        # Placeholder function to simulate Hodge rank computation
        # This is a dummy implementation for the sake of testing
        return width ** 2

    n = random.randint(5, 40)
    formula = generate_tseitin_formula(n)
    width = len(formula.split(" & "))
    hodge_rank = compute_hodge_rank(width)

    metric_value = hodge_rank
    instances_tested = 1
    conjecture_holds = (hodge_rank >= n**2 / width**2) and (hodge_rank <= 1.5 * n**2 / width**2)
    counterexample = "" if conjecture_holds else f"rank={hodge_rank}, expected=Θ({n**2 / width**2})"

    return {
        "metric_name": "minimal_hodge_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes

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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"rank exceeded expected\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")