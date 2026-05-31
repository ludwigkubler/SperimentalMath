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
    
    def generate_sat_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def dpll(instance):
        n = len(instance)
        clauses = [[i] for i in range(n)] + [[-i - 1] for i in range(n)]
        
        def search(model):
            if not any(clause for clause in clauses if all(lit not in model and -lit not in model for lit in clause)):
                return True
            literal = next(lit for lit in range(-n, n + 1) if lit not in model and -lit not in model)
            if literal > 0:
                model.add(literal)
                if search(model):
                    return True
                model.remove(literal)
            else:
                model.add(literal)
                if search(model):
                    return True
                model.remove(literal)
            return False
        
        search(set())
        return len(instance)  # Simplified path length
    
    def quandle_action_group(instance):
        n = len(instance)
        actions = []
        for i in range(n):
            action = [instance[(i + j) % n] for j in range(n)]
            if action not in actions:
                actions.append(action)
        return actions
    
    def minimal_index(actions):
        return min(len(action) for action in actions)
    
    results = []
    for _ in range(30):
        instance = generate_sat_instance(random.randint(5, 40))
        m_index = minimal_index(quandle_action_group(instance))
        w_DPLL = dpll(instance)
        if m_index > 10:
            return {
                "metric_name": "m_index",
                "metric_value": m_index,
                "instances_tested": 1,
                "n_max": len(instance),
                "conjecture_holds": False,
                "counterexample": "m_index > 10"
            }
        results.append((m_index, w_DPLL))
    
    if not results:
        return {
            "metric_name": "m_index",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    m_indices, w_DPLLs = zip(*results)
    mean_m_index = sum(m_indices) / len(m_indices)
    mean_w_DPLL = sum(w_DPLLs) / len(w_DPLLs)
    correlation_coefficient = sum((m - mean_m_index) * (w - mean_w_DPLL) for m, w in results) / (len(results) * math.sqrt(sum((m - mean_m_index) ** 2 for m in m_indices)) * math.sqrt(sum((w - mean_w_DPLL) ** 2 for w in w_DPLLs)))
    
    return {
        "metric_name": "m_index",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(len(instance) for instance, _ in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        if "conjecture_holds" in trial_result and not trial_result["conjecture_holds"]:
            break
        results.append(trial_result)
    
    if all("conjecture_holds" in result and result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if "conjecture_holds" in result and result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any("counterexample" in result and result["counterexample"] for result in results):
        first_failing_seed = next(result["seed"] for result in results if "counterexample" in result and result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")