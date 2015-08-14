class Good_Rock:
    pass

class Bad_Rock:
    def __init__(self,reason):
        self.reason=reason

class Bebop:
    def __init__(self, artist):
        self.artist = artist

class Modal:
    def __init__(self, like_kind_of_blue, mode):
        self.like_kind_of_blue = like_kind_of_blue
        self.mode = mode

class AvanteGarde:
    pass

if __name__ == '__main__':
  print("Tell Me About Music You Love")
  print("Hey, what genre do you like?")

  print("Press \"1\" for Jazz")
  print("Press \"2\" for Rock!!")
  print("Press \"Q\" to quit, because you're done.")

  while True:
    line = input().strip()
    if line == '1':
        print("OK, so I hear you like Jazz. But, what kind of Jazz?")

        print("1. Bebop")
        print("2. Modal")
        print("3. Avante-Garde")

        line = input().strip()
        if line == '1':
            print("Groovy. I like bebop too. Who's your fav?")
            fav_bebop_artist = input().strip()

            genre = Bebop(fav_bebop_artist)
            print(genre)
            break
        elif line == "2":
            print("Whoa! So, like, when you say modal, do you like Kind of Blue?")
            like_kind_of_blue = input().strip()

            print("And what's your favourite mode?")
            fav_mode = input().strip()

            genre = Modal(like_kind_of_blue, fav_mode)
            print(genre)
            break
        elif line == "3":
            print("Hokay.")

            genre = AvanteGarde()
            print(genre)
            break

    elif line=='2':
        print("OK, so I hear you like Rock. But, what kind of Rock?")

        print("1. Good")
        print("2. Nickelback")

        line = input().strip()
        if line == '1':
            print("Radical.")

            genre = Good_Rock()
            print(genre)
            break

        elif line == "2":
            print("Whoa! So, why???")
            reason = input().strip()

            genre = Bad_Rock(reason)
            print(genre)
            break

    elif line == 'Q':
        print("Goodbye my friend, I hope I was useful")
        break
