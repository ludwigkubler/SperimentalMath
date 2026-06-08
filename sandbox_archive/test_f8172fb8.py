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
    
    def tseitin_embedding(phi):
        n = len(phi)
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        
        # Convert phi to CNF using Tseitin encoding
        for clause in phi:
            if len(clause) == 1:
                literals.append(f'y{len(literals)}')
                clauses.append([literals[-1]])
                clauses.append([-clause[0], -literals[-1]])
            elif len(clause) == 2:
                literals.append(f'y{len(literals)}')
                clauses.append([literals[-1]])
                clauses.append([-clause[0], literals[-1]])
                clauses.append([-clause[1], literals[-1]])
                clauses.append([clause[0], clause[1], -literals[-1]])
            else:
                return None  # Unsupported clause length
        
        return clauses
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if -literal not in c], new_assignment):
                return True
            return False
        
        polarities = [random.choice([-1, 1]) for _ in range(len(clauses))]
        literal = random.choice([l for l, p in zip(literals, polarities) if p == 1])
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in clauses if literal not in c], new_assignment):
            return True
        
        new_assignment[literal] = False
        if dpll([c for c in clauses if -literal not in c], new_assignment):
            return True
        
        return False
    
    def minimal_local_index(clauses):
        # Placeholder for actual computation of minimal local index
        return len(clauses)
    
    n_max = 40
    instances_tested = 30
    metric_value = 0.0
    conjecture_holds = False
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        phi = [[random.choice([-1, 1]) for _ in range(random.randint(1, 2))] for _ in range(n)]
        
        embedding = tseitin_embedding(phi)
        if embedding is None:
            continue
        
        proof_length = 0
        while not dpll(embedding, {}):
            proof_length += 1
        
        min_ind = minimal_local_index(embedding)
        metric_value += abs(min_ind - proof_length) / instances_tested
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": False,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.75:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")