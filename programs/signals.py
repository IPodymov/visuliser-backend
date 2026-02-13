from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import EducationalProgram

@receiver(post_save, sender=EducationalProgram)
@receiver(post_delete, sender=EducationalProgram)
def clear_program_cache(sender, instance, **kwargs):
    """
    Clear the cache when an EducationalProgram is saved or deleted.
    Since we use cache_page, we might need to clear the entire cache 
    or use specific keys/prefixes if configured.
    For now, we clear the default cache to ensure fresh data.
    """
    cache.clear()
