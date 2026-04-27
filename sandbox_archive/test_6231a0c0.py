# auto-injected by SEC sandbox
import math
import collections
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import json
from itertools import product

# Helper functions for basic operations
def matrix_multiply(A, B):
    return [[sum(a * b for a, b in zip(row_a, col_b)) for col_b in zip(*B)] for row_a in A]

def gaussian_elimination(M):
    n = len(M)
    for i in range(n):
        # Find the pivot
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = M[j][i] / M[i][i]
            for k in range(n):
                M[j][k] -= factor * M[i][k]
    
    # Back-substitute
    x = [0.0] * n
    for i in range(n-1, -1, -1):
        x[i] = (M[i][-1] - sum(M[i][j] * x[j] for j in range(i+1, n))) / M[i][i]
    
    return x

def matrix_power(A, k):
    result = [[0]*len(A) for _ in range(len(A))]
    for i in range(len(A)):
        result[i][i] = 1
    while k > 0:
        if k % 2 == 1:
            result = matrix_multiply(result, A)
        A = matrix_multiply(A, A)
        k //= 2
    return result

def hopcroft_minimization(states, transitions, accepting):
    n = len(transitions)
    dfa_states = {frozenset([s]): i for i, s in enumerate(states)}
    dfa_accepting = [i for i, s in enumerate(dfa_states) if any(t in accepting for t in s)]
    
    def get_next_state(state, char):
        next_states = set()
        for s in state:
            next_states.update(transitions[s][char])
        return frozenset(next_states)
    
    dfa_transitions = {i: {} for i in range(len(dfa_states))}
    queue = [0]
    visited = [False] * len(dfa_states)
    while queue:
        current_state = queue.pop(0)
        visited[current_state] = True
        for char in '01':
            next_state = get_next_state(dfa_states[current_state], char)
            if next_state not in dfa_states:
                dfa_states[next_state] = len(dfa_states)
            if next_state not in dfa_transitions[current_state]:
                dfa_transitions[current_state][char] = dfa_states[next_state]
                queue.append(dfa_states[next_state])
    
    return dfa_states, dfa_transitions, dfa_accepting

def truth_table_to_dfa(truth_table, n):
    states = set(range(2**n))
    transitions = {s: {'0': [], '1': []} for s in states}
    accepting = []
    
    def get_next_state(state, char):
        next_states = set()
        for i in range(len(state)):
            if state[i] == 1 and truth_table[i][int(char)]:
                next_states.add(i)
        return frozenset(next_states)
    
    for s in states:
        transitions[s]['0'] = get_next_state(s, '0')
        transitions[s]['1'] = get_next_state(s, '1')
        if any(truth_table[i][s] for i in range(len(truth_table))):
            accepting.append(s)
    
    return dfa_states, dfa_transitions, dfa_accepting

def count_leaves(node):
    if isinstance(node, tuple):
        return 1 + sum(count_leaves(child) for child in node)
    else:
        return 0

def generate_truth_table(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in {5, 8, 11, 14}:
        for _ in range(200):
            truth_table = generate_truth_table(n)
            A_f = hopcroft_minimization(set(range(2**n)), truth_table_to_dfa(truth_table, n)[1], set())[0]
            L_f = count_leaves(build_formula(truth_table))
            results.append((A_f, L_f))
    
    max_ratio = max(A / ((n + 2) * L + 2) for A, L in results)
    conjecture_holds = all(A <= (n + 2) * L + 2 for A, L in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ratio",
        "metric_value": max_ratio,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": {"seed": seed, **result}}))
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = (sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")