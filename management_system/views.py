from django.shortcuts import render, redirect


def admin_site(request):
    return redirect("/admin/")


def error_404(request):
    return render(request, '404.html')
