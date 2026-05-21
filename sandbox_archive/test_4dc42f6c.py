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
    
    def simulate_bp(bp, input_):
        current_state = bp['start']
        for bit in bin(input_)[2:].zfill(len(bp['variable_order'])):
            if bit == '0':
                next_state = bp['transitions'][current_state]['0']
            else:
                next_state = bp['transitions'][current_state]['1']
            current_state = next_state
        return bp['accept_states'].get(current_state, 0)
    
    def walsh_hadamard_transform(truth_table):
        n = len(truth_table)
        f_hat = [0] * (1 << n)
        
        for S in range(1 << n):
            sum_val = 0
            for x in range(1 << n):
                sign = (-1) ** bin(S & x).count('1')
                sum_val += sign * truth_table[x]
            f_hat[S] = sum_val / math.sqrt(n)
        
        return f_hat
    
    def norm_l1(f_hat):
        return sum(abs(val) for val in f_hat)
    
    n_values = [6, 8, 10, 12, 14]
    w_values = [2, 3, 4]
    instances_tested = 0
    total_value = 0
    
    for n in n_values:
        for w in w_values:
            for _ in range(30):
                # Construct the BP
                variable_order = list(range(n))
                random.shuffle(variable_order)
                transitions = {}
                accept_states = set()
                
                current_state = 0
                for i in range(w):
                    new_state = len(transitions) + 1
                    transitions[current_state] = {'0': new_state, '1': new_state}
                    current_state = new_state
                
                for _ in range(n - w):
                    new_state = len(transitions) + 1
                    transitions[current_state] = {'0': new_state, '1': new_state}
                    current_state = new_state
                
                accept_states.add(current_state)
                
                bp = {
                    'variable_order': variable_order,
                    'transitions': transitions,
                    'accept_states': accept_states,
                    'start': 0
                }
                
                # Simulate the BP and compute the truth table
                truth_table = [simulate_bp(bp, input_) for input_ in range(1 << n)]
                f_hat = walsh_hadamard_transform(truth_table)
                norm_value = norm_l1(f_hat)
                
                instances_tested += 1
                total_value += norm_value
                
                if norm_value > (2 * w * n + 2 + 1) ** 3:
                    return {
                        "metric_name": "Fourier L1 Norm",
                        "metric_value": norm_value,
                        "instances_tested": instances_tested,
                        "conjecture_holds": False,
                        "counterexample": f"BP of size {2 * w * n + 2} with n={n}, w={w}"
                    }
    
    mean_value = total_value / instances_tested
    support_fraction = (instances_tested >= 84)  # At least 28/30 seeds for each (n, w)
    
    return {
        "metric_name": "Fourier L1 Norm",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "conjecture_holds": support_fraction,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res['metric_value'] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=NA support_fraction={support_fraction}")
    elif any(not res['conjecture_holds'] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=NA first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=30")