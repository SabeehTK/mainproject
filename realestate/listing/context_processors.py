from listing.models import Property
from accounts.models import Profile


def links(request):
    p=Property.objects.all()
    pf=Profile.objects.all()
    return {'propertylist': p, 'profilelist': pf}