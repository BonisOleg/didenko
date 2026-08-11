from src.services.models import Service


def list_published_services(limit: int | None = None):
    qs = Service.objects.filter(is_published=True).order_by('sort_order', 'id')
    if limit is not None:
        return qs[:limit]
    return qs


def get_published_service(slug: str) -> Service | None:
    return Service.objects.filter(slug=slug, is_published=True).first()


def resolve_service_seo(service: Service) -> dict:
    return {
        'page_title': service.seo_title or service.title,
        'seo_title': service.seo_title or service.title,
        'seo_description': service.seo_description or service.short_description,
        'seo_h1': service.seo_h1 or service.title,
    }
