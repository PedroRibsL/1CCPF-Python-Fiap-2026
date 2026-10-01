from aluno import Aluno
from disciplina import Disciplina

# criar / instanciar 1 aluno
aluno1 = Aluno("João", "123456", "Ciência da computação")

# criar / instanciar 2 disciplinas
sers = Disciplina("Soluções Renováveis", "André")
dsa = Disciplina("Data Structures", "Erick")

# MATRICULAR o aluno nas disciplinas
aluno1.matricular(sers)
aluno1.matricular(dsa)
# print(aluno1.disciplinas[1].nome)

# ATRIBUI a(s) nota(s) de cada disciplina ao aluno
aluno1.adcionar_nota(sers, 10)
aluno1.adcionar_nota(sers, 8)
aluno1.adcionar_nota(dsa, 5)
aluno1.adcionar_nota(dsa, 7)
# print(aluno1.notas_por_disciplina)

print(aluno1.calcular_media_d(dsa))
