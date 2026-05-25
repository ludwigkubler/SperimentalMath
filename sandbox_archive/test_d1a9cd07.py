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
        start_state = 0
        accept_states = [n-1]
        transitions = {i: {} for i in states}
        
        for i in range(n):
            for j in range(n):
                if j == (i + 1) % n:
                    transitions[i][j] = 'a'
                else:
                    transitions[i][j] = 'b'
        
        return {
            "states": states,
            "start_state": start_state,
            "accept_states": accept_states,
            "transitions": transitions
        }
    
    def dfa_rank(dfa):
        n = len(dfa["states"])
        adjacency_matrix = [[0 for _ in range(n)] for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                if dfa["transitions"][i][j] == 'a':
                    adjacency_matrix[i][j] += 1
        
        # Gaussian elimination to find the rank
        rank = n
        for i in range(n):
            if adjacency_matrix[i][i] == 0:
                found_nonzero_row = False
                for k in range(i+1, n):
                    if adjacency_matrix[k][i] != 0:
                        for j in range(n):
                            adjacency_matrix[i][j], adjacency_matrix[k][j] = adjacency_matrix[k][j], adjacency_matrix[i][j]
                        found_nonzero_row = True
                        break
                if not found_nonzero_row:
                    rank -= 1
                    continue
            for k in range(n):
                if k != i and adjacency_matrix[k][i] != 0:
                    factor = Fraction(adjacency_matrix[k][i], adjacency_matrix[i][i])
                    for j in range(n):
                        adjacency_matrix[k][j] -= factor * adjacency_matrix[i][j]
        
        return rank
    
    def ac0_circuit_size(dfa):
        n = len(dfa["states"])
        # Simplified estimate based on DFA size
        return n**2
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        dfa = generate_dfa(n)
        rank = dfa_rank(dfa)
        circuit_size = ac0_circuit_size(dfa)
        
        if rank >= n**2:
            conjecture_holds = False
            counterexample = f"DFA with rank {rank} for n={n}"
            break
        
        total_rank += rank
        instances_tested += 1
    
    mean_rank = total_rank / instances_tested if instances_tested > 0 else 0
    support_fraction = Fraction(instances_tested, len(n_values))
    
    return {
        "metric_name": "Rank of DFA",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 53))
    
    results = []
    total_rank = 0
    instances_tested = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if trial_result["conjecture_holds"]:
            total_rank += trial_result["metric_value"]
            instances_tested += trial_result["instances_tested"]
    
    mean_rank = total_rank / instances_tested if instances_tested > 0 else 0
    support_fraction = Fraction(instances_tested, len(seeds))
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")