# states.py

from pyDatalog import pyDatalog

# --- 1. Khởi tạo Datalog và các predicate ---
pyDatalog.clear()
pyDatalog.create_terms(
    'adjacent, coastal, border_coastal, common_adj, X, Y, N'
)

# --- 2. Định nghĩa rule ---
# border_coastal(X): X giáp với ít nhất một bang ven biển Y
border_coastal(X) <= adjacent(X, Y) & coastal(Y)
# common_adj(X): X giáp đồng thời Arkansas và Kentucky
common_adj(X) <= adjacent('Arkansas', X) & adjacent('Kentucky', X)

# --- 3. Đọc dữ liệu từ file ---
file_coastal   = 'BT2/coastal_states.txt'
file_adjacent = 'BT2/adjacent_states.txt'

# Đọc danh sách bang ven biển
with open(file_coastal, 'r') as f:
    line = f.read().strip()
    coastal_states = [s.strip() for s in line.split(',') if s.strip()]

# Thêm facts "coastal(state)"
for state in coastal_states:
    + coastal(state)

# Đọc danh sách thôn tính / liền kề
with open(file_adjacent, 'r') as f:
    adjlist = [line.strip().split(',') for line in f
               if line.strip() and line[0].isalpha()]

# Thêm facts "adjacent(A, B)" cho mỗi cặp
for L in adjlist:
    head, tail = L[0].strip(), [s.strip() for s in L[1:]]
    for state in tail:
        + adjacent(head, state)

# --- 4. Chạy các query và in kết quả ---
if __name__ == '__main__':
    # 1. Kiểm tra Nevada có giáp Louisiana?
    result = adjacent('Nevada', 'Louisiana').data
    print("\n1. Nevada giáp Louisiana?:", 'Yes' if result else 'No')

    # 2. Danh sách bang giáp Oregon
    oregon_neighbors = [r[0] for r in adjacent('Oregon', X).data]
    print("\n2. Các bang giáp Oregon:")
    for st in oregon_neighbors:
        print(st)

    # 3. Các bang ven biển giáp Mississippi
    ms_coastal = [r[0] for r in adjacent('Mississippi', X).data
                  if coastal(X).data and (r[0] in coastal_states)]
    # Tuy nhiên, để dùng rule, ta có thể query: adjacent('Mississippi', X) & coastal(X)
    ms_coastal = [r[0] for r in (adjacent('Mississippi', X) & coastal(X)).data]
    print("\n3. Các bang ven biển giáp Mississippi:")
    for st in ms_coastal:
        print(st)

    # 4. Bảy bang bất kỳ giáp với một bang ven biển
    seven = [r[0] for r in border_coastal(X).data][:7]
    print("\n4. Bảy bang giáp ít nhất một bang ven biển:")
    for st in seven:
        print(st)

    # 5. Bang giáp đồng thời Arkansas và Kentucky
    common = [r[0] for r in common_adj(X).data]
    print("\n5. Các bang giáp cả Arkansas và Kentucky:")
    for st in common:
        print(st)
