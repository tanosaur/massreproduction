# Adding similar functionality but different data

class Good_Rock:
    response = "Radical."

class Bad_Rock:
    questions = ["Whoa! So, why???"]
    def __init__(self,reason):
        self.reason=reason

class Bebop:
    questions = ["Groovy. I like bebop too. Who's your fav?"]
    # Decision to put interface information within model class
    # Here, it keeps the information localised (future changes can be made in one place)
    def __init__(self, artist):
        self.artist = artist

class Modal:
    questions = ["Whoa! So, like, when you say modal, do you like Kind of Blue?", "And what's your favourite mode?"]
    def __init__(self, like_kind_of_blue, mode):
        self.like_kind_of_blue = like_kind_of_blue
        self.mode = mode

class AvanteGarde:
    response = "Hokay." # Putting data on a class, not an instance of a class

class AskMenu:
    def __init__(self, question, menu):
        self.question = question
        self.menu = menu

    def run(self):
        print self.question

        while True:
            line = raw_input().strip()
            if self.menu.get(line):
                self.menu[line].run()
                break

class AskQuestion:
    def __init__(self, genre):
        self.genre = genre

    def run(self):
        answers = []
        for q in self.genre.questions:
            print q
            response = raw_input().strip()
            answers.append(response)
        print self.genre(*answers)

class Respond:
    def __init__(self, genre):
        self.genre = genre

    def run(self):
        print self.genre.response
        print self.genre() # Returns instance of class

class Quit:
    def run(self):
        print("Goodbye my friend, I hope I was useful")

if __name__ == '__main__':
    MENU = AskMenu("Tell Me About Music You Love\n" \
                   "Hey, what genre do you like?\n" \
                   "\n" \
                   "Press \"1\" for Jazz\n" \
                   "Press \"2\" for Rock!!\n" \
                   "Press \"Q\" to quit, because you're done.", {
        "1": AskMenu("OK, so I hear you like Jazz. But, what kind of Jazz?\n" \
                     "1. Bebop\n" \
                     "2. Modal\n" \
                     "3. Avante-Garde", {
            "1": AskQuestion(Bebop),
            "2": AskQuestion(Modal),
            "3": Respond(AvanteGarde),
        }),
        "2": AskMenu("OK, so I hear you like Rock. But, what kind of Rock?\n" \
                     "1. Good\n" \
                     "2. Nickelback" , {
            "1": Respond(Good_Rock),
            "2": AskQuestion(Bad_Rock)
        }),
        "Q": Quit(),
    })
    MENU.run()
