import heapq

# Graph dua arah (biar bisa maju & mundur)
graph = {
    'Gerbang': {'Parkiran Teknik': 2},
    'Parkiran Teknik': {'Gerbang': 2, 'Gedung Mektan': 3},
    'Gedung Mektan': {'Parkiran Teknik': 3, 'Gedung H': 2},
    'Gedung H': {'Gedung Mektan': 2, 'Tabek': 2},
    'Tabek': {'Gedung H': 2, 'LAB Elektro': 3},
    'LAB Elektro': {'Tabek': 3}
}

# Estimasi jarak ke LAB Elektro (heuristik A*)
heuristic = {
    'Gerbang': 10,
    'Parkiran Teknik': 8,
    'Gedung Mektan': 6,
    'Gedung H': 4,
    'Tabek': 2,
    'LAB Elektro': 0
}

def astar_search(graph, start, goal, heuristic):
    open_set = []
    heapq.heappush(open_set, (0 + heuristic[start], 0, start, [start]))
    visited = set()

    while open_set:
        est_total, cost, node, path = heapq.heappop(open_set)

        if node in visited:
            continue
        visited.add(node)

        if node == goal:
            return path, cost

        for neighbor in graph[node]:
            if neighbor not in visited:
                total_cost = cost + graph[node][neighbor]
                est_total_cost = total_cost + heuristic[neighbor]
                heapq.heappush(open_set, (est_total_cost, total_cost, neighbor, path + [neighbor]))

    return None, float('inf')

# Input dari user
print("📍 Tempat yang tersedia:")
for lokasi in graph:
    print("-", lokasi)

start = input("\nMasukkan tempat awal: ").strip()
goal = input("Masukkan tujuan akhir: ").strip()

# Validasi input
if start not in graph or goal not in graph:
    print("❌ Tempat tidak valid. Pastikan nama sesuai daftar.")
else:
    path, cost = astar_search(graph, start, goal, heuristic)
    if path:
        print(f"\n✅ Rute terbaik dari {start} ke {goal}:")
        print(" -> ".join(path))
        print("🛣️ Total jarak:", cost)
    else:
        print(f"❌ Tidak ditemukan rute dari {start} ke {goal}.")
