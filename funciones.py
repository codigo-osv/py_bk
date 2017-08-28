import os
import datetime


def older_than_list(path: str, days: int) -> list:
    """
    Retorna list[str] de los paths a los archivos mas viejos
    que los dias representados por days
    
    path:str: path al directorio que contiene los archivos
    days:int: cantidad de dias de antigüedad a buscar
    """
    result = []
    file_list = os.listdir(path)
    time_range = datetime.datetime.now() - datetime.timedelta(days=days)
    for file in file_list:
        path_to_file = path + file
        file_time = datetime.datetime.fromtimestamp(os.stat(path_to_file).st_mtime)
        if file_time < time_range:
            result.append(path_to_file)
    return result


#print(older_than(PATH, 300))