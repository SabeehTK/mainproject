from django.core.mail import send_mail
from django.shortcuts import render,redirect
from django.views import View
from listing.forms import AddPropertyForm,EnquiryForm,EnquiryAcceptedForm,EnquiryRejectedForm
from listing.models import Property,Wishlist,Enquiry,Payment
from accounts.models import Profile
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
import razorpay
from django.contrib import messages


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
        in_enquiry=False
        in_wishlist = False
        in_rejected=False
        if request.user.is_authenticated:
            in_wishlist = Wishlist.objects.filter(user=request.user, property=p).exists()
            in_enquiry = Enquiry.objects.filter(property=p,buyer=request.user,status__in=['accepted','pending'],buyer_rejected=False).exists()
        context = {'property': p,'in_wishlist': in_wishlist,'in_enquiry':in_enquiry}
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
        form_instance = AddPropertyForm(request.POST,request.FILES,instance=p)
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
        query = request.GET['q']
        print(query)
        b = Property.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(price__icontains=query) | Q(
            location__icontains=query) | Q(property_type__icontains=query) | Q(requirement__icontains=query))
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

class EnquiryView(View):
    def get(self, request,i):
        p=Property.objects.get(id=i)
        form = EnquiryForm()
        context = {'form': form,'property': p}
        return render(request, 'enquiry.html',context)
    def post(self, request,i):
        p=Property.objects.get(id=i)
        form = EnquiryForm(request.POST)
        if form.is_valid():
            e=form.save(commit=False)
            e.property=p
            e.buyer=request.user
            data=form.cleaned_data
            print(data)
            e.save()
            send_mail(
                subject=f"You have received an enquiry on {e.property.title}",
                message=f"Dear {e.property.owner.username},\n\n"
                        f"An enquiry for {e.property.title} has been received.\n"
                        f"the enquiry has been received from {e.buyer}.\n\n"
                        f"Message from buyer: {e.message}",
                from_email=None,  # uses DEFAULT_FROM_EMAIL
                recipient_list=[e.property.owner.email],
                fail_silently=False,
            )
            return redirect('listing:propertydetail',pk=p.id)

#for admin:
def is_admin(user):
    return user.is_superuser
@method_decorator(user_passes_test(is_admin), name='dispatch')
class DeleteEnquiryView(View):
    def get(self, request,i):
        p=Enquiry.objects.get(id=i)
        p.delete()
        return redirect('accounts:admin_dashboard')

#

@method_decorator(login_required, name='dispatch')
class AgentEnquiryView(View):
    def get(self, request):
        e=Enquiry.objects.filter(property__owner=request.user).order_by('status','-date_added')
        context = {'enquiries': e}
        return render(request, 'enquiries.html',context)

class BuyerEnquiryView(View):
    def get(self, request):
        be=Enquiry.objects.filter(buyer=request.user,status__in=['pending','accepted'],buyer_rejected=False)
        context = {'be': be}
        return render(request, 'buyerenquirypage.html',context)

class EnquiryAcceptedView(View):
    def get(self, request,i):
        e=Enquiry.objects.get(id=i)
        form = EnquiryAcceptedForm()
        context = {'form': form,'enquiry':e}
        return render(request, 'enquiryacceptform.html',context)
    def post(self, request,i):
        e=Enquiry.objects.get(id=i)
        form = EnquiryAcceptedForm(request.POST,instance=e)
        if form.is_valid():
            f=form.save(commit=False)
            f.status='accepted'
            f.save()
            send_mail(
                subject="Your enquiry has been accepted",
                message=f"Dear {f.buyer.username},\n\n"
                        f"Your enquiry for {f.property.title} has been accepted.\n"
                        f"Visit scheduled on {f.visiting_date}.\n\n"
                        f"Message from agent: {f.agent_response}",
                from_email=None,  # uses DEFAULT_FROM_EMAIL
                recipient_list=[f.email],
                fail_silently=False,
            )

            return redirect('listing:enquiries')

