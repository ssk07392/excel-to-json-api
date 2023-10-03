import json

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}


# Function to split rows with "Max Amount" > 49000
def split_rows(row):
    max_amount = row["Amount"]
    if max_amount > 49000:
        num_splits = (max_amount + 49000 - 1) // 49000  # Calculate the number of splits
        new_rows = []
        for i in range(num_splits):
            if i < num_splits - 1:
                split_max_amount = 49000
            else:
                split_max_amount = max_amount - (i * 49000)
            new_row = row.copy()
            new_row["Amount"] = split_max_amount
            new_rows.append(new_row)
        return new_rows
    else:
        return [row]


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
