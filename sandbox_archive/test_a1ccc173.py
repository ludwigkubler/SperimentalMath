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
    
    def generate_cnf(m):
        cnf = []
        for _ in range(2**m - 1):
            clause = [random.randint(-m, m) for _ in range(m)]
            if all(lit != 0 for lit in clause):
                cnf.append(clause)
        return cnf
    
    def tseitin_encoding(cnf):
        literals = set()
        for clause in cnf:
            literals.update(abs(lit) for lit in clause)
        n_vars = max(literals)
        
        new_cnf = []
        var_counter = n_vars + 1
        for i, clause in enumerate(cnf):
            tseitin_var = -var_counter
            new_clause = [tseitin_var]
            for lit in clause:
                if lit > 0:
                    new_clause.append(-lit)
                else:
                    new_clause.append(lit)
            new_cnf.append(new_clause)
            
            for j in range(len(clause)):
                other_clauses = cnf[:i] + cnf[i+1:]
                for other_clause in other_clauses:
                    if lit not in other_clause and -lit not in other_clause:
                        new_other_clause = [tseitin_var, -other_clauses[j]]
                        new_cnf.append(new_other_clause)
            
            var_counter += 1
        
        return new_cnf
    
    def min_order(cnf):
        n_vars = max(abs(lit) for lit in cnf)
        if n_vars == 0:
            return 0
        tensor_order = n_vars
        while True:
            found = False
            for clause in cnf:
                if any(abs(lit) > tensor_order for lit in clause):
                    found = True
                    break
            if not found:
                return tensor_order
            tensor_order += 1
    
    def dpll_solver(cnf):
        def solve(lits, cls):
            if not lits:
                return []
            unit_clause = next((c for c in lits if len(c) == 1), None)
            if unit_clause:
                lit = unit_clause[0]
                new_lits_true = [l for l in lits if l != lit and -l not in lits]
                new_lits_false = [l for l in lits if l != -lit and l not in lits]
                return solve(new_lits_true, cls) or solve(new_lits_false, cls)
            pure_literal = next((l for l in range(1, max(abs(lit) for lit in lits) + 1) if (l in lits and -l not in lits)), None)
            if pure_literal:
                new_lits_true = [l for l in lits if l != pure_literal]
                new_lits_false = [l for l in lits if l != -pure_literal]
                return solve(new_lits_true, cls) or solve(new_lits_false, cls)
            branching_lit = random.choice(lits[0])
            new_lits_true = [l for l in lits if l != branching_lit and -l not in lits]
            new_lits_false = [l for l in lits if l != -branching_lit and l not in lits]
            return solve(new_lits_true, cls) or solve(new_lits_false, cls)
        
        return solve(cnf, cnf)
    
    def proof_length(cnf):
        return len(dpll_solver(cnf))
    
    m = random.randint(5, 30)
    cnf = generate_cnf(m)
    tseitin_cnf = tseitin_encoding(cnf)
    min_tensor_order = min_order(tseitin_cnf)
    proof_len = proof_length(cnf)
    
    return {
        "metric_name": "min_order",
        "metric_value": min_tensor_order,
        "instances_tested": 1,
        "n_max": m,
        "conjecture_holds": min_tensor_order >= 0.5 * proof_len and min_tensor_order <= 2 * proof_len,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")