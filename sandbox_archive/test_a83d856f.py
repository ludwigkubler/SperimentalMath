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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n) if random.choice([True, False]) else -random.randint(1, n) for _ in range(random.randint(1, 3))]
            cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        queue = set()
        seen = set()
        for clause in cnf:
            queue.add(tuple(sorted(clause)))
        
        while queue:
            current_clause = min(queue, key=len)
            if len(current_clause) == 1:
                return len(seen)
            
            literal = current_clause[0]
            other_clauses = [c for c in queue if literal in c or -literal in c]
            seen.add(literal)
            queue.remove(current_clause)
            
            for clause in other_clauses:
                new_clause = list(set(clause) - {literal, -literal})
                if new_clause and tuple(sorted(new_clause)) not in seen:
                    queue.add(tuple(sorted(new_clause)))
        
        return len(seen)
    
    def formal_context(cnf):
        universe = set(range(1, 2**len(cnf[0]) + 1))
        minterms = [tuple([i for i in range(len(cnf)) if literal in cnf[i] or -literal not in cnf[i]]) for literal in universe]
        non_minterms = [tuple([i for i in range(len(cnf)) if literal not in cnf[i] and -literal in cnf[i]]) for literal in universe]
        return minterms + non_minterms
    
    def min_rank(context):
        n = len(context)
        rank = 0
        while context:
            row = context.pop(0)
            rank += 1
            context = [c for c in context if not any(x in c for x in row)]
        return rank
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        m = random.randint(n, 2*n)
        cnf = generate_cnf(n, m)
        width = resolution_width(cnf)
        context = formal_context(cnf)
        rank = min_rank(context)
        
        results.append({
            "n": n,
            "m": m,
            "width": width,
            "rank": rank
        })
    
    if not results:
        return {
            "metric_name": "min_rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_width = sum(r["width"] for r in results) / len(results)
    mean_rank = sum(r["rank"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["rank"] - mean_rank)**2 for r in results) / len(results))
    
    correlation_coefficient = sum((r["width"] - mean_width) * (r["rank"] - mean_rank) for r in results) / (len(results) * std_dev * math.sqrt(mean_width))
    
    conjecture_holds = correlation_coefficient > 0.9
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.9"
    
    return {
        "metric_name": "min_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")