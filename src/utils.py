"""
This module defines constants used throughout the application.
"""
from enum import Enum

class col_names(Enum):
    policy = 'Pòlissa/Póliza/Policy'
    technology = 'Tecnologia/Tecnología/Technology'
    diameter = 'Diàmetre comptador (cm)/Diámetro contador (cm)/Counter diameter (cm)'
    usage = 'Ús/Uso/Use'
    housing = "Tipus d'habitatge/Tipo de vivienda/Type of housing"
    date = 'Data/Fecha/Date'
    consumption = 'Índex de lectura (L/h)/Índice de lectura (L/h)/Reading index (L/h)'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value