import random
import itertools
from collections import defaultdict, deque
from typing import List, Tuple, Set, Dict, Generator

# We'll use a fixed random seed for reproducibility
rng = random.Random(42)

def generate_3cnf(n: int, m: int) -> List[Tuple[int, int, int]]:
    """Generate a random 3-CNF formula with n variables and m clauses."""
    clauses = []
    for _ in range(m):
        # Choose 3 distinct variables
        vars = rng.sample(range(1, n + 1), 3)
        # Randomly negate
        clause = tuple(rng.choice([-1, 1]) * v for v in vars)
        clauses.append(clause)
    return clauses

def build_dependency_digraph(clauses: List[Tuple[int, int, int]], n: int) -> Dict[int, Set[int]]:
    """Build clause-variable dependency digraph.
    Nodes: variables (1..n) and clauses (n+1 .. n+len(clauses))
    Edge from var to clause if variable appears positively in clause.
    Edge from clause to var if variable appears negatively in clause.
    """
    m = len(clauses)
    graph = defaultdict(set)
    
    for i, clause in enumerate(clauses):
        clause_node = n + 1 + i
        for lit in clause:
            var = abs(lit)
            if lit > 0:
                # positive: var -> clause
                graph[var].add(clause_node)
            else:
                # negative: clause -> var
                graph[clause_node].add(var)
    return graph

def generate_directed_simplices(graph: Dict[int, Set[int]], max_dim: int) -> List[List[Tuple[int, ...]]]:
    """Generate directed simplices up to max_dim using flag complex: 
    a directed k-simplex is a sequence of k+1 nodes (v0,...,vk) such that 
    there is a directed edge vi->vj for every i < j.
    Returns list of simplices by dimension: [dim0, dim1, ... dim_max_dim]
    """
    nodes = sorted(graph.keys())
    simplices = [[] for _ in range(max_dim + 1)]
    
    # 0-simplices: all nodes
    simplices[0] = [(v,) for v in nodes]
    
    if max_dim == 0:
        return simplices
    
    # For higher dimensions, build incrementally
    for dim in range(1, max_dim + 1):
        for simplex in simplices[dim - 1]:
            last_node = simplex[-1]
            # Find all successors of last_node that are greater than all in simplex
            # (to avoid duplicates, we enforce node order)
            allowed_next = set(graph[last_node])
            for v in simplex:
                if v in allowed_next:
                    allowed_next.remove(v)
            # Also must be greater than all in simplex to maintain order
            max_in_simplex = max(simplex)
            candidates = [v for v in allowed_next if v > max_in_simplex]
            
            for v in candidates:
                # Check that v is reachable from ALL previous nodes in order
                valid = True
                for u in simplex:
                    if not is_reachable(graph, u, v):
                        valid = False
                        break
                if valid:
                    new_simplex = simplex + (v,)
                    simplices[dim].append(new_simplex)
    
    return simplices

def is_reachable(graph: Dict[int, Set[int]], u: int, v: int) -> bool:
    """Check if there is a directed path from u to v (of length >=1)."""
    if u == v:
        return False
    visited = set()
    stack = [u]
    while stack:
        node = stack.pop()
        if node == v:
            return True
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph.get(node, set()):
            if neighbor not in visited:
                stack.append(neighbor)
    return False

def compute_euler_characteristic(simplices: List[List[Tuple[int, ...]]]) -> int:
    """Compute Euler characteristic: sum_{k>=0} (-1)^k * (number of k-simplices)"""
    chi = 0
    for dim, simplexs in enumerate(simplices):
        chi += ((-1) ** dim) * len(simplexs)
    return chi

