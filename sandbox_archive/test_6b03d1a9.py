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
    
    def xor_and_tree(n):
        if n == 1:
            return 'x'
        else:
            left = xor_and_tree(n // 2)
            right = xor_and_tree(n - n // 2)
            return f'({left} & {right}) | ({left} ^ {right})'

    def hodge_decomposition(tree):
        if tree == 'x':
            return [1]
        else:
            left, right = tree.split(' (')[1].split(') | ')[0], tree.split(' | ')[1].split(')')[0]
            left_hodge = hodge_decomposition(left)
            right_hodge = hodge_decomposition(right)
            return sorted(set(left_hodge + right_hodge))

    def mean_order(hodge_orders):
        return sum(hodge_orders) / len(hodge_orders)

    n_values = [5, 10, 15, 20, 30, 40]
    hodge_orders = []
    
    for n in n_values:
        tree = xor_and_tree(n)
        hodge_order = hodge_decomposition(tree)
        hodge_orders.extend(hodge_order)
    
    mean_order_value = mean_order(hodge_orders)
    Ω_n_1_3 = Fraction(n ** (1/3))
    O_n_4_5 = Fraction(n ** (4/5))
    
    conjecture_holds = Ω_n_1_3 <= mean_order_value <= O_n_4_5
    counterexample = "" if conjecture_holds else f"mean_order={mean_order_value}, expected=Ω({n}^{1/3}) to {O_n_4_5}"
    
    return {
        "metric_name": "mean_hodge_order",
        "metric_value": mean_order_value,
        "instances_tested": len(hodge_orders),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 73))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")