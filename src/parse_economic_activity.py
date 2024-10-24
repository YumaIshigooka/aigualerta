import csv
import os
from datetime import datetime

def parse_water_activity_data(file_path):
    """
    Parses a CSV file containing water consumption and economic activity data and returns structured data.

    :param file_path: Path to the CSV file
    :return: List of dictionaries with parsed water consumption and economic activity data
    """
    water_activity_data = []

    # Open the CSV file and parse its content
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        
        # Loop through each row in the CSV
        for row in csv_reader:
            try:
                # Parse the date field
                date = datetime.strptime(row['Data/Fecha/Date'], '%Y-%m-%d')  # Adjust format if necessary
                
                # Parse water-related data and economic activity details
                district = row['Districte/Distrito/District'].strip()
                municipality = row['Municipi/Municipio/Municipality'].strip()
                use = row['Ús/Uso/Use'].strip()
                economic_activity = row['Activitat econòmica/Actividad económica/Economic activity'].strip()
                economic_activity_desc = row['Descripció activitat econòmica/Descripción actividad económica/Economic activity description'].strip()
                number_of_meters = int(row['Nombre de comptadors/Número de contadores/Number of meters'])
                accumulated_consumption = float(row['Consum acumulat (L/dia)/Consumo acumulado (L/día)/Accumulated consumption (L/day)'])

                # Append parsed data as a dictionary
                water_activity_data.append({
                    'date': date,
                    'district': district,
                    'municipality': municipality,
                    'use': use,
                    'economic_activity': economic_activity,
                    'economic_activity_desc': economic_activity_desc,
                    'number_of_meters': number_of_meters,
                    'accumulated_consumption': accumulated_consumption
                })
            except ValueError as e:
                print(f"Skipping row due to parsing error: {e}")
    
    return water_activity_data


# Example usage:
dirname = os.path.dirname(__file__)
file_path = os.path.join(dirname, '../data/aigues_dataset/daily_dataset_economic_activity.csv')
#file_path = '../data/aigues_dataset/daily_dataset_economic_activity.csv'
parsed_data = parse_water_activity_data(file_path)
print(parsed_data[:5])  
