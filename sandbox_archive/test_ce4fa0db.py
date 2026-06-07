# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_geometric_entropy(G):
        n = len(G)
        if n == 0:
            return 0
        max_radius = math.ceil(math.log2(n))
        min_balls = float('inf')
        for radius in range(1, max_radius + 1):
            balls = set()
            for node in G:
                ball = {node}
                queue = [node]
                while queue:
                    current = queue.pop(0)
                    if current not in balls:
                        balls.add(current)
                        for neighbor in G[current]:
                            if neighbor not in balls and abs(neighbor - current) <= radius:
                                queue.append(neighbor)
            min_balls = min(min_balls, len(balls))
        return math.log2(min_balls)
    
    def compute_resolution_width(f):
        n = int(math.log2(len(f)))
        clauses = []
        for i in range(n):
            for j in range(i + 1, n):
                if f[2**i] != f[2**j]:
                    clauses.append([i, -j])
                    clauses.append([-i, j])
        model = {}
        
        def dpll(model, clauses):
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                if literal < 0:
                    literal = -literal
                    model[literal] = False
                else:
                    model[literal] = True
                new_clauses = []
                for c in clauses:
                    if literal not in c and -literal not in c:
                        new_clauses.append(c)
                    elif literal in c:
                        continue
                    else:
                        new_c = [x for x in c if x != -literal]
                        new_clauses.append(new_c)
                return dpll(model, new_clauses)
            unsatisfied_clauses = [c for c in clauses if not any(literal in model and model[literal] or -literal in model and not model[-literal] for literal in c)]
            if not unsatisfied_clauses:
                return True
            literal = unsatisfied_clauses[0][0]
            new_model_true = {**model, literal: True}
            if dpll(new_model_true, clauses):
                return True
            new_model_false = {**model, literal: False}
            return dpll(new_model_false, clauses)
        
        width = 1
        while not dpll(model, clauses):
            model[literal] = True
            width += 1
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_width = 0
        total_entropy = 0
        
        while len(results) < 30:
            f = generate_boolean_function(n)
            G = {i: set() for i in range(2**n)}
            for i in range(2**n):
                for j in range(i + 1, 2**n):
                    if f[i] != f[j]:
                        G[i].add(j)
                        G[j].add(i)
            
            width = compute_resolution_width(f)
            entropy = compute_geometric_entropy(G)
            
            instances_tested += 1
            total_width += width
            total_entropy += entropy
            
            results.append({
                "metric_name": "resolution_width",
                "metric_value": width,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": None,
                "counterexample": ""
            })
    
    mean_width = total_width / len(results)
    std_width = math.sqrt(sum((x['metric_value'] - mean_width) ** 2 for x in results) / len(results))
    
    return {
        "seed": seed,
        "mean_resolution_width": mean_width,
        "std_resolution_width": std_width,
        "instances_tested": len(results),
        "n_max": max(x['n_max'] for x in results),
        "conjecture_holds": None,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_width = sum(x['mean_resolution_width'] for x in results) / len(results)
    std_width = math.sqrt(sum((x['mean_resolution_width'] - mean_width) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x['conjecture_holds']) / len(results)
    
    if all(x['conjecture_holds'] is True for x in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(x['conjecture_holds'] is False for x in results):
        first_failing_seed = next(i for i, x in enumerate(results) if x['conjecture_holds'] is False)
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")