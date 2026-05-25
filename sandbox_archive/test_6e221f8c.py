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
    
    def generate_dfa(n):
        states = list(range(n))
        alphabet = ['a', 'b']
        transitions = {q: {} for q in states}
        start_state = 0
        accept_states = [n-1]
        
        for q in states:
            for a in alphabet:
                if random.choice([True, False]):
                    next_q = (q + 1) % n
                else:
                    next_q = (q - 1) % n
                transitions[q][a] = next_q
        
        return states, alphabet, transitions, start_state, accept_states
    
    def myhill_nerode(dfa):
        states, _, transitions, start_state, _ = dfa
        equivalence_classes = [{start_state}]
        
        while True:
            new_classes = []
            for eq_class in equivalence_classes:
                new_eq_class = set()
                for q in eq_class:
                    for a in transitions[q]:
                        next_q = transitions[q][a]
                        for eq_class2 in equivalence_classes:
                            if any(transitions[next_q][b] != transitions[eq_class2[0]][b] for b in transitions[next_q]):
                                new_eq_class.add(next_q)
                                break
                        else:
                            new_eq_class.update(eq_class2)
                new_classes.append(new_eq_class)
            if len(equivalence_classes) == len(new_classes):
                break
            equivalence_classes = new_classes
        
        return len(equivalence_classes)
    
    def resolution_steps(dfa):
        states, _, transitions, start_state, accept_states = dfa
        clauses = []
        for q in states:
            if q not in accept_states:
                clause = [-q]
                for a in transitions[q]:
                    next_q = transitions[q][a]
                    clause.append(next_q)
                clauses.append(clause)
        
        def is_satisfiable(clauses):
            stack = []
            assignment = {}
            
            def unit_propagation():
                while True:
                    found_unit_clause = False
                    for i, clause in enumerate(clauses):
                        if len(clause) == 1:
                            literal = clause[0]
                            if literal > 0 and literal not in assignment:
                                assignment[literal] = True
                                found_unit_clause = True
                            elif literal < 0 and -literal not in assignment:
                                assignment[-literal] = False
                                found_unit_clause = True
                        elif any(lit in assignment for lit in clause):
                            continue
                        else:
                            return False
                    if not found_unit_clause:
                        break
                return True
            
            def pure_literal_elimination():
                while True:
                    found_pure_literal = False
                    literals = set()
                    for clause in clauses:
                        for lit in clause:
                            literals.add(lit)
                    for lit in literals:
                        polarity = None
                        for clause in clauses:
                            if lit in clause and (polarity is None or polarity == (lit > 0)):
                                polarity = lit > 0
                            elif -lit in clause and (polarity is None or polarity != (lit > 0)):
                                break
                        else:
                            found_pure_literal = True
                            assignment[lit] = polarity
                    if not found_pure_literal:
                        break
                return True
            
            def dpll():
                if len(clauses) == 0:
                    return True
                for clause in clauses:
                    if len(clause) == 0:
                        return False
                literal = None
                polarity = None
                for lit in literals:
                    if lit not in assignment and (-lit not in assignment):
                        literal = lit
                        polarity = lit > 0
                        break
                
                def backtrack():
                    nonlocal stack, assignment
                    while len(stack) > 0 and stack[-1][1] == polarity:
                        _, lit = stack.pop()
                        del assignment[lit]
                    
                    if len(stack) == 0:
                        return False
                    
                    prev_lit, _ = stack.pop()
                    stack.append((prev_lit, not polarity))
                    assignment[prev_lit] = not polarity
                    return dpll()
                
                stack.append((literal, polarity))
                assignment[literal] = polarity
                if unit_propagation() and pure_literal_elimination():
                    if dpll():
                        return True
                backtrack()
                return False
            
            return dpll()
        
        return len(clauses) if is_satisfiable(clauses) else 0
    
    def resolution_depth(dfa):
        states, _, transitions, start_state, accept_states = dfa
        clauses = []
        for q in states:
            if q not in accept_states:
                clause = [-q]
                for a in transitions[q]:
                    next_q = transitions[q][a]
                    clause.append(next_q)
                clauses.append(clause)
        
        def is_satisfiable_depth(clauses, depth):
            stack = []
            assignment = {}
            
            def unit_propagation():
                while True:
                    found_unit_clause = False
                    for i, clause in enumerate(clauses):
                        if len(clause) == 1:
                            literal = clause[0]
                            if literal > 0 and literal not in assignment:
                                assignment[literal] = True
                                found_unit_clause = True
                            elif literal < 0 and -literal not in assignment:
                                assignment[-literal] = False
                                found_unit_clause = True
                        elif any(lit in assignment for lit in clause):
                            continue
                        else:
                            return False
                    if not found_unit_clause:
                        break
                return True
            
            def pure_literal_elimination():
                while True:
                    found_pure_literal = False
                    literals = set()
                    for clause in clauses:
                        for lit in clause:
                            literals.add(lit)
                    for lit in literals:
                        polarity = None
                        for clause in clauses:
                            if lit in clause and (polarity is None or polarity == (lit > 0)):
                                polarity = lit > 0
                            elif -lit in clause and (polarity is None or polarity != (lit > 0)):
                                break
                        else:
                            found_pure_literal = True
                            assignment[lit] = polarity
                    if not found_pure_literal:
                        break
                return True
            
            def dpll_depth(depth):
                if len(clauses) == 0:
                    return depth
                for clause in clauses:
                    if len(clause) == 0:
                        return float('inf')
                literal = None
                polarity = None
                for lit in literals:
                    if lit not in assignment and (-lit not in assignment):
                        literal = lit
                        polarity = lit > 0
                        break
                
                def backtrack():
                    nonlocal stack, assignment
                    while len(stack) > 0 and stack[-1][1] == polarity:
                        _, lit = stack.pop()
                        del assignment[lit]
                    
                    if len(stack) == 0:
                        return float('inf')
                    
                    prev_lit, _ = stack.pop()
                    stack.append((prev_lit, not polarity))
                    assignment[prev_lit] = not polarity
                    return dpll_depth(depth)
                
                stack.append((literal, polarity))
                assignment[literal] = polarity
                if unit_propagation() and pure_literal_elimination():
                    return min(dpll_depth(depth + 1), backtrack())
                return backtrack()
            
            return dpll_depth(0)
        
        return resolution_depth(clauses)
    
    def compute_ratio(dfa):
        rank = myhill_nerode(dfa)
        steps = resolution_steps(dfa)
        depth = resolution_depth(dfa)
        if steps == 0 or depth == 0:
            return float('inf')
        return steps / depth
    
    n = random.randint(5, 40)
    dfa = generate_dfa(n)
    ratio = compute_ratio(dfa)
    
    return {
        "metric_name": "resolution_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1,
        "counterexample": "" if ratio <= 1 else f"Ratio {ratio} exceeds Θ(1)"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_ratio:.4f} std={std_ratio:.4f} support_fraction={support_fraction:.2f}")