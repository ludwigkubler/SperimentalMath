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
    
    def generate_circuit(n, m):
        variables = list(range(n))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def dpll(circuit, assignment, literals):
        if not circuit:
            return True
        literal = literals[0]
        pos_var = abs(literal) - 1
        neg_var = pos_var + n
        if literal > 0:
            for clause in circuit[:]:
                if pos_var in clause:
                    circuit.remove(clause)
                elif neg_var not in clause:
                    return False
            return dpll(circuit, assignment + [True], literals[1:])
        else:
            for clause in circuit[:]:
                if neg_var in clause:
                    circuit.remove(clause)
                elif pos_var not in clause:
                    return False
            return dpll(circuit, assignment + [False], literals[1:])
    
    def min_dfa_states(circuit):
        n = len(circuit)
        states = {()}
        for literal in range(2 * n):
            new_states = set()
            for state in states:
                if literal < n:
                    new_state = tuple(sorted(state + (True,)))
                else:
                    new_state = tuple(sorted(state + (False,)))
                new_states.add(new_state)
            states.update(new_states)
        return len(states) - 1
    
    def dpll_tree_height(circuit):
        literals = list(range(1, 2 * n + 1))
        return dpll(circuit, [], literals)
    
    n_max = 0
    instances_tested = 0
    total_state_count = 0
    total_dpll_height = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            m = random.randint(n // 2, n * 2)
            circuit = generate_circuit(n, m)
            state_count = min_dfa_states(circuit)
            dpll_height = dpll_tree_height(circuit)
            
            if state_count == 0 or dpll_height == 0:
                continue
            
            total_state_count += state_count
            total_dpll_height += dpll_height
            instances_tested += 1
            n_max = max(n_max, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    mean_state_count = total_state_count / instances_tested
    mean_dpll_height = total_dpll_height / instances_tested
    
    correlation_coefficient = (instances_tested * sum(state_count * dpll_height for state_count, dpll_height in zip([mean_state_count] * instances_tested, [mean_dpll_height] * instances_tested)) - 
                               sum(mean_state_count) * sum(mean_dpll_height)) / math.sqrt((instances_tested * sum(state_count**2 for state_count in [mean_state_count] * instances_tested) - sum(mean_state_count)**2) *
                                                                 (instances_tested * sum(dpll_height**2 for dpll_height in [mean_dpll_height] * instances_tested) - sum(mean_dpll_height)**2))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None]))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient below 0.7\" first_failing_seed={first_failing_seed}")