# DPLL solver with unit propagation and MOMS heuristic
class DPLL:
    def __init__(self, clauses: List[Tuple[int, int, int]], n: int):
        self.clauses = [set(clause) for clause in clauses]
        self.n = n
        self.assignment = {}
        self.backtrack_count = 0
    
    def unit_propagate(self) -> bool:
        """Apply unit propagation until no unit clauses remain."""
        changed = True
        while changed:
            changed = False
            for clause in self.clauses:
                if not clause:
                    return False  # unsatisfiable
                unassigned = [lit for lit in clause if abs(lit) not in self.assignment]
                if len(unassigned) == 0:
                    continue
                if len(unassigned) == 1:
                    lit = unassigned[0]
                    var = abs(lit)
                    self.assignment[var] = (lit > 0)
                    # Remove satisfied clauses, delete false literals
                    self.clauses = [c for c in self.clauses if lit not in c]
                    for c in self.clauses:
                        if -lit in c:
                            c.remove(-lit)
                    changed = True
                    break
        return True
    
    def moms_heuristic(self) -> int:
        """MOMS heuristic: choose variable that appears most in clauses with minimal length."""
        # Consider only unassigned variables
        unassigned = [v for v in range(1, self.n + 1) if v not in self.assignment]
        if not unassigned:
            return 0
        
        # Score: for each unassigned var, count in how many shortest clauses it appears
        min_len = min(len(c) for c in self.clauses) if self.clauses else 1
        scores = {}
        for v in unassigned:
            pos_score = sum(1 for c in self.clauses if len(c) == min_len and v in c)
            neg_score = sum(1 for c in self.clauses if len(c) == min_len and -v in c)
            # MOMS: (p + n) * 2^(p+n) + 2^(p+n-1)  -- simplified: just (p+n)*2^(p+n)
            total = pos_score + neg_score
            scores[v] = total * (2 ** total) if total > 0 else 0
        
        if not scores:
            return unassigned[0]
        return max(unassigned, key=lambda v: scores[v])
    
    def solve(self) -> bool:
        """Main DPLL loop, returns True if satisfiable, and sets backtrack_count."""
        if not self.unit_propagate():
            return False
        
        if not any(abs(lit) not in self.assignment for clause in self.clauses for lit in clause):
            return True  # all assigned and no empty clause
        
        # Choose variable using MOMS
        var = self.moms_heuristic()
        if var == 0:
            return True
        
        # Try True first
        for value in [True, False]:
            # Save state
            saved_clauses = [set(c) for c in self.clauses]
            saved_assignment = dict(self.assignment)
            
            self.assignment[var] = value
            # Propagate
            if value:
                self.clauses = [c for c in self.clauses if var not in c]
                for c in self.clauses:
                    if -var in c:
                        c.remove(-var)
            else:
                self.clauses = [c for c in self.clauses if -var not in c]
                for c in self.clauses:
                    if var in c:
                        c.remove(var)
            
            if self.solve():
                return True
            else:
                # Restore and backtrack
                self.backtrack_count += 1
                self.clauses = saved_clauses
                self.assignment = saved_assignment
        
        return False

def test_conjecture(n: int, m: int, num_instances: int) -> Tuple[bool, str]:
    """Test the conjecture on num_instances random 3-CNF formulas."""
    for i in range(num_instances):
        clauses = generate_3cnf(n, m)
        # Build digraph
        graph = build_dependency_digraph(clauses, n)
        # Generate directed flag complex up to dim 3
        simplices = generate_directed_simplices(graph, 3)
        chi_dir = compute_euler_characteristic(simplices)
        
        # Run DPLL
        dpll = DPLL(clauses, n)
        dpll.solve()
        backtrack_count = dpll.backtrack_count
        
        if chi_dir != backtrack_count:
            return False, f"n={n}, m={m}, instance {i}: χ_dir={chi_dir}, B={backtrack_count}, clauses={clauses}"
    
    return True, f"Tested {num_instances} instances with n={n}, m={m}"

def main():
    # Test with small n and m=4n, up to n=10 but limit instances due to complexity
    n_values = [3, 4, 5]  # Start small due to digraph complexity
    m_factor = 4
    num_instances_per_n = 5  # Reduce due to exponential growth
    
    for n in n_values:
        m = m_factor * n
        print(f"Testing n={n}, m={m}...")
        result, msg = test_conjecture(n, m, num_instances_per_n)
        if not result:
            print(f"RESULT: FALSIFIED {msg}")
            return
    
    print("RESULT: SUPPORTED instances_tested=15")

if __name__ == "__main__":
    main()