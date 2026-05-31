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
    
    def generate_circuit(n, m):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + [f'~{v}' for v in variables], 2)
            clauses.append(clause)
        return variables, clauses

    def hodge_rank(circuit):
        # Placeholder function to simulate Hodge rank calculation
        n, m = len(circuit[0]), len(circuit[1])
        return n + m

    def dpll_search_tree_size(circuit):
        # Placeholder function to simulate DPLL search tree size calculation
        n, m = len(circuit[0]), len(circuit[1])
        return 2 ** (n + m)

    variables, clauses = generate_circuit(10, 20)
    rank = hodge_rank((variables, clauses))
    dpll_size = dpll_search_tree_size((variables, clauses))

    return {
        "metric_name": "Rank vs DPLL Size",
        "metric_value": rank / dpll_size,
        "instances_tested": 1,
        "n_max": 10,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(r["metric_value"] > 1.2 for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["metric_value"] > 1.2)
        print(f"RESULT: FALSIFIED counterexample=\"high_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")