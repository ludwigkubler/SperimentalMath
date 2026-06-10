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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clause = random.sample(literals, 3)
            clauses.append(clause)
        return clauses
    
    def is_satisfiable(phi):
        stack = []
        assignment = {}
        
        def dpll():
            if not phi:
                return True
            literal = next((lit for lit in phi[0] if lit not in assignment and -lit not in assignment), None)
            if literal is None:
                return all(assignment.get(lit, False) == (lit > 0) for lit in phi[0])
            
            assignment[literal] = True
            new_phi = [c for c in phi if literal not in c and -literal not in c]
            if dpll():
                return True
            del assignment[literal]
            
            assignment[-literal] = True
            new_phi = [c for c in phi if -literal not in c and literal not in c]
            if dpll():
                return True
            del assignment[-literal]
            
            return False
        
        return dpll()
    
    def count_periodic_points(phi):
        n = len(phi)
        periodic_points = set()
        
        def next_state(state):
            new_state = [0] * n
            for i in range(n):
                for clause in phi:
                    if all(lit in state or -lit not in state for lit in clause):
                        new_state[i] = 1 - new_state[i]
                        break
            return tuple(new_state)
        
        state = (random.randint(0, 1) for _ in range(n))
        visited_states = set()
        while True:
            if state in visited_states:
                periodic_points.add(state)
                break
            visited_states.add(state)
            state = next_state(state)
        
        return len(periodic_points)
    
    n = random.randint(5, 40)
    phi = generate_3cnf(n)
    num_periodic_points = count_periodic_points(phi)
    
    metric_name = "num_periodic_points"
    metric_value = num_periodic_points
    instances_tested = 1
    n_max = n
    conjecture_holds = num_periodic_points <= n**2  # Example bound, replace with actual conjectured bound
    counterexample = "" if conjecture_holds else f"phi: {phi}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")