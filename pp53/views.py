from django.shortcuts import render


def index(request):
    return render(request, 'pp53/index.html')


# --- Exercici 1: Decimal a Binari ---

def decimal_a_binari(num):
    if num == 0:
        return "0"
    residus = []
    while num > 0:
        residus.append(num % 2)
        num //= 2
    return "".join(str(b) for b in reversed(residus))


def exercici1(request):
    numero_str = request.GET.get('numero', '')
    resultat = None
    numero = ''
    if numero_str != '':
        try:
            numero = int(numero_str)
            resultat = decimal_a_binari(numero)
        except ValueError:
            pass
    return render(request, 'pp53/exercici1.html', {'numero': numero, 'resultat': resultat})


# --- Exercici 2: Logs ---

TOTS_ELS_MISSATGES = [
    {'tipus': 'info',    'text': 'Servidor iniciat correctament.'},
    {'tipus': 'info',    'text': 'Consum de CPU ok.'},
    {'tipus': 'warning', 'text': 'Consum de CPU elevat.'},
    {'tipus': 'error',   'text': 'Missatge de correu retornat.'},
    {'tipus': 'info',    'text': 'Consum de CPU ok.'},
]

NIVELL_MINIM = {
    'info': 3,
    'warning': 2,
    'error': 1,
}


def exercici2(request):
    try:
        nivell = int(request.GET.get('nivell', 3))
    except ValueError:
        nivell = 3

    missatges = [m for m in TOTS_ELS_MISSATGES if NIVELL_MINIM[m['tipus']] <= nivell]
    return render(request, 'pp53/exercici2.html', {'nivell': nivell, 'missatges': missatges})


# --- Exercici 3: Array Multidimensional ---

NARUTO = [
    {
        'Arc': 'Examenes Chuunin',
        'Protagonista': 'Naruto Uzumaki',
        'Antagonista': 'Orochimaru',
        'Altres_Personatges': ['Sasuke Uchiha', 'Sakura Haruno', 'Kakashi Hatake', 'Rock Lee'],
    },
    {
        'Arc': 'Invasio de Konoha',
        'Protagonista': 'Naruto Uzumaki',
        'Antagonista': 'Pain',
        'Altres_Personatges': ['Jiraiya', 'Hinata Hyuga', 'Tsunade', 'Itachi Uchiha'],
    },
    {
        'Arc': 'Quarta Guerra Ninja',
        'Protagonista': 'Naruto Uzumaki',
        'Antagonista': 'Obito Uchiha',
        'Altres_Personatges': ['Sasuke Uchiha', 'Kakashi Hatake', 'Sakura Haruno', 'Madara Uchiha'],
    },
]


def exercici3(request):
    return render(request, 'pp53/exercici3.html', {'naruto': NARUTO})
