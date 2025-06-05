import sqlite3

data_path = "data/sde_lite.sqlite"

def get_category_info(name: str):
    conn = sqlite3.connect(data_path)
    cursor = conn.cursor()
    cursor.execute("SELECT categoryID FROM typeInfo WHERE typeName = ?", (name,))
    categoryID = cursor.fetchone()[0]
    return categoryID

if __name__ == "__main__":
    pass