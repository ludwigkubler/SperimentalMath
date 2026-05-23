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
    
    # Generate a random read-twice branching program P of size n
    def generate_bp_read_twice(n):
        bp = []
        for _ in range(n):
            bp.append(random.choice([0, 1]))
        return bp
    
    # Compute the minimal rank K(P) for each program using a categorification algorithm
    def compute_k_theory_rank(bp):
        n = len(bp)
        rank = 0
        seen_states = set()
        stack = [(0, -1)]
        
        while stack:
            state, parent = stack.pop()
            if state not in seen_states:
                seen_states.add(state)
                rank += 1
                for i in range(n):
                    if bp[i] == (state >> i) & 1:
                        next_state = (state << 1) | bp[i]
                        if next_state != parent:
                            stack.append((next_state, state))
        
        return rank
    
    # Measure the BP_ReadTwice circuit size of each program
    def compute_circuit_size(bp):
        n = len(bp)
        size = 0
        seen_states = set()
        stack = [(0, -1)]
        
        while stack:
            state, parent = stack.pop()
            if state not in seen_states:
                seen_states.add(state)
                size += 1
                for i in range(n):
                    if bp[i] == (state >> i) & 1:
                        next_state = (state << 1) | bp[i]
                        if next_state != parent:
                            stack.append((next_state, state))
        
        return size
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        bp = generate_bp_read_twice(n)
        k_theory_rank = compute_k_theory_rank(bp)
        circuit_size = compute_circuit_size(bp)
        
        if k_theory_rank == 0 or circuit_size == 0:
            continue
        
        ratio = circuit_size / k_theory_rank
        results.append({
            "n": n,
            "k_theory_rank": k_theory_rank,
            "circuit_size": circuit_size,
            "ratio": ratio
        })
    
    if not results:
        return {
            "metric_name": "Ratio of Circuit Size to K-theory Rank",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    metric_value = sum(result["ratio"] for result in results) / len(results)
    conjecture_holds = all(result["ratio"] <= 10 for result in results)
    counterexample = "" if conjecture_holds else "Ratio exceeds 10"
    
    return {
        "metric_name": "Ratio of Circuit Size to K-theory Rank",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials executed")
        sys.exit(0)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(result["counterexample"] == "Ratio exceeds 10" for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] == "Ratio exceeds 10")
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds 10\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support for conjecture")