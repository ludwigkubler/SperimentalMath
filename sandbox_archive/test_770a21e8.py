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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}, model=[]):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([cl for cl in cnf if not any(lit in cl or -lit in cl for lit in new_assignment)], new_assignment, model):
                return True
            new_assignment[literal] = False
            if dpll([cl for cl in cnf if not any(lit in cl or -lit in cl for lit in new_assignment)], new_assignment, model):
                return True
            return False
        pure_literal = next((l for l in range(1, n + 1) if all(l in c or -l in c for c in cnf)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            if dpll([cl for cl in cnf if not any(lit in cl or -lit in cl for lit in new_assignment)], new_assignment, model):
                return True
            new_assignment[pure_literal] = False
            if dpll([cl for cl in cnf if not any(lit in cl or -lit in cl for lit in new_assignment)], new_assignment, model):
                return True
            return False
        literal = next((l for l in range(1, n + 1) if l not in assignment and -l not in assignment), None)
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([cl for cl in cnf if not any(lit in cl or -lit in cl for lit in new_assignment)], new_assignment, model):
            return True
        new_assignment[literal] = False
        if dpll([cl for cl in cnf if not any(lit in cl or -lit in cl for lit in new_assignment)], new_assignment, model):
            return True
        return False
    
    def topological_entropy(cnf):
        n = len(cnf)
        transitions = {}
        states = set()
        
        def dfs(state):
            if state not in states:
                states.add(state)
                for clause in cnf:
                    if all(lit in state or -lit not in state for lit in clause):
                        new_state = state.copy()
                        for lit in clause:
                            if lit > 0 and lit not in new_state:
                                new_state.add(lit)
                            elif lit < 0 and -lit in new_state:
                                new_state.remove(-lit)
                        dfs(new_state)
        
        dfs(set())
        
        for state in states:
            for clause in cnf:
                if all(lit in state or -lit not in state for lit in clause):
                    new_state = state.copy()
                    for lit in clause:
                        if lit > 0 and lit not in new_state:
                            new_state.add(lit)
                        elif lit < 0 and -lit in new_state:
                            new_state.remove(-lit)
                    transitions[(tuple(state), tuple(new_state))] = transitions.get((tuple(state), tuple(new_state)), 0) + 1
        
        total_transitions = sum(transitions.values())
        log_total_states = math.log(len(states))
        
        entropy = -sum(count / total_transitions * (math.log(count / total_transitions) / log_total_states) for count in transitions.values())
        
        return entropy
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        if not dpll(cnf):
            continue
        entropy = topological_entropy(cnf)
        metrics.append(entropy)
    
    mean_entropy = sum(metrics) / len(metrics)
    max_n = max(n_values)
    
    return {
        "metric_name": "topological_entropy",
        "metric_value": mean_entropy,
        "instances_tested": len(metrics),
        "n_max": max_n,
        "conjecture_holds": all(abs(entropy - mean_entropy) <= 3 for entropy in metrics),
        "counterexample": "" if all(abs(entropy - mean_entropy) <= 3 for entropy in metrics) else "Entropy exceeds bound by more than 3 units"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and abs(r["metric_value"] - mean_value) > 3 for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"] and abs(r["metric_value"] - mean_value) > 3)
        print(f"RESULT: FALSIFIED counterexample=\"Entropy exceeds bound by more than 3 units\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")