# Archivos `python` importantes
## scrapper.py
Este código utiliza `selenium` para automatizar un navegador web, buscar etiquetas específicas, recolectar encabezados de una tabla en esa página y obtener los datos de las celdas. También crea una tabla en Pandas a partir de una lista vacía y cierra el navegador al final del código.
## separador.py
Este código implementa una función que lee los archivos CoC y luego separa la información en dos dataframes, uno para estructuras que requieren oro y otro para estructuras que requieren elixir. Luego, la función procesa esta información para obtener el nivel máximo y mínimo de cada estructura, así como la cantidad de cada una en el pueblo. Finalmente, la función guarda estos dataframes en dos archivos de salida separados.
## hill-climbing.py
Este código implementa un algoritmo de Hill Climbing para encontrar una solución óptima a un problema dado. El algoritmo comienza con una solución inicial y luego genera vecinos de esa solución utilizando la función operadormovimiento. Luego, evalúa cada vecino utilizando la función evaluate_solution y si encuentra un vecino que es mejor que la solución actual, actualiza la solución y continúa iterando. Si no encuentra un vecino mejor, el algoritmo finaliza y devuelve la solución y un registro del "makespan", que se refiere al tiempo total que se tarda en encontrar una solución óptima.

# Carpetas
## Available
La carpeta Available cuenta con archivos csv que indican la disponibilidad de las estructuras según los niveles del ayuntamiento.
## Resources
Esta carpeta contiene información de cada una de las estructuras disponibles, indicando sus costes por nivel, tiempo de construcción y el ayuntamiento requerido para desbloquear la mejora.
## Resultados
Esta carpeta contiene las imagenes para los resultados de Mejor Mejora y Primer Mejora
## Test
Esta carpeta contiene la información adecuada para que Hill Climbing trabaje correctamente los datos, corresponde a una fusión entre la disponibilidad de las edificaciones y sus recursos específicos.
## Townhall
Esta carpeta contiene todas las edificaciones disponibles según un ayuntamiento.
