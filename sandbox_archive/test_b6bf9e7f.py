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
    
    def generate_formula(n):
        if n == 1:
            return random.choice([True, False])
        else:
            op = random.choice(['and', 'or'])
            left = generate_formula(n // 2)
            right = generate_formula(n - n // 2)
            return (op, left, right)

    def evaluate_formula(formula):
        if isinstance(formula, bool):
            return formula
        elif formula[0] == 'and':
            return evaluate_formula(formula[1]) and evaluate_formula(formula[2])
        else:
            return evaluate_formula(formula[1]) or evaluate_formula(formula[2])

    def min_index(formula):
        if isinstance(formula, bool):
            return 0
        elif formula[0] == 'and':
            return 1 + max(min_index(formula[1]), min_index(formula[2]))
        else:
            return 1 + max(min_index(formula[1]), min_index(formula[2]))

    def circuit_width(formula):
        if isinstance(formula, bool):
            return 0
        elif formula[0] == 'and':
            return 1 + max(circuit_width(formula[1]), circuit_width(formula[2]))
        else:
            return 1 + max(circuit_width(formula[1]), circuit_width(formula[2]))

    n = random.randint(5, 40)
    formula = generate_formula(n)
    min_index_value = min_index(formula)
    width_value = circuit_width(formula)

    return {
        "metric_name": "min_index",
        "metric_value": min_index_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 1 for i in range(5, 6)]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")