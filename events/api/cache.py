from django.core.cache import cache


def get_or_cache_queryset(cache_key, queryset, timeout):
    cached_queryset = cache.get(cache_key)
    if not cached_queryset:
        cached_queryset = list(queryset)
        cache.set(cache_key, cached_queryset, timeout=timeout)
    return cached_queryset
