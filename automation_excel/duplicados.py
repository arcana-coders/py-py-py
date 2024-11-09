import openpyxl
import pandas as pd
import xlrd

#CREO QUE NO SIRVE; NO LO SE!! no se necesita.
data = pd.read_excel('duplicados.xlsx')
data.sort_values('SKU', inplace=True)
data.drop_duplicates(subset = 'SKU', keep = False, inplace=True)
data.to_pickle.to_excel('duplicados.xlsx')
print('Ya no debe haber duplicados')

