import requests
import pandas as pd

def fetch_data_and_save_to_csv(transect_ids, output_csv):
    base_url = "http://coastsat.wrl.unsw.edu.au/time-series/"
    data_list = []

#     for transect_id in transect_ids:
#         url = base_url + str(transect_id)
#         response = requests.get(url)
#
#         if response.status_code == 200:
#             # Assuming the data returned is in JSON format
#             data = response.json()
#             data_list.append(data)
#
#     # Convert the list of data into a DataFrame
#     df = pd.DataFrame(data_list)
#
#     # Save the DataFrame to a CSV file
#     df.to_csv(output_csv, index=False)
#
# if __name__ == "__main__":
#     # Replace these with your desired transect IDs
#     transect_ids_to_fetch = [1, 2, 3, 4, 5]
#
#     # Replace "output.csv" with the desired name for the CSV file
#     fetch_data_and_save_to_csv(transect_ids_to_fetch, "output.csv")
