def shorten_amazon_url(url: str) -> str:
    if '/dp/' in url:
        parts = url.split('/dp/')
        return f"{parts[0]}/dp/{parts[1].split('/')[0]}"
    return url


def shorten_target_url(url: str) -> str:
    if '/p/' in url and '/-/A-' in url:
        parts = url.split('/p/')
        return f"{parts[0]}/p/{parts[1].split('/-/A-')[0]}/-/A-{parts[1].split('/-/A-')[1].split('#')[0].split('?')[0]}"
    return url


def shorten_walmart_url(url: str) -> str:
    if '/ip/' in url:
        parts = url.split('/ip/')
        return f"{parts[0]}/ip/{parts[1].split('?')[0]}"
    return url


def shorten_ulta_url(url: str) -> str:
    if '/p/' in url and 'xlsImpprod' in url:
        parts = url.split('/p/')
        return f"{parts[0]}/p/{parts[1].split('xlsImpprod')[0]}xlsImpprod{parts[1].split('xlsImpprod')[1].split('?')[0]}"
    return url


def shorten_bestbuy_url(url: str) -> str:
    if '/site/' in url and '.p' in url and 'skuId=' in url:
        parts = url.split('/site/')
        return f"{parts[0]}/site/{parts[1].split('.p')[0]}.p?skuId={parts[1].split('skuId=')[1].split('&')[0]}"
    return url


def shorten_ebay_url(url: str) -> str:
    if '/itm/' in url:
        parts = url.split('/itm/')
        return f"{parts[0]}/itm/{parts[1].split('/')[0]}"
    return url


def shorten_bathandbodyworks_url(url: str) -> str:
    if '/p/' in url:
        parts = url.split('/p/')
        return f"{parts[0]}/p/{parts[1].split('?')[0]}"
    return url


def shorten_oarsandalps_url(url: str) -> str:
    if '/products/' in url and 'variant=' in url:
        parts = url.split('/products/')
        return f"{parts[0]}/products/{parts[1].split('?variant=')[0]}?variant={parts[1].split('variant=')[1].split('&')[0]}"
    return url


def shorten_url(url: str) -> str:
    if "amazon.com" in url:
        return shorten_amazon_url(url)
    elif "target.com" in url:
        return shorten_target_url(url)
    elif "walmart.com" in url:
        return shorten_walmart_url(url)
    elif "ulta.com" in url:
        return shorten_ulta_url(url)
    elif "bestbuy.com" in url:
        return shorten_bestbuy_url(url)
    elif "ebay.com" in url:
        return shorten_ebay_url(url)
    elif "bathandbodyworks.com" in url:
        return shorten_bathandbodyworks_url(url)
    elif "oarsandalps.com" in url:
        return shorten_oarsandalps_url(url)
    return url
