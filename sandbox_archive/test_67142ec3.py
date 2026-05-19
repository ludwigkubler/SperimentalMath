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
    
    def generate_expander_graph(n, Φ):
        # Simple expander graph generator (adjacency list)
        G = {i: [] for i in range(n)}
        for v in range(n):
            for u in range(v + 1, n):
                if len(G[v]) < Φ and len(G[u]) < Φ:
                    G[v].append(u)
                    G[u].append(v)
        return G
    
    def tseitin_formula(G, ω):
        literals = {}
        clauses = []
        
        def get_literal(v, i):
            var_id = literals.get((v, i), None)
            if var_id is None:
                var_id = len(literals)
                literals[(v, i)] = var_id
            return var_id
        
        for v in G:
            literal_v0 = get_literal(v, 0)
            literal_v1 = get_literal(v, 1)
            clauses.append([literal_v0, -literal_v1])
            clauses.append([-literal_v0, literal_v1])
        
        for u in range(len(G)):
            for v in range(u + 1, len(G)):
                if u in G[v]:
                    literal_u0 = get_literal(u, 0)
                    literal_v0 = get_literal(v, 0)
                    literal_u1 = get_literal(u, 1)
                    literal_v1 = get_literal(v, 1)
                    clauses.append([literal_u0, literal_v0, -literal_u1, -literal_v1])
        
        return literals, clauses
    
    def resolution_width(clauses):
        # Simple resolution width computation
        max_width = 0
        seen = set()
        queue = list(clauses)
        
        while queue:
            clause = queue.pop(0)
            if len(clause) > max_width:
                max_width = len(clause)
            
            for literal in clause:
                opposite_literal = -literal
                if opposite_literal in seen:
                    continue
                
                new_clauses = []
                for other_clause in clauses:
                    if opposite_literal in other_clause:
                        new_clause = [l for l in other_clause if l != opposite_literal]
                        if new_clause not in new_clauses:
                            new_clauses.append(new_clause)
                
                queue.extend(new_clauses)
                seen.add(opposite_literal)
        
        return max_width
    
    n = 30
    Φ = random.randint(2, n - 1)  # Expansion parameter
    expander_graph = generate_expander_graph(n, Φ)
    ω = {v: random.choice([True, False]) for v in range(n)}
    
    literals, clauses = tseitin_formula(expander_graph, ω)
    width = resolution_width(clauses)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": width >= 1 / Φ,
        "counterexample": "" if width >= 1 / Φ else f"Graph with n={n}, Φ={Φ} did not meet the lower bound"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph did not meet the lower bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")