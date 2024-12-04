class User:
    def __init__(self, firstName, lastName, yearOfBirth):
        self.__firstName = firstName
        self.__lastName = lastName
        self.yearOfBirth = yearOfBirth
        self.isLoggedIn = False

    def getFirstName(self):
        return self.__firstName

    def getLastName(self):
        return self.__lastName


class Film:
    def __init__(self, title, director, genre, releaseDate, is3d):
        self.title = title
        self.director = director
        self.genre = genre
        self.releaseDate = releaseDate
        self.is3d = is3d

    def showInformation(self):
        print(f"Назва: {self.title}")
        print(f"Жанр: {self.genre}")
        print(f"Режисер: {self.director}")
        print(f"3D: {self.is3d}")
        print(f"Дата виходу: {self.releaseDate}")


class Seat:
    def __init__(self, seatNumber):
        self.seatNumber = seatNumber - 1
        self.isAvailable = True
        self.price = 100

    def calculatePrice(self, is3D=False, points=0):
        price = self.price
        if is3D:
            price += 30
        if points >= 100:
            price = 0
            points -= 100
            print("Використано 100 балів лояльності для отримання безкоштовного квитка.")
        return price

    def reserve(self, seats):
        if self.isAvailable:
            self.isAvailable = False
            seats[self.seatNumber // 6][self.seatNumber % 6] = "*"
        else:
            print("Це місце заброньоване. Виберіть інше.")


class BasicSeat(Seat):
    def __init__(self, seatNumber):
        super().__init__(seatNumber)
        self.price = 100


class VIPSeat(Seat):
    def __init__(self, seatNumber):
        super().__init__(seatNumber)
        self.price = 150

    def calculatePrice(self, is3D=False):
        price = self.price
        if is3D:
            price += 50
        return price


class LoyaltyProgram:
    def __init__(self, points=0):
        self.points = points

    def addPoints(self, points):
        self.points += points

    def showPoints(self):
        print(f"У вас {self.points} балів лояльності.")


class LoyaltyUser(User, LoyaltyProgram):
    def __init__(self, firstName, lastName, yearOfBirth, points=0):
        User.__init__(self, firstName, lastName, yearOfBirth)
        LoyaltyProgram.__init__(self, points)

    def showLoyaltyInfo(self):
        print(f"Користувач: {self.getFirstName()} {self.getLastName()}")
        self.showPoints()


class Sorting:
    @staticmethod
    def printFilms(films, condition, label):
        found = False
        print(f"\n{label}:")
        for film in films:
            if condition(film):
                print(f"  - Назва: {film.title}, Режисер: {film.director}, Жанр: {film.genre}, "
                      f"Дата виходу: {film.releaseDate}, 3D: {'Так' if film.is3d else 'Ні'}")
                found = True
        if not found:
            print("  Фільм не знайдено.")

    @staticmethod
    def sortByTitle(films, inputTitle):
        def condition(film):
            return film.title.lower() == inputTitle.lower()

        Sorting.printFilms(films, condition, f"Фільми з назвою '{inputTitle}'")

    @staticmethod
    def sortByDirector(films, inputDirector):
        def condition(film):
            return film.director.lower() == inputDirector.lower()

        Sorting.printFilms(films, condition, f"Фільми режисера '{inputDirector}'")

    @staticmethod
    def sortByGenre(films, inputGenre):
        def condition(film):
            return film.genre.lower() == inputGenre.lower()

        Sorting.printFilms(films, condition, f"Фільми жанру '{inputGenre}'")

    @staticmethod
    def sortByReleaseDate(films, inputReleaseDate):
        def condition(film):
            return film.releaseDate == inputReleaseDate

        Sorting.printFilms(films, condition, f"Фільми з датою виходу '{inputReleaseDate}'")

    @staticmethod
    def sortByIs3D(films, inputIs3d):
        def condition(film):
            return film.is3d == inputIs3d

        status = "фільми з 3D" if inputIs3d else "фільми без 3D"
        Sorting.printFilms(films, condition, status)


class Ticket:
    @staticmethod
    def showTicket(user, title, seat, films):
        user.addPoints(10)
        film = next((f for f in films if f.title == title), None)
        if film:
            print("\nВаш квиток:")
            print("=" * 30)
            print(f"Користувач: {user.getFirstName()} {user.getLastName()}")
            print(f"Фільм: {film.title}")
            print(f"Режисер: {film.director}")
            print(f"Жанр: {film.genre}")
            print(f"Дата виходу: {film.releaseDate}")
            print(f"Тип місця: {'VIP' if isinstance(seat, VIPSeat) else 'Звичайне'}")
            print(f"Номер місця: {seat.seatNumber + 1}")
            price = seat.calculatePrice(film.is3d)
            print(f"Ціна: {price} грн")
            print("Вам додалося 10 балів :)")
            print("=" * 30)
        else:
            print("Фільм не знайдено.")


def main():
    seats = [["."] * 6 for i in range(5)]
    #нумерація сидінь
    numberOfSeat = 1
    for i in range(5):
        for j in range(6):
            seats[i][j] = numberOfSeat
            numberOfSeat += 1

    films = [
        Film("Титанік", "Джеймс Кемерон", "Драма", "1997-12-19", False),
        Film("Аватар", "Джеймс Кемерон", "Наукові", "2009-12-18", False),
        Film("Зоряні війни: Нова надія", "Джордж Лукас", "Фантастика", "1977-05-25", False),
        Film("Володар перснів: Спів братства", "Пітер Джексон", "Фентезі", "2001-12-19", False),
        Film("Месники: Кінцева гра", "Ентоні Руссо, Джо Руссо", "Екшн", "2019-04-26", True),
        Film("Джуманджі: Поклик джунглів", "Джейк Касдан", "Пригодницький", "2017-12-20", True),
        Film("Шерлок Холмс", "Гай Річі", "Детектив", "2009-12-25", False),
        Film("Планета мавп", "Руперт Уайятт", "Наукові", "2011-08-05", True),
    ]

    print("Вас вітає ПолітехCinema :)")

    print("Введіть ваше імʼя:")
    firstName = input()
    print("Введіть ваше прізвище:")
    lastName = input()
    print("Введіть ваш рік народження:")
    yearOfBirth = int(input())
    user = LoyaltyUser(firstName, lastName, yearOfBirth)

    while True:
        print("\nГоловне меню:")
        print("1. Пошук фільмів")
        print("2. Перегляд балів лояльності")
        print("3. Вихід")

        choice = input("Введіть номер дії: ")

        if choice == "1":
            while True:
                print("\nМеню пошуку:")
                print("1. За назвою")
                print("2. За режисером")
                print("3. За жанром")
                print("4. За датою виходу")
                print("5. За наявністю 3D")
                print("6. Надрукувати всі фільми")
                print("7. Повернутися до головного меню")

                search_choice = input("Введіть номер дії: ")

                if search_choice == "1":
                    title = input("Введіть назву фільму: ")
                    Sorting.sortByTitle(films, title)
                    print("Якщо вибрали фільм напишіть yes, інакше no")
                    decision = input()
                    if decision == "yes":
                        break
                elif search_choice == "2":
                    director = input("Введіть ім'я режисера: ")
                    Sorting.sortByDirector(films, director)
                    print("Якщо вибрали фільм напишіть yes, інакше no")
                    decision = input()
                    if decision == "yes":
                        break
                elif search_choice == "3":
                    genre = input("Введіть жанр: ")
                    Sorting.sortByGenre(films, genre)
                    print("Якщо вибрали фільм напишіть yes, інакше no")
                    decision = input()
                    if decision == "yes":
                        break
                elif search_choice == "4":
                    release_date = input("Введіть дату виходу (YYYY-MM-DD): ")
                    Sorting.sortByReleaseDate(films, release_date)
                    print("Якщо вибрали фільм напишіть yes, інакше no")
                    decision = input()
                    if decision == "yes":
                        break
                elif search_choice == "5":
                    is3d_input = input("Шукаєте фільми з 3D? (yes/no): ").lower()
                    is3d = is3d_input == "yes"
                    Sorting.sortByIs3D(films, is3d)
                    print("Якщо вибрали фільм напишіть yes, інакше no")
                    decision = input()
                    if decision == "yes":
                        break
                elif search_choice == "6":
                    for film in films:
                        print(f"  - Назва: {film.title}, Режисер: {film.director}, Жанр: {film.genre}, "
                              f"Дата виходу: {film.releaseDate}, 3D: {'Так' if film.is3d else 'Ні'}")
                    print("Якщо вибрали фільм напишіть yes, інакше no")
                    decision = input()
                    if decision == "yes":
                        break
                elif search_choice == "7":
                    break
                else:
                    print("Невірний вибір. Спробуйте ще раз.")

            print("Якщо бажаєте вийти напишіть yes, інакше no")
            decision = input()
            if decision == "yes":
                break

            print("Введіть назву фільму, який ви вибрали: ")
            title = input()
            print("Вільні місця (заброньовані позначені через *): ")
            for i in range(5):
                for j in range(6):
                    print(seats[i][j], end=" ")
                print()
            print("Введіть номер місця:")
            number = int(input())
            print("Чи бажаєте замовити VIP місце? Введіть yes або no")
            decision = input()
            isVIP = False
            if decision == "yes":
                isVIP = True
                seat = VIPSeat(number)
            else:
                seat = BasicSeat(number)
            seat.reserve(seats)
            Ticket.showTicket(user, title, seat, films)

        elif choice == "2":
            user.showLoyaltyInfo()
            input("Натисніть Enter, щоб повернутися до головного меню.")

        elif choice == "3":
            print("Дякуємо за використання ПолітехCinema! На все добре!")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main()

