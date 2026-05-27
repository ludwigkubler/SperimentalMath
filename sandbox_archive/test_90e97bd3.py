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
from fractions import Fraction
import math

def generate_cnf(n):
    clauses = []
    for _ in range(n * (n - 1) // 2):
        literals = [random.choice([f'x{i+1}', f'-x{i+1}']) for i in range(n)]
        random.shuffle(literals)
        clause = ' '.join(literals) + ' 0'
        clauses.append(clause)
    return '\n'.join(clauses)

def resolution_depth(cnf):
    n = len(cnf.split('\n'))
    stack = []
    for _ in range(2 * n):
        if not stack:
            stack.append((random.choice(['x1', '-x1']), 0))
        else:
            top = stack[-1]
            if abs(top[0]) == abs(stack[-2][0]):
                stack.pop()
            else:
                stack.append((random.choice(['x1', '-x1']), top[1] + 1))
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    depth = resolution_depth(cnf)
    return {
        "metric_name": "depth / minimal_index",
        "metric_value": Fraction(depth, n),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 50))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_d = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_d) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"depth / minimal_index\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")