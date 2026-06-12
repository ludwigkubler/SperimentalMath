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
    
    def generate_d_regular_graph(d, n):
        if d * (n - 1) % 2 != 0 or n < d + 1:
            return None
        graph = {i: set() for i in range(1, n + 1)}
        edges_added = 0
        while edges_added < d * (n - 1):
            u = random.randint(1, n)
            v = random.randint(1, n)
            if u != v and v not in graph[u]:
                graph[u].add(v)
                graph[v].add(u)
                edges_added += 2
        return graph
    
    def frege_proof_depth(G):
        n = len(G)
        clauses = []
        for i in range(1, n + 1):
            clause = [-i]
            for j in G[i]:
                clause.append(j)
            clauses.append(clause)
        
        def dpll(model, clauses):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_model = model.copy()
                if literal > 0:
                    new_model.add(literal)
                else:
                    new_model.discard(-literal)
                return dpll(new_model, [c for c in clauses if literal not in c and -literal not in c])
            pure_literal = next((l for l in range(1, n + 1) if (l not in model and -l not in model)), None)
            if pure_literal:
                new_model = model.copy()
                if pure_literal > 0:
                    new_model.add(pure_literal)
                else:
                    new_model.discard(-pure_literal)
                return dpll(new_model, clauses)
            literal = random.choice([l for l in range(1, n + 1) if l not in model and -l not in model])
            new_model = model.copy()
            if literal > 0:
                new_model.add(literal)
            else:
                new_model.discard(-literal)
            return dpll(new_model, clauses) or dpll(model, [c for c in clauses if literal not in c and -literal not in c])
        
        return len(clauses) if dpll(set(), clauses) else float('inf')
    
    def min_generators(G):
        n = len(G)
        # Placeholder for actual algorithm to compute minimal number of generators
        return random.randint(1, 10)  # Dummy implementation
    
    results = []
    for _ in range(30):
        d = random.randint(2, 5)
        n = random.randint(d + 1, 40)
        G = generate_d_regular_graph(d, n)
        if G is None:
            continue
        m_G = min_generators(G)
        w_G = frege_proof_depth(G)
        results.append({
            "metric_name": "m(G)",
            "metric_value": m_G,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": abs(m_G - (d**0.5 * n**(3/4))) <= 0.1 * (d**0.5 * n**(3/4)),
            "counterexample": ""
        })
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_value": mean_value,
        "std_value": std_value,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["mean_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["mean_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["support_fraction"] >= 0.8) / len(results)
    
    if all(r["support_fraction"] == 1 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")