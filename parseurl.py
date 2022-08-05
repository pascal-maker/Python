from urllib.parse import urljoin

base_url = 'https://apps.apple.com/be/app/lovia/id1574149291?l=nl'

path = 'https://play.google.com/store/apps/details?id=com.lovialove'

result = urljoin(base_url, path)

# 👇️ https://example.com/qrcode/androidios/001.png
print(result)

# 👇️ /qrcode/android/ios/001.png
print(urljoin('/qrcode/android/', 'ios/001.png'))

