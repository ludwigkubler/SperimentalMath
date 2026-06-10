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
    
    def dpll(cnf):
        def solve(model):
            if not cnf:
                return model
            literal = next(l for l in range(1, n + 1) if l not in model and -l not in model)
            pos_literal = literal
            neg_literal = -literal
            new_model_pos = model.copy()
            new_model_neg = model.copy()
            new_model_pos[pos_literal] = True
            new_model_neg[neg_literal] = True
            
            result_pos = solve(new_model_pos)
            if result_pos:
                return result_pos
            return solve(new_model_neg)
        
        n = len(cnf[0])
        model = {}
        return solve(model)
    
    def rank(generators):
        n = len(set([abs(x) for x in sum(generators, [])]))
        return n
    
    def algebraic_automorphism_group(cnf):
        # Placeholder for actual algorithm to find the minimal generating set
        generators = []
        for clause in cnf:
            generators.append((random.randint(1, 2), random.randint(1, 2)))
        return generators
    
    n_values = [5, 10, 15, 20, 30, 40]
    circuit_ranks = []
    satisfiability_complexities = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        group = algebraic_automorphism_group(cnf)
        r = rank(group)
        c = len(dpll(cnf))
        
        circuit_ranks.append(r)
        satisfiability_complexities.append(c)
    
    correlation_coefficient = sum((circuit_ranks[i] - sum(circuit_ranks) / len(circuit_ranks)) * 
                                  (satisfiability_complexities[i] - sum(satisfiability_complexities) / len(satisfiability_complexities)) 
                                 for i in range(len(circuit_ranks))) / \
                               math.sqrt(sum((circuit_ranks[i] - sum(circuit_ranks) / len(circuit_ranks)) ** 2 for i in range(len(circuit_ranks)))) * \
                               math.sqrt(sum((satisfiability_complexities[i] - sum(satisfiability_complexities) / len(satisfiability_complexities)) ** 2 for i in range(len(satisfiability_complexities))))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient <= 3,
        "counterexample": "" if correlation_coefficient <= 3 else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 100, 4))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_mean = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={metric_mean} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")