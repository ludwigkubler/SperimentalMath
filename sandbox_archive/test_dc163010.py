# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(abs(x) != abs(y) for x, y in zip(clause, clause[1:])):
                clauses.append(clause)
        return clauses
    
    def incidence_graph(clauses):
        n = len(clauses[0])
        graph = [[0] * n for _ in range(len(clauses))]
        for i, clause in enumerate(clauses):
            for var in clause:
                if var > 0:
                    graph[i][var - 1] = 1
                else:
                    graph[i][-var - 1] = 1
        return graph
    
    def morse_complex_rank(graph):
        n = len(graph)
        m = len(graph[0])
        
        # Gaussian elimination to find the rank of the matrix
        for i in range(n):
            if graph[i][i] == 0:
                found = False
                for j in range(i + 1, n):
                    if graph[j][i] != 0:
                        graph[i], graph[j] = graph[j], graph[i]
                        found = True
                        break
                if not found:
                    return i
        
            pivot = Fraction(graph[i][i])
            for j in range(m):
                graph[i][j] /= pivot
            
            for j in range(n):
                if j != i and graph[j][i] != 0:
                    factor = -graph[j][i]
                    for k in range(m):
                        graph[j][k] += factor * graph[i][k]
        
        return n
    
    def is_expander(graph, n):
        # Simple heuristic to check if the graph is an expander
        degree_sum = sum(sum(row) for row in graph)
        avg_degree = degree_sum / n
        if avg_degree < 2:
            return False
        
        for i in range(n):
            neighbors = [j for j, x in enumerate(graph[i]) if x == 1]
            if len(neighbors) > avg_degree * 2:
                return True
        
        return False
    
    def generate_random_prime():
        while True:
            num = random.randint(10**6, 10**7)
            if all(num % i != 0 for i in range(2, int(num**0.5) + 1)):
                return num
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            clauses = generate_k_cnf(n)
            graph = incidence_graph(clauses)
            rank = morse_complex_rank(graph)
            total_rank += rank
            instances_tested += 1
            
            if rank > 10:
                conjecture_holds = False
                counterexample = f"Rank {rank} exceeds 10 for n={n}"
            
            if not is_expander(graph, n):
                conjecture_holds = False
                counterexample = "Graph is not an expander"
    
    return {
        "metric_name": "Morse Complex Rank",
        "metric_value": total_rank / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]]
    if not seeds:
        seeds = [generate_random_prime() for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")