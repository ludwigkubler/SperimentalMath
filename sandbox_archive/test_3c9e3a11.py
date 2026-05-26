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
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for var in variables:
            clauses.append(f'{var} | ~{var}')
        return ' & '.join(clauses)

    def hodge_class_rank(n):
        # Placeholder function to simulate Hodge class rank computation
        # This is a dummy implementation and should be replaced with actual logic
        return n * (n + 1) // 2

    def tseitin_circuit_width(formula):
        # Placeholder function to simulate Tseitin circuit width computation
        # This is a dummy implementation and should be replaced with actual logic
        return len(formula.split(' & '))

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        formula = tseitin_formula(n)
        width = tseitin_circuit_width(formula)
        rank = hodge_class_rank(n)
        results.append({
            "metric_name": "hodge_class_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": rank >= n**2 / width**2 and rank <= 1.5 * n**2 / width**2,
            "counterexample": ""
        })

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    return {
        "seed": seed,
        "mean_rank": mean_rank,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [389, 421, 463, 503, 547, 593, 631, 677, 727, 773, 821, 877, 929]
    results = [run_trial(seed) for seed in seeds]

    print("TRIALS:")
    for result in results:
        print(f"TRIAL: {result}")

    mean_rank = sum(result["mean_rank"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.8) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=NA support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=NA first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")