from .models import SiteInfo


def site_info(request):
    """اطلاعات سایت را در تمام تمپلیت‌ها در دسترس قرار می‌دهد."""
    return {'site': SiteInfo.load()}
