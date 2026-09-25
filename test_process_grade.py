import pytest

# Si tu archivo se llama process_grades.py cambia esta línea
from process_grades import process_grades


# =====================================================================
# ACTIVIDAD 1 - COBERTURA DE SENTENCIAS
# Un solo caso que pasa por TODAS las sentencias del ciclo
# =====================================================================

def test_CS01_todas_las_sentencias(capsys):
    students = [
        {'name': 'Pedro', 'grades': None},          # sentencia print + continue
        {'name': 'Ana',   'grades': [80, 90, 85]},  # passed.append   (prom 85)
        {'name': 'Luis',  'grades': [60, 60, 60]},  # print recovery  (prom 60)
        {'name': 'Marta', 'grades': [40, 45, 50]},  # failed.append   (prom 45)
    ]
    result = process_grades(students)
    salida = capsys.readouterr().out

    assert "Student Pedro has no grades" in salida
    assert "Luis is in recovery" in salida
    assert result['passed'] == ['Ana']
    assert result['failed'] == ['Marta']
    # RF5: (85 + 60 + 45) / 3 = 63.33
    assert result['overall_average'] == 63.33


# =====================================================================
# ACTIVIDAD 2 - COBERTURA DE DECISIONES
# D1: for (entra / no entra)       D2: grades == None (V/F)
# D3: average > 70 (V/F)           D4: average >= 50 (V/F)
# D5: counter > 0 (V/F)
# =====================================================================

def test_CD01_lista_vacia():
    # D1 = F (no entra al ciclo), D5 = F
    result = process_grades([])
    assert result == {'passed': [], 'failed': [], 'overall_average': 0}


def test_CD02_grades_none(capsys):
    # D1 = V, D2 = V, D5 = F
    result = process_grades([{'name': 'Pedro', 'grades': None}])
    assert "Student Pedro has no grades" in capsys.readouterr().out
    assert result == {'passed': [], 'failed': [], 'overall_average': 0}


def test_CD03_aprobado():
    # D2 = F, D3 = V, D5 = V
    result = process_grades([{'name': 'Ana', 'grades': [90, 90, 90]}])
    assert result['passed'] == ['Ana']
    assert result['failed'] == []
    assert result['overall_average'] == 90      # RF5


def test_CD04_recuperacion(capsys):
    # D3 = F, D4 = V, D5 = V
    result = process_grades([{'name': 'Luis', 'grades': [60, 60, 60]}])
    assert "Luis is in recovery" in capsys.readouterr().out
    assert result['passed'] == [] and result['failed'] == []
    assert result['overall_average'] == 60      # RF5


def test_CD05_reprobado():
    # D3 = F, D4 = F, D5 = V
    result = process_grades([{'name': 'Marta', 'grades': [40, 40, 40]}])
    assert result['failed'] == ['Marta']
    assert result['passed'] == []
    assert result['overall_average'] == 40      # RF5


# =====================================================================
# ACTIVIDAD 3 - COBERTURA DE CAMINOS (+ valores límite)
# =====================================================================

def test_CC01_camino_sin_estudiantes():
    # P1: inicio -> for(F) -> counter>0(F) -> return
    assert process_grades([]) == {'passed': [], 'failed': [], 'overall_average': 0}


def test_CC02_camino_none():
    # P2: for(V) -> None(V) -> continue -> for(F) -> counter>0(F) -> return
    assert process_grades([{'name': 'P', 'grades': None}])['overall_average'] == 0


def test_CC03_camino_aprobado():
    # P3: None(F) -> >70(V) -> counter>0(V)
    r = process_grades([{'name': 'A', 'grades': [100, 80]}])
    assert r == {'passed': ['A'], 'failed': [], 'overall_average': 90}


def test_CC04_camino_recuperacion():
    # P4: None(F) -> >70(F) -> >=50(V) -> counter>0(V)
    r = process_grades([{'name': 'L', 'grades': [55, 65]}])
    assert r == {'passed': [], 'failed': [], 'overall_average': 60}


def test_CC05_camino_reprobado():
    # P5: None(F) -> >70(F) -> >=50(F) -> counter>0(V)
    r = process_grades([{'name': 'M', 'grades': [20, 30]}])
    assert r == {'passed': [], 'failed': ['M'], 'overall_average': 25}


def test_CC06_limite_promedio_70():
    # Límite: RF3 dice >= 70 -> aprobado
    r = process_grades([{'name': 'Luis', 'grades': [70, 70, 70]}])
    assert r['passed'] == ['Luis']


def test_CC07_limite_promedio_50(capsys):
    # Límite: 50 -> recuperación
    process_grades([{'name': 'Eva', 'grades': [50, 50]}])
    assert "Eva is in recovery" in capsys.readouterr().out


def test_CC08_limite_promedio_49_99():
    # Límite: justo debajo de 50 -> reprobado
    r = process_grades([{'name': 'Leo', 'grades': [49.99]}])
    assert r['failed'] == ['Leo']


def test_CC09_lista_de_notas_vacia(capsys):
    # Caso excepcional: RF4 -> mensaje y omitir, NO debe tronar
    r = process_grades([{'name': 'Jorge', 'grades': []}])
    assert "Student Jorge has no grades" in capsys.readouterr().out
    assert r == {'passed': [], 'failed': [], 'overall_average': 0}


def test_CC10_datos_del_main():
    # Los datos originales del programa
    students = [
        {'name': 'Ana', 'grades': [80, 90, 85]},
        {'name': 'Luis', 'grades': [70, 70, 70]},
        {'name': 'Jorge', 'grades': []},
        {'name': 'Marta', 'grades': [40, 45, 50]},
    ]
    r = process_grades(students)
    # (85 + 70 + 45) / 3 = 66.67
    assert r == {'passed': ['Ana', 'Luis'], 'failed': ['Marta'],
                 'overall_average': 66.67}