# auto-injected by SEC sandbox
import itertools
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import json
from collections import defaultdict

def build_decision_tree(f, n):
    # Build the canonical decision tree T_f* using DP on partial assignments
    # Each state is represented as a tuple of (var, val) pairs
    memo = {}

    def dp(state):
        if state in memo:
            return memo[state]

        # Check if all variables are fixed
        fixed_vars = {var for var, _ in state}
        if len(fixed_vars) == n:
            # Leaf node: evaluate the function on the fixed assignment
            assignment = [0] * n
            for var, val in state:
                assignment[var] = val
            return (1, (assignment, assignment))  # (min_leaf_count, (left_serial, right_serial))

        # Find the smallest unfixed variable
        for var in range(n):
            if var not in fixed_vars:
                break

        # Recursively build the left and right subtrees
        left_state = state + ((var, 0),)
        right_state = state + ((var, 1),)
        left_count, left_serial = dp(left_state)
        right_count, right_serial = dp(right_state)

        # Choose the child with the smallest min_leaf_count, with lex tie-break
        if left_count < right_count:
            min_count = left_count
            serial = (left_serial, right_serial)
        elif right_count < left_count:
            min_count = right_count
            serial = (right_serial, left_serial)
        else:
            # Tie-break on serialized tree shapes
            if left_serial < right_serial:
                min_count = left_count
                serial = (left_serial, right_serial)
            else:
                min_count = right_count
                serial = (right_serial, left_serial)

        memo[state] = (min_count + 1, serial)
        return memo[state]

    _, tree = dp(())
    return tree

def compute_rrd(tree):
    # Compute the right-rotation rank (rrd) of the decision tree
    if isinstance(tree, tuple) and len(tree) == 2 and isinstance(tree[0], tuple) and isinstance(tree[1], tuple):
        left_leaves = compute_rrd(tree[0])
        right_leaves = compute_rrd(tree[1])
        return left_leaves + right_leaves + abs(left_leaves - right_leaves)
    else:
        return 1

def construct_matrix(f, n):
    # Construct the matrix M[a,b] = f(a XOR b)
    size = 1 << n
    matrix = []
    for a in range(size):
        row = []
        for b in range(size):
            xor = a ^ b
            row.append(f[xor])
        matrix.append(row)
    return matrix

def rank_f2(matrix):
    # Compute the rank of the matrix over F2 using Gaussian elimination
    if not matrix:
        return 0

    rows = len(matrix)
    cols = len(matrix[0])
    rank = 0

    for col in range(cols):
        # Find the pivot row
        pivot = -1
        for row in range(rank, rows):
            if matrix[row][col] == 1:
                pivot = row
                break

        if pivot == -1:
            continue

        # Swap the current row with the pivot row
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]

        # Eliminate this column in all other rows
        for row in range(rows):
            if row != rank and matrix[row][col] == 1:
                for c in range(col, cols):
                    matrix[row][c] ^= matrix[rank][c]

        rank += 1

    return rank

def run_trial(seed):
    random.seed(seed)
    n = random.choice([4, 5, 6, 7])
    f = [random.randint(0, 1) for _ in range(1 << n)]

    # Build the decision tree and compute rrd
    tree = build_decision_tree(f, n)
    rrd = compute_rrd(tree)

    # Construct the matrix and compute its rank over F2
    matrix = construct_matrix(f, n)
    rank = rank_f2(matrix)

    # Compute the ratio
    if rrd >= 4:
        ratio = math.log2(rank) / math.log2(1 + rrd)
    else:
        ratio = 1.0  # Default value when rrd < 4

    # Determine if the conjecture holds
    conjecture_holds = ratio >= 0.25 if rrd >= 4 else True
    counterexample = f"rrd={rrd}, ratio={ratio}" if not conjecture_holds and rrd >= 4 else ""

    return {
        "metric_name": "log2(rank_F2(M)) / log2(1 + rrd(T_f*))",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample,
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    metric_values = []
    conjecture_holds_counts = 0
    total_instances = 0
    first_failing_seed = None

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps({'seed': seed, **result})}")
        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            conjecture_holds_counts += 1
        total_instances += result["instances_tested"]
        if not result["conjecture_holds"] and first_failing_seed is None:
            first_failing_seed = seed

    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0.0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0.0
    support_fraction = conjecture_holds_counts / len(seeds) if seeds else 0.0

    if first_failing_seed is not None:
        print(f'RESULT: FALSIFIED counterexample="{result["counterexample"]}" first_failing_seed={first_failing_seed}')
    elif support_fraction >= 0.8:
        print(f'RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}')
    else:
        print('RESULT: INCONCLUSIVE reason=insufficient_support')