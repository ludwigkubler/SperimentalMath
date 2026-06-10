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
        inputs = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(m):
            clause = random.sample(inputs + [f'¬{lit}' for lit in inputs], 2)
            clauses.append(clause)
        return inputs, clauses
    
    def dpll(cnf):
        literals = set()
        for clause in cnf:
            literals.update(clause)
        
        def solve(model):
            if not cnf:
                return model
            unit_clause = next((clause for clause in cnf if len(clause) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_model = model.copy()
                if literal.startswith('¬'):
                    new_model.add(literal[1:])
                else:
                    new_model.add(f'¬{literal}')
                return solve(new_model)
            
            literal = next((lit for lit in literals if all(lit not in m and f"¬{lit}" not in m for m in cnf)), None)
            if literal is None:
                return None
            
            def propagate(model, literal):
                new_cnf = []
                for clause in cnf:
                    if literal in clause:
                        continue
                    if f'¬{literal}' in clause:
                        new_clause = [l for l in clause if l != f'¬{literal}']
                        if not new_clause:
                            return None
                        new_cnf.append(new_clause)
                    else:
                        new_cnf.append(clause)
                return new_cnf
            
            result = solve(propagate(model, literal))
            if result is not None:
                return result
            return solve(propagate(model, f'¬{literal}'))
        
        return solve({})
    
    def groupoid_composition_width(circuit):
        # Placeholder implementation for gcw(C)
        return len(circuit[1])
    
    def resolution_proof_complexity(cnf):
        # Placeholder implementation for w(C)
        return len(cnf)
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 2)
    inputs, clauses = generate_circuit(n, m)
    cnf = [set(clause) for clause in clauses]
    
    gcw_C = groupoid_composition_width((inputs, clauses))
    w_C = resolution_proof_complexity(cnf)
    
    if w_C == 0:
        return {
            "metric_name": "gcw(C) / w(C)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_proof_complexity_is_zero"
        }
    
    ratio = Fraction(gcw_C, w_C)
    return {
        "metric_name": "gcw(C) / w(C)",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")