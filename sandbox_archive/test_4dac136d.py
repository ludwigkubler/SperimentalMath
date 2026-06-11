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
        for _ in range(m):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(random.randint(1, m))]
            cnf.append(literals)
        return cnf
    
    def formal_context(cnf):
        context = {}
        for literal in set(abs(lit) for lit in sum(cnf, [])):
            context[literal] = [i for i, clause in enumerate(cnf) if literal in clause or -literal in clause]
        return context
    
    def resolution_proof_depth(cnf):
        stack = cnf[:]
        depth = 0
        while True:
            new_clause = None
            for i in range(len(stack)):
                for j in range(i + 1, len(stack)):
                    if any(-lit in stack[i] and lit in stack[j] for lit in set(abs(lit) for lit in stack[i])):
                        new_clause = [lit for lit in stack[i] if lit not in stack[j]] + [lit for lit in stack[j] if -lit not in stack[i]]
                        break
                if new_clause:
                    break
            if new_clause is None:
                return depth
            stack.append(new_clause)
            depth += 1
    
    def min_index(context):
        indices = {}
        for literal, extent in context.items():
            indices[literal] = len(extent) * sum(len(extent) - len(intersection) for intersection in (context.get(-lit, []) for lit in extent))
        return sum(indices.values())
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        context = formal_context(cnf)
        depth = resolution_proof_depth(cnf)
        index = min_index(context)
        
        if index > depth:
            return {
                "metric_name": "min_index",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"min_index({index}) > resolution_depth({depth})"
            }
        
        results.append((index, depth))
    
    if len(results) < 30:
        return {
            "metric_name": "min_index",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    indices, depths = zip(*results)
    correlation = sum((x - mean(indices)) * (y - mean(depths)) for x, y in results) / math.sqrt(sum((x - mean(indices)) ** 2 for x in indices) * sum((y - mean(depths)) ** 2 for y in depths))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
    }

def mean(values):
    return sum(values) / len(values)

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 99983) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = mean([r["metric_value"] for r in results])
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")