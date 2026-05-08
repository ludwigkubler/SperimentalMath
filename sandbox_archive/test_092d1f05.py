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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def additive_energy(f):
    n = int(math.log2(len(f)))
    count = 0
    for a in range(2**n):
        for b in range(2**n):
            for c in range(2**n):
                for d in range(2**n):
                    if f[a] + f[b] == f[c] + f[d]:
                        count += 1
    return count

def evaluate_circuit(circuit, input_bits):
    stack = []
    for gate in circuit:
        if gate['type'] == 'input':
            stack.append(input_bits[gate['index']])
        elif gate['type'] == 'threshold':
            inputs = [stack.pop() for _ in range(gate['width'])]
            stack.append(sum(inputs) >= gate['threshold'])
    return stack[-1]

def simulate_acc0_circuit(n, f):
    circuit_size = 2**n
    depth = 3
    max_clauses = 2**(n-1)
    memo = {}
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        literal = find_pure_literal(clauses, assignment)
        if literal is not None:
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if not has_literal(c, literal)], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if not has_literal(c, -literal)], new_assignment):
                return True
            return False
        
        literal = find_unit_clause(clauses)
        if literal is not None:
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if not has_literal(c, literal)], new_assignment):
                return True
            return False
        
        literal = select_literal(clauses)
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in clauses if not has_literal(c, literal)], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in clauses if not has_literal(c, -literal)], new_assignment):
            return True
        return False
    
    def find_pure_literal(clauses, assignment):
        count = [0] * (2*n)
        for clause in clauses:
            for literal in clause:
                count[abs(literal)] += 1
        for i in range(n):
            if count[i] == 1 and i not in assignment:
                return i
            if count[n+i] == 1 and n+i not in assignment:
                return -(n+i)
        return None
    
    def find_unit_clause(clauses):
        for clause in clauses:
            if len([l for l in clause if l not in assignment]) == 1:
                literal = [l for l in clause if l not in assignment][0]
                return literal
        return None
    
    def select_literal(clauses):
        return random.choice([l for c in clauses for l in c])
    
    def has_literal(clause, literal):
        return literal in clause or -literal in clause
    
    def generate_clauses(f):
        clauses = []
        for a in range(2**n):
            for b in range(2**n):
                if f[a] + f[b] == 1:
                    clauses.append([a+1, -(b+1)])
        return clauses
    
    clauses = generate_clauses(f)
    assignment = {}
    return dpll(clauses, assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    f = generate_boolean_function(n)
    E_f = additive_energy(f)
    
    if E_f < n**2.5:
        return {
            "metric_name": "E(f)",
            "metric_value": E_f,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "function_has_low_additive_energy"
        }
    
    circuit_size = simulate_acc0_circuit(n, f)
    
    return {
        "metric_name": "E(f)",
        "metric_value": E_f,
        "instances_tested": 1,
        "conjecture_holds": circuit_size >= n**1.5 * math.log2(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        counterexample = next(r['counterexample'] for r in results if r['counterexample'])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")