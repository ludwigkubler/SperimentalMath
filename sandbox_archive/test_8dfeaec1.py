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
    
    def generate_xor_and_tree(n):
        if n == 1:
            return 'x'
        else:
            left = generate_xor_and_tree(n // 2)
            right = generate_xor_and_tree(n - n // 2)
            return f'({left} | {right})'

    def hodge_decomposition(tree):
        if tree[0] != '(' or tree[-1] != ')':
            raise ValueError("Invalid tree format")
        
        stack = []
        current = ""
        for char in tree:
            if char == '(':
                stack.append(current)
                current = ""
            elif char == ')':
                if not stack:
                    raise ValueError("Unbalanced parentheses")
                parent = stack.pop()
                current = f'({parent} | {current})'
            else:
                current += char
        
        if stack:
            raise ValueError("Unbalanced parentheses")
        
        return len(current.split(' | '))

    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        tree = generate_xor_and_tree(n)
        hodge_order = hodge_decomposition(tree)
        
        if hodge_order < math.ceil(n ** (1/3)) or hodge_order > math.floor(n ** (4/5)):
            return {
                "metric_name": "hodge_order",
                "metric_value": hodge_order,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"hodge_order={hodge_order}, expected=[{math.ceil(n ** (1/3))}, {math.floor(n ** (4/5))}]"
            }
        
        total_metric_value += hodge_order
        instances_tested += 1
    
    return {
        "metric_name": "hodge_order",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [37]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")