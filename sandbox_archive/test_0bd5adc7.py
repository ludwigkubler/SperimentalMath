# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from fractions import Fraction

def generate_formula(n, d, seed):
    random.seed(seed)
    if d == 2:
        return generate_balanced_formula(n, 2)
    elif d == 3:
        return generate_balanced_formula(n, 3)
    else:
        return generate_balanced_formula(n, 4)

def generate_balanced_formula(n, d):
    if d == 1:
        return random.choice(['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10'])[:n]
    else:
        left = generate_balanced_formula(n, d - 1)
        right = generate_balanced_formula(n, d - 1)
        op = random.choice(['AND', 'OR'])
        return f'({left} {op} {right})'

def compile_to_bp(formula):
    if formula.startswith('x'):
        return [('x', formula[1:])]
    elif formula.startswith('NOT'):
        return [('NOT', compile_to_bp(formula[4:-1]))]
    else:
        left = compile_to_bp(formula[1:formula.find(' ')])
        op = formula[formula.find(' ') + 1:formula.find(' ', formula.find(' ') + 1)]
        right = compile_to_bp(formula[formula.find(' ', formula.find(' ') + 1) + 1:-1])
        if op == 'AND':
            return left + right + [('AND', len(left), len(right))]
        else:
            return left + right + [('OR', len(left), len(right))]

def evaluate_bp(bp, x):
    stack = []
    for gate in bp:
        if gate[0] == 'x':
            stack.append(x[int(gate[1]) - 1])
        elif gate[0] == 'NOT':
            stack.append(not stack.pop())
        elif gate[0] == 'AND':
            a = stack.pop()
            b = stack.pop()
            stack.append(a and b)
        elif gate[0] == 'OR':
            a = stack.pop()
            b = stack.pop()
            stack.append(a or b)
    return stack[0]

def cycle_type(perm):
    cycles = []
    visited = set()
    for i in range(len(perm)):
        if i not in visited:
            cycle = []
            j = i
            while j not in visited:
                visited.add(j)
                cycle.append(j)
                j = perm[j]
            cycles.append(tuple(cycle))
    cycle_lengths = sorted(len(cycle) for cycle in cycles)
    return tuple(cycle_lengths)

def compute_mix(bp, n, seed):
    random.seed(seed)
    inputs = list(itertools.product([0, 1], repeat=n))
    L = len(bp)
    pi_star = {1: Fraction(119, 120), 2: Fraction(1, 120)}
    mix = 0
    for x in inputs:
        mu_t = [{} for _ in range(L)]
        current_perm = list(range(5))
        for t in range(L):
            gate = bp[t]
            if gate[0] == 'x':
                bit = x[int(gate[1]) - 1]
                if bit:
                    current_perm = [current_perm[1], current_perm[2], current_perm[3], current_perm[4], current_perm[0]]
                else:
                    current_perm = [current_perm[0], current_perm[2], current_perm[3], current_perm[4], current_perm[1]]
            elif gate[0] == 'NOT':
                current_perm = [current_perm[0], current_perm[1], current_perm[2], current_perm[3], current_perm[4]]
            elif gate[0] == 'AND':
                a = gate[1]
                b = gate[2]
                current_perm = [current_perm[0], current_perm[1], current_perm[2], current_perm[3], current_perm[4]]
            elif gate[0] == 'OR':
                a = gate[1]
                b = gate[2]
                current_perm = [current_perm[0], current_perm[1], current_perm[2], current_perm[3], current_perm[4]]
            cycle = cycle_type(current_perm)
            if cycle in mu_t[t]:
                mu_t[t][cycle] += 1
            else:
                mu_t[t][cycle] = 1
        for t in range(L):
            total = sum(mu_t[t].values())
            for cycle in mu_t[t]:
                mu_t[t][cycle] = Fraction(mu_t[t][cycle], total)
            distance = 0
            for cycle in mu_t[t]:
                if cycle in pi_star:
                    distance += abs(mu_t[t][cycle] - pi_star[cycle])
                else:
                    distance += mu_t[t][cycle]
            mix += distance
    mix /= (L * len(inputs))
    return mix

def run_trial(seed):
    random.seed(seed)
    n = random.choice([6, 8, 10])
    d = random.choice([2, 3, 4])
    formula = generate_formula(n, d, seed)
    bp = compile_to_bp(formula)
    L = len(bp)
    leaf_size = n
    mix = compute_mix(bp, n, seed)
    metric_value = mix * L
    log_leaf_size = math.log2(leaf_size)
    conjecture_holds = metric_value >= (1/8) * log_leaf_size
    counterexample = ""
    if not conjecture_holds:
        counterexample = f"MIX·L={metric_value} < (1/8)·log2(LeafSize)={log_leaf_size}"
    return {
        "metric_name": "MIX·L",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample,
        "log_leaf_size": log_leaf_size
    }

if __name__ == "__main__":
    seeds = sys.argv[1:] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    log_leaf_sizes = []
    conjecture_holds_count = 0
    first_failing_seed = None
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        log_leaf_sizes.append(result["log_leaf_size"])
        if result["conjecture_holds"]:
            conjecture_holds_count += 1
        else:
            if first_failing_seed is None:
                first_failing_seed = seed
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_count / len(seeds)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif first_failing_seed is not None:
        print(f"RESULT: FALSIFIED counterexample=\"MIX·L < (1/8)·log2(LeafSize)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")