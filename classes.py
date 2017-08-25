import os
import datetime
from typing import List, Tuple


class TimedDirectory:
    """
    Representa un directorio con información temporal
    de los archivos que contiene
    """
    def __init__(self, path: str):
        """
        Toma el path al directorio a representar
        :param path: str: String representando el path al directorio
        """
        # Asegurar que el path termina con '/'
        if not path.endswith('/'):
            path += '/'
        self.path = path
        self._current_time = datetime.datetime.now()

    def _timed_list(self) -> List[Tuple[str, datetime.datetime]]:
        """
        Retorna una lista de tuplas de dos elementos:
        Elemento[0]: string representando el path completo al archivo,
        incluyendo su nombre. Ej: '/home/xxx/nombre.txt'.
        Elemento[1]: objeto datetime.datetime representando la más
        reciente modificación al archivo (os.stat(archivo).st_mtime)
        La lista se encuentra ordenada de archivo mas antiguo a mas reciente.
        """
        files_paths_list = [self.path + file for file in os.listdir(self.path)]
        paths_with_time_list = [
            (file, datetime.datetime.fromtimestamp(os.stat(file).st_mtime))
            for file in files_paths_list
        ]
        return sorted(paths_with_time_list, key=lambda x: x[1])

    def oldest_files_list(self, older_than: int) -> List[str]:
        """
        Devuelve una lista de strings representando los path + nombre
        de los archivos mas antiguos que el rango de dias expresado por
        older_than.
        :param older_than: int: representa la cantidad dias de antigüedad
        a comprobar.
        """
        time_range = self._current_time - datetime.timedelta(days=older_than)
        return [
            file[0] for file in self._timed_list()
            if file[1] < time_range
        ]

    def newest_file_older_than(self, older_than: int) -> bool:
        """
        Devuelve True si el archivo más nuevo del directorio
        es más antiguo que la cantidad de días ingresados.
        Hace la comparación sobre el último elemento de _timed_list()
        ya que la lista que devuelve esa función está ordenada de mas
        antiguo a mas reciente.
        En caso de que _timed_list() devuelva una lista vacía, se devuelve True,
        indicando que el directorio esta vacío.
        :param older_than: int: cantidad de dias de antigüedad
        a calcular.
        """
        time_range = self._current_time - datetime.timedelta(days=older_than)
        try:
            result = self._timed_list()[-1][1] < time_range
        except IndexError:
            result = True
        return result

#print(TimedDirectory('').newest_file_older_than(1))
#print(TimedDirectory('/home/ivan/cosas').path)
