import pickle
from aigualerta.services.resource_handler import get_absolute_path

EXPECTED_COLUMNS = [
    'DATETIME',
    'CONSUMPTION',
    'POLICY',
    'TECHNOLOGY',
    'DIAMETER',
    'USAGE',
    'HOUSING'
]

short_names = {
    'Pòlissa/Póliza/Policy': 'POLICY',
    'Tecnologia/Tecnología/Technology': 'TECHNOLOGY',
    'Diàmetre comptador (cm)/Diámetro contador (cm)/Counter diameter (cm)': 'DIAMETER',
    'Ús/Uso/Use': 'USAGE',
    "Tipus d'habitatge/Tipo de vivienda/Type of housing": 'HOUSING',
    'Data/Fecha/Date': 'DATETIME',
    'Índex de lectura (L/h)/Índice de lectura (L/h)/Reading index (L/h)': 'CONSUMPTION',
}

KMEANS_THRESHHOLD = 2.5
WINDOW_SIZE = 4

model_path = get_absolute_path('../../data/models/model_test.sav')

model = pickle.load(open(model_path, 'rb'))
