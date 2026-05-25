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
    
    def generate_dfa(n):
        states = list(range(n))
        start_state = 0
        final_states = [n-1]
        transitions = {}
        for i in range(n):
            transitions[i] = {j: (i + j) % n for j in range(2)}
        return states, start_state, final_states, transitions
    
    def dfa_rank(dfa):
        states, _, _, _ = dfa
        adjacency_matrix = [[0] * len(states) for _ in range(len(states))]
        for i in range(len(states)):
            for j in range(2):
                adjacency_matrix[i][transitions[i][j]] += 1
        rank = 0
        for row in adjacency_matrix:
            if sum(row) > 0:
                rank += 1
        return rank
    
    def ac0_circuit_size(n):
        # Placeholder function to simulate AC⁰ circuit size
        # This is a dummy implementation and should be replaced with actual logic
        return n**2
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    dfa = generate_dfa(n)
    rank = dfa_rank(dfa)
    circuit_size = ac0_circuit_size(n)
    
    if rank >= n**2:
        return {
            "metric_name": "DFA Rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"DFA with rank {rank} cannot be computed by AC⁰ circuit of size O(n^c)"
        }
    
    return {
        "metric_name": "DFA Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"DFA with rank Ω(n^2) cannot be computed by AC⁰ circuit\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")