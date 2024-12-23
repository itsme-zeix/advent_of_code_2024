from itertools import combinations

def process_input():
  with open("./day-23/input.txt", "r") as f:
    connections = f.read().split()
    return connections

def solve_part1():
  connections = process_input()
  graph = {}
  
  for connection in connections:
    c1, c2 = connection.split('-')
    graph.setdefault(c1, set()).add(c2)
    graph.setdefault(c2, set()).add(c1)
  
  triplets_with_t = set()
  for node, neighbours in graph.items():
    if 't' not in node: continue

    for a, b in combinations(neighbours, 2):
      if a in graph[b]:
        triplets_with_t.add(frozenset([node, a, b]))

  return len(triplets_with_t)

def solve_part2():
  connections = process_input()
  graph = {}
  
  for connection in connections:
    c1, c2 = connection.split('-')
    graph.setdefault(c1, set()).add(c2)
    graph.setdefault(c2, set()).add(c1)

  # Build adjacency matrix
  adj_matrix = [[0] * len(graph) for _ in range(len(graph))]
  index = {node: index for index, node in enumerate(graph.keys())}
  index_to_node = {index: node for index, node in enumerate(graph.keys())}
  for node, connections in graph.items():
    for neighbour in connections:
      adj_matrix[index[node]][index[neighbour]] = 1
      adj_matrix[index[neighbour]][index[node]] = 1

  # Get max cliques
  max_clique_indexes = compute_max_clique(adj_matrix)
  max_clique = [index_to_node[i] for i in max_clique_indexes]

  return ",".join(sorted(max_clique))

def compute_max_clique(adj_matrix):
  def helper(clique, candidates):
    # Base case
    if not candidates:
      return clique

    largest_clique = clique
    for i in range(len(candidates)):
      candidate = candidates[i]
      new_clique = clique + [candidate]
      # candidates[i + 1:] to avoid revisiting candidates that are already visited.
      new_candidates = [c for c in candidates[i + 1:] if adj_matrix[candidate][c]]
      
      candidate_clique = helper(new_clique, new_candidates)
      if len(candidate_clique) > len(largest_clique):
        largest_clique = candidate_clique

    return largest_clique

  return helper([], list(range(len(adj_matrix))))


if __name__ == "__main__":
  print(solve_part1())
  print(solve_part2())