class EnquiryRejectedView(View):
    def get(self, request,i):
        e=Enquiry.objects.get(id=i)
        form=EnquiryRejectedForm()
        context = {'form': form,'enquiry':e}
        return render(request, 'enquiryrejectform.html',context)
    def post(self, request,i):
        e=Enquiry.objects.get(id=i)
        form = EnquiryRejectedForm(request.POST,instance=e)
        if form.is_valid():
            f=form.save(commit=False)
            f.status='rejected'
            f.save()
            send_mail(
                subject="Your enquiry has been rejected",
                message=f"Dear {f.buyer.username},\n\n"
                        f"Your enquiry for {f.property.title} has been declined.\n"
                        f"Message from agent: {f.agent_response}",
                from_email=None,
                recipient_list=[f.email],
                fail_silently=False,
            )
            return redirect('listing:enquiries')

class BuyerVisitedView(View):
    def get(self, request,i):
        e=Enquiry.objects.get(id=i)
        e.buyer_visited=True
        e.save()
        return redirect('listing:enquiries')

class AdvancePaymentView(View):
    def get(self, request,i):
        try:
            e=Enquiry.objects.get(id=i)
            a=e.property.price
            amount=0.1*a
            if amount>500000:
                amount=499999
            client = razorpay.Client(auth=('rzp_test_Rn853YhSiRl2l7', 'UpKFAcdCLWN1ph277XjeDNcH'))
            order=client.order.create({'amount':amount*100,'currency':'INR'})
            print(order)
            p=Payment.objects.create(enquiry=e,razorpay_order_id=order['id'],amount=amount,status='Created')
            print(p)
            context = {'payment':order}
            return render(request,'payment.html',context)
        except:
            print('amount is high')
            messages.error(request,'Advance payment exceeds the maximum allowed limit')
            return redirect('listing:buyerenquiries')


class PaymentSuccessView(View):
    # def get(self, request):
    #     return render(request, 'paymentsuccess.html')
    def post(self, request):
        client = razorpay.Client(auth=('rzp_test_Rn853YhSiRl2l7', 'UpKFAcdCLWN1ph277XjeDNcH'))
        print(request.user.username)
        print(request.POST)
        data=request.POST
        data_dict={'razorpay_order_id': data.get('razorpay_order_id'),
            'razorpay_payment_id': data.get('razorpay_payment_id'),
            'razorpay_signature': data.get('razorpay_signature')
            }
        try:
            client.utility.verify_payment_signature(data_dict)
            p=Payment.objects.get(razorpay_order_id=data_dict['razorpay_order_id'])
            p.razorpay_payment_id=data_dict['razorpay_payment_id']
            p.razorpay_signature=data_dict['razorpay_signature']
            p.status = 'success'
            p.paid_by=request.user
            p.save()
            p.enquiry.property.is_available=False
            p.enquiry.property.save()
            send_mail(
                subject="Your Advance amount has been successfully paid",
                message=f"Dear {p.paid_by.username},\n\n"
                        f"Your Advance Amount for {p.enquiry.property.title} has been paid successfully.\n\n"
                        f"Your Payment id: {p.razorpay_payment_id}",
                from_email=None,
                recipient_list=[p.paid_by.email],
                fail_silently=False,
            )

            return render(request,'paymentsuccess.html')
        except razorpay.errors.SignatureVerificationError:
            p=Payment.objects.get(razorpay_order_id=data_dict['razorpay_order_id'])
            p.status='failed'
            p.save()
            return redirect('listing:paymentfailure')

class PaymentFailureView(View):
    def get(self, request):
        return render(request,'paymentfailure.html')

class BuyerAdvancedPropertiesView(View):
    def get(self, request):
        p=Property.objects.filter(enquiry__payment__paid_by=request.user,enquiry__payment__status='success')
        context={'p':p}
        return render(request,'buyeradvanceproperties.html',context)

class BuyerRejectedView(View):
    def get(self, request,i):
        e=Enquiry.objects.get(id=i)
        e.buyer_rejected=True
        e.save()
        return redirect('index')



