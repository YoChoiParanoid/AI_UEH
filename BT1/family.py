# family.py

from pyDatalog import pyDatalog

# --- 1. Khởi tạo và xóa mọi thứ ---
pyDatalog.clear()
pyDatalog.create_terms(
    'father, mother, parent, grandparent, sibling, uncle, spouses, '
    'X, Y, Z, C'
)

# --- 2. Nhúng JSON vào biến data ---
data = {
    "father": [
        {"John": "William"}, {"John": "David"}, {"John": "Adam"},
        {"William": "Chris"}, {"William": "Stephanie"},
        {"David": "Wayne"}, {"David": "Tiffany"}, {"David": "Julie"},
        {"David": "Neil"}, {"David": "Peter"},
        {"Adam": "Sophia"}
    ],
    "mother": [
        {"Megan": "William"}, {"Megan": "David"}, {"Megan": "Adam"},
        {"Emma": "Stephanie"}, {"Emma": "Chris"},
        {"Olivia": "Tiffany"}, {"Olivia": "Julie"},
        {"Olivia": "Neil"}, {"Olivia": "Peter"},
        {"Lily": "Sophia"}
    ]
}

# --- 3. Thêm fact bằng cú pháp “+ predicate(arg1,arg2)” ---
for rec in data['father']:
    dad, ch = next(iter(rec.items()))
    + father(dad, ch)

for rec in data['mother']:
    mom, ch = next(iter(rec.items()))
    + mother(mom, ch)

# --- 4. Định nghĩa các rule ---
# parent(X,Y)  nếu X là father(X,Y) hoặc mother(X,Y)
parent(X, Y) <= father(X, Y)
parent(X, Y) <= mother(X, Y)

# grandparent(X,Y) nếu X là cha/mẹ của Z và Z là cha/mẹ của Y
grandparent(X, Y) <= parent(X, Z) & parent(Z, Y)

# sibling(X,Y) nếu X và Y có cùng một phụ huynh Z, và X != Y
sibling(X, Y) <= parent(Z, X) & parent(Z, Y) & (X != Y)

# uncle(X,Y) nếu tồn tại P mà P là parent(P,Y) và X là sibling của P
uncle(X, Y) <= parent(Z, Y) & sibling(X, Z)

# spouses(X,Y) nếu có một đứa con C sao cho father(X,C) và mother(Y,C)
spouses(X, Y) <= father(X, C) & mother(Y, C) & (X != Y)

# --- 5. Chạy các query và in kết quả ---
if __name__ == '__main__':

    # 1. Con của John
    print("1. Con của John:", father('John', X).data)

    # 2. Mẹ của William (lấy 1 kết quả đầu nếu có)
    moms = mother(X, 'William').data
    print("2. Mẹ của William:", moms[0][0] if moms else "Không có dữ liệu")

    # 3. Cha mẹ của Adam
    print("3. Cha mẹ của Adam:", parent(X, 'Adam').data)

    # 4. Ông bà của Wayne
    print("4. Ông bà của Wayne:", grandparent(X, 'Wayne').data)

    # 5. Các cháu của Megan
    print("5. Các cháu của Megan:", grandparent('Megan', X).data)

    # 6. Anh/chị/em của David
    sibs = [r[0] for r in sibling(X, 'David').data]
    print("6. Anh/chị/em của David:", sibs)

    # 7. Chú của Tiffany (loại bỏ cha nếu vô tình lọt vào)
    #    tìm trước cha của Tiffany để loại
    dads = father(X, 'Tiffany').data
    tf = dads[0][0] if dads else None
    uncs = [r[0] for r in uncle(X, 'Tiffany').data if r[0] != tf]
    print("7. Chú của Tiffany:", uncs)

    # 8. Danh sách các cặp vợ chồng
    couples = [(r[0], r[1]) for r in spouses(X, Y).data]
    print("8. Danh sách các cặp vợ chồng:")
    for h, w in couples:
        print(f"   Chồng: {h}  <==>  Vợ: {w}")
