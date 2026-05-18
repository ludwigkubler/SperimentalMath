# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

def generate_formula(n, d, seed):
    random.seed(seed)
    if d == 1:
        return random.choice(['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10'])[:n]
    else:
        left = generate_formula(n, d-1, seed)
        right = generate_formula(n, d-1, seed+1)
        op = random.choice(['AND', 'OR'])
        return f"({left} {op} {right})"

def compile_to_bp(formula):
    if formula.startswith('x'):
        return [('x', formula)]
    elif formula.startswith('('):
        op = formula[formula.find(' ') + 1:formula.find(' ', formula.find(' ') + 1)]
        left = formula[1:formula.rfind(')')]
        right = formula[formula.rfind(')') + 2:-1]
        if op == 'AND':
            return compile_and(left, right)
        elif op == 'OR':
            return compile_or(left, right)
    else:
        return []

def compile_and(left, right):
    left_bp = compile_to_bp(left)
    right_bp = compile_to_bp(right)
    return left_bp + right_bp + [('AND',)]

def compile_or(left, right):
    left_bp = compile_to_bp(left)
    right_bp = compile_to_bp(right)
    return left_bp + right_bp + [('OR',)]

def evaluate_bp(bp, input_bits):
    stack = []
    for gate in bp:
        if gate[0] == 'x':
            stack.append(input_bits[int(gate[1][1:])-1])
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
    cycle_types = []
    for cycle in cycles:
        cycle_types.append(len(cycle))
    cycle_types.sort()
    return tuple(cycle_types)

def run_trial(seed):
    random.seed(seed)
    n = random.choice([6, 8, 10])
    d = random.choice([2, 3, 4])
    formula = generate_formula(n, d, seed)
    leaf_size = formula.count('x')
    bp = compile_to_bp(formula)
    L = len(bp)
    if L == 0:
        return {
            "metric_name": "MIX*L",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "empty BP"
        }

    pi_star = {1: 119/120, 2: 1/120, 3: 0, 4: 0, 5: 0}
    total_mix = 0.0
    instances_tested = 0

    for input_bits in itertools.product([0, 1], repeat=n):
        mu_t = defaultdict(int)
        current_perm = list(range(5))
        for t, gate in enumerate(bp):
            if gate[0] == 'x':
                bit = input_bits[int(gate[1][1:])-1]
                if bit:
                    current_perm = [current_perm[i-1] for i in range(1, 5)] + [current_perm[4]]
                else:
                    current_perm = [current_perm[i-1] for i in range(1, 5)] + [current_perm[4]]
            elif gate[0] == 'AND':
                current_perm = [current_perm[i-1] for i in range(1, 5)] + [current_perm[4]]
            elif gate[0] == 'OR':
                current_perm = [current_perm[i-1] for i in range(1, 5)] + [current_perm[4]]
            cycle_types = cycle_type(current_perm)
            mu_t[cycle_types] += 1
        total = sum(mu_t.values())
        for cycle_type in mu_t:
            mu_t[cycle_type] /= total
        mix = sum(abs(mu_t.get(cycle_type, 0) - pi_star.get(len(cycle_type), 0)) for cycle_type in mu_t)
        total_mix += mix
        instances_tested += 1

    if instances_tested == 0:
        return {
            "metric_name": "MIX*L",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "no instances tested"
        }

    mix_l = (total_mix / instances_tested) * L
    log_leaf_size = math.log2(leaf_size)
    conjecture_holds = mix_l >= (1/8) * log_leaf_size

    return {
        "metric_name": "MIX*L",
        "metric_value": mix_l,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"MIX*L={mix_l} < (1/8)*log2(LeafSize)={(1/8)*log_leaf_size}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        result["seed"] = seed
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing = next((r for r in results if not r["conjecture_holds"]), None)
        if first_failing:
            print(f"RESULT: FALSIFIED counterexample=\"{first_failing['counterexample']}\" first_failing_seed={first_failing['seed']}")
        else:
            print("RESULT: INCONCLUSIVE reason=no_failing_instances")