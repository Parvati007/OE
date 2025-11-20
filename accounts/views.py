from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .forms import UserStyleProfileForm
from .models import UserStyleProfile

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    orders = request.user.orders.all()[:5]
    style_profile = getattr(request.user, 'style_profile', None)
    return render(request, 'accounts/profile.html', {
        'orders': orders,
        'style_profile': style_profile
    })


@login_required
def style_profile(request):
    profile, created = UserStyleProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserStyleProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = UserStyleProfileForm(instance=profile)
    
    return render(request, 'accounts/style_profile.html', {'form': form})


@login_required
@require_http_methods(["GET"])
def get_user_profile(request):
    """JSON endpoint to fetch user's style profile"""
    try:
        profile = request.user.style_profile
        # Return format expected by chatbot.js
        return JsonResponse({
            'profile': {
                'height': profile.height,
                'skin_tone': profile.skin_tone,
                'body_type': profile.body_type,
                'favourite_colors': profile.favourite_colors if isinstance(profile.favourite_colors, list) else [],
                'preferred_clothing_types': profile.preferred_clothing_types if isinstance(profile.preferred_clothing_types, list) else [],
                'gender': profile.gender or '',
            }
        })
    except UserStyleProfile.DoesNotExist:
        return JsonResponse({
            'profile': None
        }, status=200)
    except Exception as e:
        return JsonResponse({
            'profile': None,
            'error': str(e)
        }, status=200)