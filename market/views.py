from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User

from .forms import ItemForm
from .models import Item

def main(request):
    items = Item.objects.all()  # order by latest
    return render(request, 'market/index.html', {'items': items})  # render to HTML


def render_404(request):
    return render(request, "market/404.html", {})


def item_edit(request, pk):
    # from https://stackoverflow.com/questions/1854237/django-edit-form-based-on-add-form
    if pk:
        item = get_object_or_404(Item, pk=pk)
        # if item.user != request.user:
        #     return HttpResponseForbidden()
    else:
        item = Item(user=request.user)

    form = ItemForm(request.POST or None, instance=item)
    if request.POST and form.is_valid():
        form.save()

        # Save was successful, so redirect to another page
        return redirect('market:item_detail', pk=item.pk)

    return render(request, "market/edit.html", {'form': form, 'item': item})



def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, "market/detail.html", {"item": item})


def item_new(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_date = timezone.now()
            try:
                item.user = User.objects.get(username='bedrockdev')
            except :
                item.user = User.objects.get(username='joey914')
                item.save()
                print('POST saved')
                return redirect('market:item_detail', pk=item.pk)
        else:
            print('Warning: not valid form')
    else:
        form = ItemForm()
        return render(request, "market/new.html", {'form': form})
