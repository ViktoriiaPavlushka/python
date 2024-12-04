from django import forms
from .models import User, Director, Hall, Price, Genre, Film, Seat, Session, Ticket

class DirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = '__all__'

class HallForm(forms.ModelForm):
    class Meta:
        model = Hall
        fields = '__all__'

class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = 'name', 'directorID', 'year', 'description', 'country', 'minAge'

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'

class SeatForm(forms.ModelForm):
    class Meta:
        model = Seat
        fields = '__all__'

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = '__all__'

class PriceForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = '__all__'


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['userID','sessionID', 'priceID', 'seatID']
        widgets = {
            'UserID': forms.Select,
            'sessionID': forms.Select,
            'priceID': forms.Select,
            'seatID': forms.Select,
        }

class Login(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phoneNumber', 'password']
        widgets = {
            'phoneNumber': forms.TextInput(),
            'password': forms.PasswordInput(),
        }
class Registration(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(),
            'lastName': forms.TextInput(),
            'yearOfBirth': forms.TextInput(),
            'phoneNumber': forms.TextInput(),
            'password': forms.TextInput(),

        }