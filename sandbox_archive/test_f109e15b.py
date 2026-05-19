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
    
    def generate_expander_graph(n, phi):
        # Generate a random expander graph using the adjacency list representation
        adj_list = [[] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < phi / (n - 1):
                    adj_list[i].append(j)
                    adj_list[j].append(i)
        return adj_list
    
    def tseitin_formula(adj_list, omega):
        # Construct the Tseitin formula for the expander graph
        clauses = []
        literals = {}
        var_id = 0
        
        def add_clause(clause):
            clauses.append(clause)
        
        def get_literal(v, i):
            if (v, i) not in literals:
                literals[(v, i)] = var_id
                var_id += 1
            return literals[(v, i)]
        
        for v in range(len(adj_list)):
            literal_v0 = get_literal(v, 0)
            literal_v1 = get_literal(v, 1)
            add_clause([-literal_v0, -literal_v1])
            add_clause([literal_v0])
            add_clause([literal_v1])
            
            for u in adj_list[v]:
                literal_u0 = get_literal(u, 0)
                literal_u1 = get_literal(u, 1)
                add_clause([-literal_v0, literal_u0])
                add_clause([-literal_v1, literal_u1])
        
        return clauses
    
    def resolution_width(clauses):
        # Compute the resolution width of the formula
        queue = [set(c) for c in clauses]
        learned_clauses = []
        max_width = 0
        
        while True:
            new_clause = None
            for clause1, clause2 in combinations(queue, 2):
                if len(clause1 & clause2) == 1:
                    new_clause = (clause1 - clause2).union(clause2 - clause1)
                    break
            if new_clause is None:
                break
            
            max_width = max(max_width, len(new_clause))
            queue.append(new_clause)
        
        return max_width
    
    def generate_balanced_assignment(n):
        # Generate a balanced assignment for the variables
        omega = {i: (n - i) / n for i in range(n)}
        return omega
    
    n = 40
    phi = random.uniform(2, 3)
    expander_graph = generate_expander_graph(n, phi)
    omega = generate_balanced_assignment(n)
    tseitin_clauses = tseitin_formula(expander_graph, omega)
    width = resolution_width(tseitin_clauses)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": width >= Fraction(1, phi),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")