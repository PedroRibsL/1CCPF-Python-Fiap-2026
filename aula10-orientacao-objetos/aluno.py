from email.policy import default
from disciplina import Disciplina

class Aluno:
    def __init__(self, nome, rm, curso):
        self.nome = nome
        self.rm = rm
        self.curso = curso
        self.disciplinas = []           # [Disciplina, Disciplina, ...]
        self.notas_por_disciplina = {}  # ("nome da disciplina": [nota, nota, ...]

    def matricular(self, disciplina: Disciplina):
        self.disciplinas.append(disciplina)
        self.notas_por_disciplina.setdefault(disciplina.nome, [])

    def adcionar_nota(self, disciplina: Disciplina, nota: float):
        self.notas_por_disciplina[disciplina.nome].append(nota)

    def calcular_media_d(self, d: Disciplina)-> float:
        notas = self.notas_por_disciplina.get(d.nome, [])
        if not notas:
            return 0
        return  sum(notas) / len(notas)

    def calcular_media_g(self) -> float:
        medias = []
        for d in self.disciplinas:
            media_d = self.calcular_media_d(d)
            medias.append(media_d)
        return sum(medias) / len(medias)


    # EXIBIR BOLETIM COM NOME, RM, DISCIPLINAS, CALCULAR MEDIA GERAL
    # 2 DESAFIO TRANSFORMAR O MINI CRM EM ORIENTAÇÃO AO OBJETO

