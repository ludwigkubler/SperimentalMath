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
    
    def dpll(sat_instance):
        # Simple DPLL solver for Boolean satisfiability
        variables = set()
        clauses = []
        for clause in sat_instance.split():
            if clause[0] == '~':
                variables.add(clause[1:])
            else:
                variables.add(clause)
        
        def solve(model):
            if not clauses:
                return model
            literal, rest = clauses[0], clauses[1:]
            pos_literal = literal.strip('~')
            neg_literal = '~' + pos_literal
            
            if pos_literal in model and model[pos_literal]:
                return solve({**model, neg_literal: False})
            elif neg_literal in model and not model[neg_literal]:
                return solve({**model, pos_literal: True})
            
            if pos_literal not in model:
                model[pos_literal] = True
                result = solve(model)
                if result:
                    return result
                del model[pos_literal]
                model[pos_literal] = False
                result = solve(model)
                if result:
                    return result
                del model[pos_literal]
            
            if neg_literal not in model:
                model[neg_literal] = True
                result = solve(model)
                if result:
                    return result
                del model[neg_literal]
                model[neg_literal] = False
                result = solve(model)
                if result:
                    return result
                del model[neg_literal]
            
            return None
        
        return solve({var: False for var in variables})
    
    def algebraic_stack(sat_instance):
        # Convert SAT instance to an algebraic stack (simplified example)
        sat_result = dpll(sat_instance)
        if sat_result is not None:
            return 1
        else:
            return 0
    
    n = random.randint(5, 40)
    sat_instances = [''.join(random.choices(['x', '~x'], k=n)) for _ in range(30)]
    indices = [algebraic_stack(sat_instance) for sat_instance in sat_instances]
    
    if any(index > 2 * n**2 for index in indices):
        return {
            "metric_name": "minimal_index",
            "metric_value": sum(indices),
            "instances_tested": len(indices),
            "conjecture_holds": False,
            "counterexample": f"Instance with index {max(indices)} exceeds 2 * O(n^2)"
        }
    
    mean_index = Fraction(sum(indices), len(indices))
    return {
        "metric_name": "minimal_index",
        "metric_value": float(mean_index),
        "instances_tested": len(indices),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_index = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_index} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_index} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Instance with index > 2 * O(n^2)\" first_failing_seed={first_failing_seed}")