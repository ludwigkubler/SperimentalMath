# auto-injected by SEC sandbox
import math
import itertools
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import json
from collections import defaultdict

def barrington_construction(formula):
    stack = [[]]
    for node in formula:
        if node[0] == 'AND':
            stack.append([])
        elif node[0] == 'OR':
            stack[-1].extend(stack.pop())
        elif node[0] == 'NOT':
            stack[-1][len(stack[-1]) - 1] = (stack[-1][len(stack[-1]) - 1][0], '1', '0')
        else:
            stack[-1].append((len(stack[-1]) + 1, '0', '1'))
    return stack[0]

def lift_to_f2(triples):
    a = [(1, 2, 3, 4, 5)]
    b = [(1, 2)]
    f2_word = []
    for triple in triples:
        var_index, sigma_true, sigma_false = triple
        if sigma_true == '0':
            f2_word.extend(a)
        elif sigma_true == '1':
            f2_word.extend(b)
        if sigma_false == '0':
            f2_word.extend(b)
        elif sigma_false == '1':
            f2_word.extend(a)
    return reduce_f2_word(f2_word)

def reduce_f2_word(word):
    stack = []
    for letter in word:
        if stack and (stack[-1] == ('a', 'b') or stack[-1] == ('b', 'a')):
            stack.pop()
        else:
            stack.append(letter)
    return stack

def count_aba(word):
    aba_count = 0
    a_inv_b_inv_a_inv_count = 0
    for i in range(len(word) - 2):
        if word[i:i+3] == ('a', 'b', 'a'):
            aba_count += 1
        elif word[i:i+4] == ('a', 'b', 'a', 'b') or word[i:i+4] == ('b', 'a', 'b', 'a'):
            a_inv_b_inv_a_inv_count += 1
    return aba_count - a_inv_b_inv_a_inv_count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n, depth):
        if depth == 0:
            return [('NOT', random.choice([0, 1]))]
        else:
            op = random.choice(['AND', 'OR'])
            left = generate_formula(n // 2, depth - 1)
            right = generate_formula(n // 2, depth - 1)
            if op == 'AND':
                return [('AND', left, right)]
            elif op == 'OR':
                return [('OR', left, right)]

    def evaluate_formula(formula, x):
        stack = []
        for node in formula:
            if node[0] == 'NOT':
                stack.append(not evaluate_formula(node[1], x))
            else:
                a, b = x[node[2]], x[node[3]]
                if node[0] == 'AND':
                    stack.append(a and b)
                elif node[0] == 'OR':
                    stack.append(a or b)
        return stack[-1]

    n_values = [4, 6, 8]
    depth_values = [2, 3, 4, 5]
    results = defaultdict(list)

    for n in n_values:
        for d in depth_values:
            formula = generate_formula(n, d)
            max_tau = 0
            for _ in range(10):
                x = {i: random.choice([0, 1]) for i in range(n)}
                triples = barrington_construction(formula)
                f2_word = lift_to_f2(triples)
                tau = count_aba(f2_word)
                max_tau = max(max_tau, abs(tau))
            results[(n, d)].append(max_tau)

    metric_values = [max(results[(n, d)] for n in n_values) / (2 ** d) for d in depth_values]
    mean_value = sum(metric_values) / len(depth_values)
    std_value = (sum((x - mean_value) ** 2 for x in metric_values) / len(depth_values)) ** 0.5
    support_fraction = sum(1 for v in metric_values if 0.25 <= v <= 4) / len(depth_values)

    conjecture_holds = support_fraction >= 0.8 and all(metric_values[i] <= metric_values[i + 1] for i in range(len(metric_values) - 1))
    counterexample = "" if conjecture_holds else f"median ratio {mean_value} not in [0.25,4] or non-monotonic"

    return {
        "metric_name": "max_tau_over_2^d",
        "metric_value": mean_value,
        "instances_tested": len(depth_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"median ratio {mean_value} not in [0.25,4] or non-monotonic\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")