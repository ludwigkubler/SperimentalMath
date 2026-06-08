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
    
    def generate_cnf(n: int, m: int):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0], clause[1] = -clause[0], -clause[1]
            cnf.append(clause)
        return cnf
    
    def dpll_length(cnf):
        assignment = {}
        
        def is_satisfiable():
            stack = []
            unit_clauses = []
            
            while True:
                if not stack and not unit_clauses:
                    return False
                
                if unit_clauses:
                    clause, literal = unit_clauses.pop()
                    assignment[literal] = True
                    for c in cnf:
                        if literal in c:
                            c.remove(literal)
                        if -literal in c:
                            c.remove(-literal)
                            if not c:
                                return False
                else:
                    literal = random.choice([l for l in range(1, n+1) if l not in assignment and -l not in assignment])
                    stack.append((literal, cnf[:]))
                
                unit_clauses = [(c, i) for i, c in enumerate(cnf) if len([x for x in c if x not in assignment]) == 1]
            
            return True
        
        length = 0
        while is_satisfiable():
            length += 1
            assignment.clear()
        
        return length
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n, n * (n - 1) // 2)
        length = dpll_length(cnf)
        results.append(length)
    
    mean_length = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_length) ** 2 for x in results) / len(results))
    
    return {
        "metric_name": "DPLL Proof Length",
        "metric_value": mean_length,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": False if std_dev == 0 else True,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_length = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_length) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.7 * mean_length and r <= 1.3 * mean_length) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_dev} support_fraction={support_fraction}")
    elif any(r < 0.7 * mean_length or r > 1.3 * mean_length for r in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if result < 0.7 * mean_length or result > 1.3 * mean_length)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")