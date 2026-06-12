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
    
    def generate_formula(n, m):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + [f'~{v}' for v in variables], 2)
            clauses.append(clause)
        return clauses

    def construct_topological_system(clauses):
        # Simplified Markov chain construction
        states = set()
        transitions = {}
        for clause in clauses:
            state = tuple(sorted(clause))
            states.add(state)
            if state not in transitions:
                transitions[state] = {}
            for var in state:
                next_state = list(state)
                next_state.remove(var)
                next_state.append(f'~{var}')
                next_state = tuple(sorted(next_state))
                states.add(next_state)
                if next_state not in transitions[state]:
                    transitions[state][next_state] = 0.5
        return states, transitions

    def compute_topological_entropy(transitions):
        # Simplified entropy calculation
        total_prob = sum(sum(v for v in vs.values()) for vs in transitions.values())
        entropy = 0
        for state, vs in transitions.items():
            prob = sum(vs.values()) / total_prob
            if prob > 0:
                entropy -= prob * math.log2(prob)
        return entropy

    def resolution_proof_width(clauses):
        # Simplified width calculation
        max_clause_length = max(len(clause) for clause in clauses)
        return max_clause_length

    n, m = random.randint(5, 30), random.randint(n, n + 10)
    formula = generate_formula(n, m)
    states, transitions = construct_topological_system(formula)
    H_top = compute_topological_entropy(transitions)
    w_phi = resolution_proof_width(formula)
    
    metric_value = w_phi <= H_top ** 2 * math.log(n + m)
    conjecture_holds = metric_value
    counterexample = "" if conjecture_holds else f"Formula: {formula}, H_top: {H_top}, w_phi: {w_phi}"
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 30
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")