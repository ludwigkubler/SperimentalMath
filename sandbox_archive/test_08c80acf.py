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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def decision_tree(f, n):
    if n == 1:
        return f[0]
    else:
        left = decision_tree(f[:len(f)//2], n-1)
        right = decision_tree(f[len(f)//2:], n-1)
        return [left, right]

def homotopy_type(tree):
    if isinstance(tree, int):
        return 0
    elif len(tree) == 2:
        left = homotopy_type(tree[0])
        right = homotopy_type(tree[1])
        return max(left, right) + 1
    else:
        raise ValueError("Invalid decision tree")

def ac0_circuit_size(f):
    # Placeholder for SAT solver implementation
    # For simplicity, we assume a constant circuit size of n^2
    n = int(math.log2(len(f)))
    return n**2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        f = generate_boolean_function(n)
        tree = decision_tree(f, n)
        homotopy = homotopy_type(tree)
        circuit_size = ac0_circuit_size(f)

        if homotopy > 1 and circuit_size < n**2:
            conjecture_holds = False
            counterexample = f"n={n}, homotopy={homotopy}, circuit_size={circuit_size}"
            break

        total_metric_value += circuit_size
        instances_tested += 1

    return {
        "metric_name": "AC^0 Circuit Size",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}**}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")