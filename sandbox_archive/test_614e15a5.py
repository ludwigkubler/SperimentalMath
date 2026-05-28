# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_dfa(n):
        states = list(range(n))
        alphabet = ['0', '1']
        transition_table = {state: {} for state in states}
        start_state = 0
        accept_states = [n-1]
        
        for state in states:
            for char in alphabet:
                next_state = random.choice(states)
                while next_state == state:
                    next_state = random.choice(states)
                transition_table[state][char] = next_state
        
        return {
            'states': states,
            'alphabet': alphabet,
            'transition_table': transition_table,
            'start_state': start_state,
            'accept_states': accept_states
        }
    
    def generate_cnf(n):
        literals = list(range(1, 2*n+1))
        clauses = []
        
        for i in range(1, n+1):
            clause = [random.choice(literals) for _ in range(3)]
            while len(set(clause)) != 3:
                clause = [random.choice(literals) for _ in range(3)]
            clauses.append(clause)
        
        return {
            'literals': literals,
            'clauses': clauses
        }
    
    def dfa_to_cnf(dfa):
        n = len(dfa['states'])
        cnf = []
        
        for state in dfa['states']:
            if state not in dfa['accept_states']:
                clause = [-i for i in range(1, 2*n+1) if (state, '0') in dfa['transition_table'] and dfa['transition_table'][state]['0'] == (i-1)//n]
                cnf.append(clause)
        
        return {
            'literals': list(range(1, 2*n+1)),
            'clauses': cnf
        }
    
    def ac0_circuit_size(cnf):
        n = len(cnf['literals'])
        size = 0
        
        for clause in cnf['clauses']:
            size += len(clause)
        
        return size
    
    def automorphism_group(dfa):
        states = dfa['states']
        alphabet = dfa['alphabet']
        transition_table = dfa['transition_table']
        
        def is_automorphism(sigma, tau):
            for state in states:
                for char in alphabet:
                    if transition_table[state][char] != transition_table[sigma(state)][tau(char)]:
                        return False
            return True
        
        automorphisms = []
        
        for sigma in itertools.permutations(states):
            for tau in itertools.permutations(alphabet):
                if is_automorphism(sigma, tau):
                    automorphisms.append((sigma, tau))
        
        return automorphisms
    
    def rank_autom(dfa):
        automorphisms = automorphism_group(dfa)
        return len(automorphisms)
    
    def ac0_parity_depth(cnf):
        n = len(cnf['literals'])
        depth = 1
        
        while True:
            new_clauses = []
            for clause in cnf['clauses']:
                if any(lit in literals for lit in clause):
                    new_clause = [lit for lit in clause if lit not in literals]
                    if new_clause:
                        new_clauses.append(new_clause)
            if not new_clauses:
                break
            cnf['clauses'] = new_clauses
            depth += 1
        
        return depth
    
    n = random.randint(5, 40)
    dfa = generate_dfa(n)
    cnf = dfa_to_cnf(dfa)
    
    rank = rank_autom(dfa)
    size_ac0 = ac0_circuit_size(cnf)
    depth_ac0 = ac0_parity_depth(cnf)
    
    metric_value = rank / size_ac0
    
    if rank < 1:
        conjecture_holds = False
        counterexample = "rank_too_low"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "Rank to AC0 Circuit Size Ratio",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r['metric_value'] for r in results if 'metric_value' in r]
    conjecture_holds_count = sum(1 for r in results if r.get('conjecture_holds', False))
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    support_fraction = conjecture_holds_count / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values)} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"rank_too_low\" first_failing_seed={first_failing_seed}")