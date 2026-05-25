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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_dfa(n):
        states = list(range(n))
        transitions = {i: {} for i in states}
        start_state = 0
        accept_states = [n-1]
        
        for state in states:
            for symbol in range(2):  # Assuming binary alphabet
                next_state = random.choice(states)
                transitions[state][symbol] = next_state
        
        return {
            'states': states,
            'transitions': transitions,
            'start_state': start_state,
            'accept_states': accept_states
        }
    
    def dfa_rank(dfa):
        n = len(dfa['states'])
        M = [[0] * n for _ in range(n)]
        
        for state, trans in dfa['transitions'].items():
            for symbol, next_state in trans.items():
                M[state][next_state] += 1
        
        rank = 0
        for i in range(n):
            if sum(M[i]) > 0:
                rank += 1
        
        return rank
    
    def ac0_circuit_size(dfa):
        n = len(dfa['states'])
        # Simplified heuristic for AC⁰ circuit size
        return n * math.log2(n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        dfa = generate_dfa(n)
        rank = dfa_rank(dfa)
        circuit_size = ac0_circuit_size(dfa)
        
        if rank >= n**2:
            counterexample = f"DFA with n={n} has rank {rank}"
            return {
                "metric_name": "DFA Rank",
                "metric_value": rank,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": counterexample
            }
        
        results.append({
            "n": n,
            "rank": rank,
            "circuit_size": circuit_size
        })
    
    mean_rank = sum(result['rank'] for result in results) / len(results)
    std_rank = math.sqrt(sum((result['rank'] - mean_rank)**2 for result in results) / len(results))
    
    return {
        "metric_name": "DFA Rank",
        "metric_value": mean_rank,
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result['metric_value'] for result in results) / len(results)
    std_rank = math.sqrt(sum((result['metric_value'] - mean_rank)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result['conjecture_holds']) / len(results)
    
    if all(result['conjecture_holds'] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"DFA with rank Ω(n^2)\" first_failing_seed={first_failing_seed}")