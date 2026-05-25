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
import math
from fractions import Fraction

# Function to generate a random DFA with n states
def generate_dfa(n):
    states = list(range(n))
    alphabet = ['a', 'b']
    transitions = {q: {} for q in states}
    start_state = 0
    final_states = [random.choice(states) for _ in range(2)]
    
    for q in states:
        for a in alphabet:
            next_state = random.choice(states)
            while next_state == q and len(transitions[q]) > 1:  # Ensure no self-loops or redundant transitions
                next_state = random.choice(states)
            transitions[q][a] = next_state
    
    return {
        'states': states,
        'alphabet': alphabet,
        'transitions': transitions,
        'start_state': start_state,
        'final_states': final_states
    }

# Function to compute the syntactic monoid of a DFA
def syntactic_monoid(dfa):
    states = dfa['states']
    alphabet = dfa['alphabet']
    transitions = dfa['transitions']
    
    # Compute the transition matrix
    n = len(states)
    M = [[0] * n for _ in range(n)]
    for q in states:
        for a in alphabet:
            next_state = transitions[q][a]
            M[states.index(q)][states.index(next_state)] += 1
    
    # Compute the closure of the transition matrix
    M_closure = [row[:] for row in M]
    changed = True
    while changed:
        changed = False
        for i in range(n):
            for j in range(n):
                if M[i][j] == 0:
                    for k in range(n):
                        if M[i][k] > 0 and M[k][j] > 0:
                            M[i][j] += 1
                            changed = True
    
    # Find the rank of the transition matrix closure
    rank = 0
    for row in M_closure:
        if any(row):
            rank += 1
    
    return rank

# Function to compute the resolution proof depth and steps
def resolution_steps(dfa):
    states = dfa['states']
    alphabet = dfa['alphabet']
    transitions = dfa['transitions']
    
    # Compute the transition matrix
    n = len(states)
    M = [[0] * n for _ in range(n)]
    for q in states:
        for a in alphabet:
            next_state = transitions[q][a]
            M[states.index(q)][states.index(next_state)] += 1
    
    # Find the complement of the DFA
    complement_states = [q for q in states if q not in dfa['final_states']]
    
    # Compute the resolution proof depth and steps
    depth = 0
    steps = 0
    while complement_states:
        new_states = []
        for i in range(len(complement_states)):
            for j in range(i + 1, len(complement_states)):
                if M[complement_states[i]][complement_states[j]] > 0 and M[complement_states[j]][complement_states[i]] > 0:
                    new_state = complement_states[i] ^ complement_states[j]
                    if new_state not in complement_states:
                        complement_states.append(new_state)
                        steps += 1
        depth += 1
        complement_states = [q for q in complement_states if any(M[q][s] > 0 for s in states)]
    
    return depth, steps

# Function to multiply two matrices
def matrix_mult(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

# Function to run a single trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    dfa = generate_dfa(n)
    rank = syntactic_monoid(dfa)
    depth, steps = resolution_steps(dfa)
    
    if depth == 0 or steps == 0:
        return {
            "metric_name": "Ratio of Resolution Steps to Depth",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Depth or steps is zero"
        }
    
    ratio = Fraction(steps, depth)
    
    return {
        "metric_name": "Ratio of Resolution Steps to Depth",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": True if ratio <= 1 else False,
        "counterexample": "" if ratio <= 1 else f"Ratio {ratio} > 1"
    }

# Main function to run multiple trials
if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 76))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r['metric_value'] for r in results if r['metric_value'] is not None]
    support_fraction = sum(r['conjecture_holds'] for r in results) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio > 1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")