class Disciplina:
    def __init__(self, nome, professor):
        self.nome = nome
        self.professor = professor

    def exibir_info(self):
        print(f"Disciplina: {self.nome} | Professor: {self.professor}")


# TEMPORARIO
# prompt_ia = Disciplina("Prompt & IA", professor= "Jorge")
# cs = Disciplina("Computer Science", professor= "Maurício")
# cs.exibir_info()