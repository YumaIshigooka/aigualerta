import csv
from datetime import datetime

def parse_water_consumption_data(file_path):
    """
    Parses a CSV file containing water consumption data and returns structured data.

    :param file_path: Path to the CSV file
    :return: List of dictionaries with parsed water consumption data
    """
    water_data = []

    # Open the CSV file and parse its content
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        
        # Loop through each row in the CSV
        for row in csv_reader:
            try:
                # Parse the date field
                date = datetime.strptime(row['Data/Fecha/Date'], '%Y-%m-%d')  # Adjust format if necessary
                
                # Parse water-related data
                census_section = row['Secció censal/Sección censal/Census section'].strip()
                district = row['Districte/Distrito/District'].strip()
                municipality = row['Municipi/Municipio/Municipality'].strip()
                use = row['Ús/Uso/Use'].strip()
                number_of_meters = int(row['Nombre de comptadors/Número de contadores/Number of meters'])
                accumulated_consumption = float(row['Consum acumulat (L/dia)/Consumo acumulado (L/día)/Accumulated consumption (L/day)'])

                # Append parsed data as a dictionary
                water_data.append({
                    'date': date,
                    'census_section': census_section,
                    'district': district,
                    'municipality': municipality,
                    'use': use,
                    'number_of_meters': number_of_meters,
                    'accumulated_consumption': accumulated_consumption
                })
            except ValueError as e:
                print(f"Skipping row due to parsing error: {e}")
    
    return water_data


# Example usage:
file_path = '/Users/ar-suleyman.hasanov/Documents/github/aigualerta/data/aigues_dataset/daily_dataset.csv'
parsed_data = parse_water_consumption_data(file_path)
print(parsed_data[:5])  