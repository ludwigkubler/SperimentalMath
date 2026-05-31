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
    
    def generate_satisfiability_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def dpll(instance, assignment, path_length=0):
        if not instance:
            return True, path_length
        literal = next(lit for lit in range(len(instance)) if instance[lit] == -1)
        pos_lit = literal * 2
        neg_lit = pos_lit + 1
        
        def extend_assignment(assignment, lit, value):
            new_assignment = assignment[:]
            new_assignment.append((lit, value))
            return new_assignment
        
        if dpll(instance[:pos_lit] + instance[pos_lit+1:neg_lit] + instance[neg_lit+1:], extend_assignment(assignment, pos_lit, 0), path_length + 1)[0]:
            return True, path_length + 1
        elif dpll(instance[:pos_lit] + instance[pos_lit+1:neg_lit] + instance[neg_lit+1:], extend_assignment(assignment, neg_lit, 1), path_length + 1)[0]:
            return True, path_length + 1
        else:
            return False, path_length
    
    def compute_quandle_action_group(instance):
        n = len(instance)
        action_group = []
        for i in range(n):
            for j in range(n):
                if instance[i] != instance[j]:
                    action_group.append((i, j))
        return action_group
    
    def minimal_index(action_group):
        if not action_group:
            return 0
        return len(set(tuple(sorted(pair)) for pair in action_group))
    
    n_values = [5, 10, 15, 20, 30, 40]
    m_indices = []
    w_dpll_values = []
    
    for n in n_values:
        instance = generate_satisfiability_instance(n)
        assignment = [-1] * (n * n)
        path_length = dpll(instance, assignment)[1]
        action_group = compute_quandle_action_group(instance)
        m_index = minimal_index(action_group)
        
        if m_index > 10:
            return {
                "metric_name": "m_index",
                "metric_value": m_index,
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "m_index exceeds 10"
            }
        
        m_indices.append(m_index)
        w_dpll_values.append(path_length)
    
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(m_indices, w_dpll_values)) / math.sqrt(sum((x - mean_x)**2 for x in m_indices) * sum((y - mean_y)**2 for y in w_dpll_values))
    mean_m_index = sum(m_indices) / len(m_indices)
    
    return {
        "metric_name": "m_index",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_m_index = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_m_index} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and max(r["n_max"] for r in results) >= 16:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"m_index exceeds 10\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(seeds)}")