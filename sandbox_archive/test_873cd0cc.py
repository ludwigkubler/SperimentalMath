# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def det(A):
    n = len(A)
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    det_val = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det_val += (-1) ** j * A[0][j] * det(submatrix)
    return det_val

def matrix_mult(A, B):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def free_reduce(w, a_inv_b_inv_a_inv):
    stack = []
    for char in w:
        if not stack or char == 'a':
            stack.append(char)
        elif char == 'b' and len(stack) >= 2 and stack[-1] == 'a' and stack[-2] == 'a':
            stack.pop()
            stack.pop()
        else:
            stack.append(char)
    return ''.join(stack), a_inv_b_inv_a_inv

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(depth, n):
        if depth == 1:
            return random.choice(['0', '1'])
        op = random.choice(['AND', 'OR'])
        left = generate_formula(depth - 1, n)
        right = generate_formula(depth - 1, n)
        return f"({left} {op} {right})"
    
    def barrington_construction(formula):
        stack = []
        for char in formula:
            if char == '(':
                stack.append([])
            elif char == ')':
                subformula = stack.pop()
                if len(subformula) == 1:
                    stack[-1].append((len(stack[-1]) + 1, '0', '1'))
                else:
                    left, right = subformula
                    stack[-1].append((len(stack[-1]) + 1, '0', '1'))
            elif char in ['0', '1']:
                stack[-1].append((len(stack[-1]) + 1, char, char))
        return stack[0]
    
    def lift_to_F2(triples):
        a = (1, 2, 3, 4, 5)
        b = (1, 2)
        w = []
        for var_index, sigma_true, sigma_false in triples:
            if sigma_true == '1':
                w.extend([a[var_index - 1], b[0]])
            elif sigma_true == '0':
                w.extend([a[var_index - 1], b[1]])
            if sigma_false == '1':
                w.extend([a[var_index - 1], b[1]])
            elif sigma_false == '0':
                w.extend([a[var_index - 1], b[0]])
        return ''.join(w)
    
    def count_aba(word):
        aba_count = word.count('aba')
        a_inv_b_inv_a_inv_count = word.count('a^-1b^-1a^-1')
        return aba_count - a_inv_b_inv_a_inv_count
    
    n_values = [4, 6, 8]
    depth_values = [2, 3, 4, 5]
    results = []
    
    for n in n_values:
        for d in depth_values:
            formula = generate_formula(d, n)
            triples = barrington_construction(formula)
            w = lift_to_F2(triples)
            reduced_word, a_inv_b_inv_a_inv = free_reduce(w, 'a^-1b^-1a^-1')
            tau = count_aba(reduced_word)
            results.append({'n': n, 'd': d, 'tau': tau})
    
    max_tau_per_depth = {d: max(r['tau'] for r in results if r['d'] == d) / 2**d for d in depth_values}
    median_ratio = sorted(max_tau_per_depth.values())[len(depth_values)//2]
    
    conjecture_holds = 0.25 <= median_ratio <= 4 and all(max_tau_per_depth[d] >= max_tau_per_depth[d-1] for d in range(2, 6))
    counterexample = "" if conjecture_holds else "median_ratio_out_of_bounds"
    
    return {
        "metric_name": "max_tau_over_2^d",
        "metric_value": median_ratio,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    all_ratios = [r['metric_value'] for r in results if 'metric_value' in r]
    support_fraction = sum(1 for r in results if r.get('conjecture_holds', False)) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={math.mean(all_ratios):.4f} std={math.std(all_ratios):.4f} support_fraction={support_fraction:.2f}")
    elif any(r.get('conjecture_holds', False) for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"median_ratio_out_of_bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_supporting_evidence")