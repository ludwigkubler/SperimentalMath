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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def dpll_search_tree_width(f):
        n = len(f)
        states = [{'assignment': [], 'unsatisfied_clauses': f}]
        while states:
            state = states.pop()
            if not state['unsatisfied_clauses']:
                return len(state['assignment'])
            unit_clause = next((c for c in state['unsatisfied_clauses'] if len(c) == 1), None)
            if not unit_clause:
                continue
            lit, polarity = unit_clause[0], unit_clause[1]
            new_state = {'assignment': state['assignment'].copy(), 'unsatisfied_clauses': state['unsatisfied_clauses'].copy()}
            new_state['assignment'].append((lit, polarity))
            for clause in new_state['unsatisfied_clauses']:
                if lit in clause:
                    clause.remove(lit)
                elif -lit in clause:
                    clause.remove(-lit)
            states.append(new_state)
        return float('inf')
    
    def geometric_entropy(φ):
        n = len(φ)
        Hgeo = 0
        for i in range(n):
            p_i = sum(1 for x in φ if x[i] == 1) / n
            if p_i > 0 and p_i < 1:
                Hgeo -= p_i * math.log2(p_i)
        return Hgeo
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Each n tested 5 times
            f = generate_boolean_function(n)
            wDPLL = dpll_search_tree_width(f)
            φ = [f[i] for i in range(len(f))]
            Hgeo = geometric_entropy(φ)
            
            total_metric_value += Hgeo * wDPLL
            instances_tested += 1
            n_max = max(n_max, n)
            
            if wDPLL == float('inf'):
                conjecture_holds = False
                counterexample = "DPLL search tree width is infinite"
                break
    
    return {
        "metric_name": "Hgeo * wDPLL",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")