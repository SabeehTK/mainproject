from django.shortcuts import render,redirect
from django.views import View
from listing.forms import AddPropertyForm
from listing.models import Property,Wishlist
from accounts.models import Profile
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.
class IndexView(View):
    def get(self, request):
        p=Property.objects.all()
        context = {'property_list': p}
        return render(request, 'index.html',context)

class PropertyListView(View):
    def get(self, request):
        p=Property.objects.all()
        context = {'property_list': p}
        return render(request, 'propertylist.html',context)

class PropertyDetailView(View):
    def get(self, request,pk):
        p=Property.objects.get(id=pk)
        in_wishlist = False
        if request.user.is_authenticated:
            in_wishlist = Wishlist.objects.filter(user=request.user, property=p).exists()
        context = {'property': p,'in_wishlist': in_wishlist}
        return render(request, 'propertydetail.html',context)

class PropertyForSaleView(View):
    def get(self, request):
        ps=Property.objects.all()
        context = {'property': ps}
        return render(request, 'propertyforsale.html',context)

class PropertyForRentView(View):
    def get(self, request):
        ps = Property.objects.all()
        context = {'property': ps}
        return render(request, 'propertyforrent.html',context)

class HouseForSaleView(View):
    def get(self, request):
        ps = Property.objects.all()
        context = {'property': ps}
        return render(request, 'houseforsale.html',context)

class FlatForSaleView(View):
    def get(self, request):
        ps = Property.objects.all()
        context = {'property': ps}
        return render(request, 'flatforsale.html',context)

class PlotForSaleView(View):
    def get(self, request):
        ps = Property.objects.all()
        context = {'property': ps}
        return render(request, 'plotforsale.html',context)

class HouseForRentView(View):
    def get(self, request):
        ps = Property.objects.all()
        context = {'property': ps}
        return render(request, 'houseforrent.html',context)

class FlatForRentView(View):
    def get(self, request):
        ps = Property.objects.all()
        context = {'property': ps}
        return render(request, 'flatforrent.html',context)

class PlotForRentView(View):
    def get(self, request):
        ps = Property.objects.all()
        context = {'property': ps}
        return render(request, 'plotforrent.html',context)

class AgentView(View):
    def get(self, request):
        a = Profile.objects.all()
        context = {'profile': a}
        return render(request, 'agent.html',context)

class AddPropertyView(View):
    def get(self, request):
        form_instance = AddPropertyForm()
        context = {'form': form_instance}
        return render(request,'addproperty.html',context)
    def post(self, request):
        form_instance = AddPropertyForm(request.POST,request.FILES)
        if form_instance.is_valid():
            data=form_instance.cleaned_data
            print(data)
            form_instance.save()
            return redirect('listing:addproperty')

class EditPropertyView(View):
    def get(self, request,i):
        p=Property.objects.get(id=i)
        form_instance = AddPropertyForm(instance=p)
        context = {'form': form_instance}
        return render(request,'editproperty.html',context)
    def post(self, request,i):
        p=Property.objects.get(id=i)
        form_instance = AddPropertyForm(request.POST,instance=p)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('index')

class DeletePropertyView(View):
    def get(self, request,i):
        p=Property.objects.get(id=i)
        p.delete()
        return redirect('index')

class SearchView(View):
    def get(self, request):
        query = request.GET['q']  # Reads the keyword
        print(query)
        # ORM query to filter records from the table
        b = Property.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(price__icontains=query) | Q(
            location__icontains=query) | Q(property_type__icontains=query) | Q(requirement__icontains=query))  # __icontains-lookups
        print(b)
        context = {'p': b,'query': query}
        return render(request, 'search.html',context)


@method_decorator(login_required, name='dispatch')
class AddWishlistView(View):
    def get(self, request,i):
        p=Property.objects.get(id=i)
        u=request.user
        c = Wishlist.objects.create(user=u,property=p)
        c.save()
        return redirect('listing:wishlist')

class WishlistView(View):
    def get(self, request):
        u=request.user
        c=Wishlist.objects.filter(user=u)
        print(c)
        context = {'wish':c}
        return render(request, 'wishlist.html',context)

class RemoveWishlist(View):
    def get(self, request,i):
        p=Property.objects.get(id=i)
        w=Wishlist.objects.filter(user=request.user, property=p)
        w.delete()
        return redirect('listing:wishlist')

class MyPropertyView(View):
    def get(self, request):
        props = Property.objects.filter(owner=request.user)
        context = {'property': props}
        return render(request, 'myproperty.html',context)