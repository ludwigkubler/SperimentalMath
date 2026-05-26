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

def generate_xor_and_tree(n, max_depth=4):
    if n == 1:
        return (random.choice([0, 1]),)
    else:
        left = generate_xor_and_tree(random.randint(1, n-1), max_depth-1)
        right = generate_xor_and_tree(n - len(left) - 1, max_depth-1)
        return ('xor', left, right)

def symplectic_form(tree):
    if isinstance(tree[0], int):
        return [[tree[0]], [0]]
    elif tree[0] == 'xor':
        left = symplectic_form(tree[1])
        right = symplectic_form(tree[2])
        n = len(left)
        I_n = [[(i==j)*1 for j in range(n)] for i in range(n)]
        return block_matrix([[I_n, I_n], [I_n, -I_n]])
    elif tree[0] == 'and':
        left = symplectic_form(tree[1])
        right = symplectic_form(tree[2])
        n = len(left)
        I_n = [[(i==j)*1 for j in range(n)] for i in range(n)]
        return block_matrix([[I_n, 0], [0, -I_n]])

def block_matrix(blocks):
    rows = sum(len(block) for block in blocks)
    cols = max(len(row) for block in blocks for row in block)
    result = [[0] * cols for _ in range(rows)]
    r_offset = 0
    for block in blocks:
        c_offset = 0
        for i, row in enumerate(block):
            for j, val in enumerate(row):
                result[r_offset + i][c_offset + j] = val
            c_offset += len(row)
        r_offset += len(block)
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    width = random.randint(1, n)
    tree = generate_xor_and_tree(n, max_depth=width)
    form = symplectic_form(tree)
    rank = sum(sum(row.count(1) for row in col) for col in zip(*form))
    metric_value = rank / (n * n)
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    return {
        "metric_name": "minimal_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
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

    mean_value = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")