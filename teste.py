class Teste:
    def __init__(self, response):
        self.__response = response
        self.a = "ola"

    def execute(self):
        self.__response.execute(self)

    def show(self):
        print("A: " + self.a)


class Response:
    def __init__(self, b):
        self.b = b

    def execute(teste):
        teste.a = "adeus"


response = Response("x")
teste = Teste(response)
teste.execute()
teste.show()