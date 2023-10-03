import random
import string

from flask import Flask, render_template, request,jsonify
import pandas as pd
import os
from functions import split_rows,allowed_file
import json
import requests

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file and allowed_file(file.filename):
        # Save the uploaded file

        #filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        upload_dir = os.path.join(os.path.dirname(__file__),app.config['UPLOAD_FOLDER'])
        # Then, you can use the full path to save the uploaded file
        filename = os.path.join(upload_dir, file.filename)
        if os.path.exists(filename):
            # If the file exists, delete it
            os.remove(filename)

            # Save the uploaded file
        file.save(filename)

        # Read the Excel file using pandas
        df = pd.read_excel(filename)
        df = df.map(lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if isinstance(x, pd.Timestamp) else x)
        # Mapping of equivalent column names to standardized column names
        column_mapping = {
            "sl no": "SR",
            "max amount": "Amount",
            "bank name": "Bank",
            "account number": "Account",
            "ifsc code": "IFSC",
            "name": "Name",
        }

        # Rename columns based on the mapping
        # Rename columns based on the mapping
        df.columns = df.columns.str.lower()
        df.rename(columns=column_mapping, inplace=True)

        # Apply the split_rows function to each row and flatten the result, then append to the original DataFrame
        new_rows = []
        for i, row in df.iterrows():
            split_data = split_rows(row)
            new_rows.extend(split_data)

        # Create a new DataFrame with the split data
        split_df = pd.DataFrame(new_rows)
        # Concatenate the original DataFrame with the split DataFrame
       # df = pd.concat([df, split_df], ignore_index=True)
        split_df = split_df.map(lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if isinstance(x, pd.Timestamp) else x)
        split_df['status'] = 'default'
        split_df['utr'] = ''
        # You can now work with the DataFrame 'df'
        data_dict = split_df.to_dict(orient='records')

        # Convert the dictionary to JSON
        #json_data = json.dumps(data_dict)

        # Return JSON response
        return data_dict#render_template('table.html',data=data_dict)
    else:
        return 'Invalid file format'


@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        # Simulate a random success or failure status
        status = random.choice([True, False])

        # Simulate random data or null data if status is false
        data = generate_random_data(request.form) if status else None

        response = {
            "message": "Success" if status else "Failure",
            "status": status,
            "data": data
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({
            "message": "Error",
            "status": False,
            "data": str(e)
        })

def generate_random_data(request_data):
    data = {"id": random.randint(1, 100),
            "member_id": ''.join(random.choices(string.ascii_letters + string.digits, k=16)),
            "amount": request_data.get('amount'), "status": "Success" if random.choice([True, False]) else "Failed",
            "payment_method": "IMPS", "utr": ''.join(random.choices(string.digits, k=16)),
            "gateway_id": random.randint(1, 1000000), "created_at": "2023-08-28 11:46:40",
            "updated_at": "2023-08-28 11:46:46", "is_refunded": random.choice([0, 1]),
            "status_count": random.randint(0, 10), "merchant_ref_no": request_data.get('merchant_ref_no'),
            "commission": round(random.uniform(1, 10), 2), "customer_name": "Random Name",
            "customer_account_number": ''.join(random.choices(string.digits, k=12)),
            "customer_ifsc": "IFSC" + ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
            "customer_mobile": "9" + ''.join(random.choices(string.digits, k=9)),
            "account_number": request_data.get('account_number'), "bank_name": request_data.get('bank_name'),
            "ifsc_code": request_data.get('ifsc_code'), "name": request_data.get('name'),
            "email": request_data.get('email'), "mobile_number": request_data.get('mobile_number')}

    # Replace specific parameters with values from the request

    return data


if __name__ == '__main__':
    app.run(debug=True)


