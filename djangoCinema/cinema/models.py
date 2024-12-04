from django.db import models

class User(models.Model):
    userID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    yearOfBirth = models.DateField()
    phoneNumber = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return f"{self.name} {self.lastName}"

class Director(models.Model):
    directorID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    yearOfBirth = models.DateField()
    yearOfDeath = models.DateField(null=True, blank=True)
    mostPopularFilm = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.lastName}"

class Hall(models.Model):
    hallID = models.AutoField(primary_key=True)
    numberOfSeats = models.IntegerField()
    is3D = models.BooleanField(default=False)

    def __str__(self):
        return f"Number of seats: {self.numberOfSeats}"

class Price(models.Model):
    priceID = models.AutoField(primary_key=True)
    basePrice = models.DecimalField(max_digits=5, decimal_places=2)
    VIPPrice = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Base: {self.basePrice}, VIP: {self.VIPPrice}"

class Genre(models.Model):
    genreID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Film(models.Model):
    filmID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    year = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    minAge = models.IntegerField(default=3)
    description = models.CharField(max_length=1000, null=True, blank=True)
    directorID = models.ForeignKey(Director, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre, through='FilmGenre')

    def __str__(self):
        return self.name

class FilmGenre(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('film', 'genre')

class Seat(models.Model):
    seatID = models.AutoField(primary_key=True)
    rowNumber = models.IntegerField()
    numberOfSeat = models.IntegerField()
    isVIP = models.BooleanField(default=False)
    hallID = models.ForeignKey(Hall, on_delete=models.CASCADE)

    def __str__(self):
        return f"Row {self.rowNumber}, Seat {self.numberOfSeat}"

class Session(models.Model):
    sessionID = models.AutoField(primary_key=True)
    dateAndTime = models.DateTimeField()
    hallID = models.ForeignKey(Hall, on_delete=models.CASCADE)
    filmID = models.ForeignKey(Film, on_delete=models.CASCADE)
    duration = models.TimeField()

    def __str__(self):
        return f"{self.filmID.name} at {self.dateAndTime}"

class Ticket(models.Model):
    ticketID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    seatID = models.ForeignKey(Seat, on_delete=models.CASCADE)
    sessionID = models.ForeignKey(Session, on_delete=models.CASCADE)
    priceID = models.ForeignKey(Price, on_delete=models.CASCADE)

    def __str__(self):
        return f"Ticket for {self.userID.name} {self.userID.lastName}"
