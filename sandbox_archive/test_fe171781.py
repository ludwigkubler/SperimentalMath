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
    
    def generate_tseitin_formula(depth):
        if depth == 1:
            return random.choice(['A', 'B'])
        else:
            p = generate_tseitin_formula(random.randint(1, depth-1))
            q = generate_tseitin_formula(random.randint(1, depth-1))
            return f'({p} & {q}) | ({p} -> {random.choice(["A", "B"])}'

    def tseitin_resolution_tree(formula):
        # Simplified version of Tseitin resolution tree generation
        if formula.isalpha():
            return [formula]
        elif formula.startswith('(') and formula.endswith(')'):
            parts = formula[1:-1].split()
            if len(parts) == 3:
                p, op, q = parts
                if op == '&':
                    return tseitin_resolution_tree(p) + tseitin_resolution_tree(q)
                elif op == '|':
                    return tseitin_resolution_tree(f'~{p}') + tseitin_resolution_tree(f'~{q}')
        return []

    def geometric_quantization_rank(tree):
        # Simplified version of geometric quantization rank calculation
        if not tree:
            return 0
        else:
            return max(geometric_quantization_rank(subtree) for subtree in tree) + 1

    depth = random.randint(5, 40)
    formula = generate_tseitin_formula(depth)
    tree = tseitin_resolution_tree(formula)
    rank = geometric_quantization_rank(tree)

    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank >= 2**(0.4 * depth)
    counterexample = f'Depth {depth}, Rank {rank}' if not conjecture_holds else ''

    return {
        "metric_name": "geometric_quantization_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*2 + 1, 2))  # Default to first 30 primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Depth {results[0]['counterexample'].split(',')[1]}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")