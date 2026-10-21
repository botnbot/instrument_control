from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django import forms


class RFIDLoginForm(forms.Form):
    rfid_card = forms.CharField(
        label="Приложите карту",
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Ожидание карты...'})
    )


def rfid_login_view(request):
    if request.method == 'POST':
        form = RFIDLoginForm(request.POST)
        if form.is_valid():
            rfid = form.cleaned_data['rfid_card']
            # Аутентификация через наш бэкенд
            user = authenticate(request, rfid_card=rfid)
            if user is not None:
                login(request, user)
                return redirect('instrument_list')  # или на главную страницу
            else:
                form.add_error('rfid_card', 'Карта не найдена или пользователь неактивен.')
    else:
        form = RFIDLoginForm()

    return render(request, 'user/rfid_login.html', {'form': form})
