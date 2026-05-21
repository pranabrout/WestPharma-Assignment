import requests
import re

res = requests.get('https://automationexercise.com/products', timeout=30)
print('status', res.status_code)
html = res.text
print('overlay count', html.count('product-overlay'))
print('productinfo count', html.count('productinfo'))
print('add to cart count', html.lower().count('add to cart'))
print('add to cart button count', html.lower().count('add to cart'))

matches = re.findall(r'<a[^>]+href=["\']([^"\']*product[^"\']*)["\'][^>]*>(.*?)</a>', html, re.IGNORECASE | re.DOTALL)
print('product links found:', len(matches))
for i, (href, text) in enumerate(matches[:10], 1):
    print(i, href, repr(text.strip())[:80])

# print sample product divs
for m in re.finditer(r'(<div[^>]+class=["\']([^"\']*product[^"\']*)["\'][^>]*>.*?</div>)', html, re.IGNORECASE | re.DOTALL):
    print('DIV', m.group(2))
    snippet = m.group(1)
    if 'add to cart' in snippet.lower():
        print(snippet[:500].replace('\n', ' '))
        break
