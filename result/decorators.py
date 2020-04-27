from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Décorateur pour les vues qui vérifient que l'utilisateur connecté est un étudiant,
     redirige vers la page de connexion si nécessaire.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_student or u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def lecturer_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
        Décorateur pour les vues qui vérifient que l'utilisateur connecté est un enseignant,
        redirige vers la page de connexion si nécessaire.   
     '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_lecturer or u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
