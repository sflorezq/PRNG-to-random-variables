import pandas as pd
def load_file(file_name:str) -> list[float]:
    # Cargar el archivo Excel
    df = pd.read_excel(file_name+".xlsx")
    numeros = df[file_name].tolist()
    return numeros

def export(numbers:list[float],name:str) :
    df = pd.DataFrame(numbers,columns=[name])
    df.to_excel(name+".xlsx",index=False)