"""Compile approved editorial content to public JavaScript using an explicit allowlist.

No source documents, customer records, or secrets belong in this repository.
The output directory is public in its entirety, including unreferenced assets.
"""
import json
import math
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {'rakit', 'detailing', 'filet', 'repaint', 'repair'}
MAP_HOSTS = {'www.google.com', 'maps.google.com', 'maps.app.goo.gl'}
SOCIAL_HOSTS = {
    'instagram': {'instagram.com', 'www.instagram.com'},
    'shopee': {'shopee.co.id', 'www.shopee.co.id', 'shopee.id', 'www.shopee.id'},
}


def text(value, field, required=True, limit=1600):
    if not isinstance(value, str) or len(value) > limit:
        raise ValueError(f'{field}: must be text up to {limit} characters')
    value = value.strip()
    if required and not value:
        raise ValueError(f'{field}: text required')
    return value


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', value):
        raise ValueError('Invalid public record identifier')
    return value


def image_path(value):
    if not isinstance(value, str) or not re.fullmatch(r'assets/[a-zA-Z0-9_/-]+\.(?:webp|png|jpe?g)', value):
        raise ValueError('Image must be a local JPEG/PNG/WebP asset')
    if not (ROOT / 'dist' / value).is_file():
        raise ValueError('Referenced public image is missing')
    return value


def iso_date(value):
    value = text(value, 'date', limit=10)
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        raise ValueError('Use an ISO date: YYYY-MM-DD')
    date.fromisoformat(value)
    return value


def trusted_url(value, field, hosts):
    value = text(value, field, required=False, limit=1500)
    if not value:
        return ''
    parsed = urlparse(value)
    if parsed.scheme != 'https' or parsed.hostname not in hosts or parsed.username or parsed.password or parsed.port not in [None, 443]:
        raise ValueError(f'{field}: use an official HTTPS link')
    return value


def create_qr(value, filename):
    """Create a local SVG QR without requiring ReportLab."""
    destination = ROOT / 'dist' / 'assets' / filename
    try:
        import qrcode
        import qrcode.image.svg

        factory = qrcode.image.svg.SvgPathImage
        image = qrcode.make(value, image_factory=factory)
        image.save(str(destination))
    except ImportError as error:
        raise RuntimeError(
            'Package qrcode is required only for QR generation'
        ) from error
    return 'assets/' + filename


def compile_site(source):
    result = {'contact': {'whatsapp': '', 'whatsappQr': '', 'address': '', 'hours': '', 'mapsUrl': '', 'latitude': None, 'longitude': None},
              'socials': {'instagram': '', 'instagramQr': '', 'shopee': '', 'shopeeQr': ''}, 'projects': [], 'steps': [], 'progress': []}
    contact = source.get('contact', {})
    if contact.get('approved') is True:
        phone = text(contact.get('whatsapp', ''), 'whatsapp', required=False, limit=255)
        if phone and not (
            re.fullmatch(r'[1-9]\d{7,14}', phone)
            or re.fullmatch(r'https://wa\.me/[1-9]\d{7,20}', phone)
        ):
            raise ValueError('WhatsApp must be an international number or a valid wa.me link')
        result['contact']['whatsapp'] = phone
        if phone:
            result['contact']['whatsappQr'] = create_qr('https://wa.me/' + phone, 'qr-whatsapp.svg')
        for key in ['address', 'hours']:
            result['contact'][key] = text(contact.get(key, ''), key, required=False, limit=500)
        url = text(contact.get('mapsUrl', ''), 'mapsUrl', required=False, limit=1500)
        if url:
            parsed = urlparse(url)
            if parsed.scheme != 'https' or parsed.hostname not in MAP_HOSTS or parsed.username or parsed.password or parsed.port not in [None, 443]:
                raise ValueError('Map URL requires an approved HTTPS Google Maps origin')
        result['contact']['mapsUrl'] = url
        lat, lon = contact.get('latitude'), contact.get('longitude')
        if lat is not None or lon is not None:
            if any(isinstance(n, bool) or not isinstance(n, (int, float)) or not math.isfinite(n) for n in [lat, lon]):
                raise ValueError('Coordinates must be a finite numeric pair')
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                raise ValueError('Coordinates outside valid ranges')
            result['contact'].update(latitude=lat, longitude=lon)
    socials = source.get('socials', {})
    if socials.get('approved') is True:
        for channel in ['instagram', 'shopee']:
            url = trusted_url(socials.get(channel, ''), channel, SOCIAL_HOSTS[channel])
            result['socials'][channel] = url
            if url:
                result['socials'][channel + 'Qr'] = create_qr(url, 'qr-' + channel + '.svg')
    seen = set()
    for project in source.get('projects', []):
        if project.get('approved') is not True:
            continue
        pid = identifier(project.get('id'))
        if pid in seen:
            raise ValueError('Duplicate project ID')
        seen.add(pid)
        if project.get('category') not in CATEGORIES:
            raise ValueError('Unknown portfolio category')
        if not isinstance(project.get('concept'), bool):
            raise ValueError('Set concept to true or false explicitly')
        record = {'id': pid, 'category': project['category'], 'image': image_path(project.get('image')), 'concept': project['concept']}
        for key in ['label', 'title', 'subtitle', 'alt', 'status', 'focus', 'description', 'result']:
            record[key] = text(project.get(key), key)
        result['projects'].append(record)
    steps = source.get('steps', [])
    if len(steps) != 5:
        raise ValueError('Five process stages are required by the current HTML layout')
    for step in steps:
        result['steps'].append({key: text(step.get(key), key) for key in ['title', 'description']})
    seen.clear()
    for entry in source.get('progress', []):
        if entry.get('approved') is not True:
            continue
        pid = identifier(entry.get('id'))
        if pid in seen:
            raise ValueError('Duplicate progress ID')
        seen.add(pid)
        record = {'id': pid, 'date': iso_date(entry.get('date'))}
        for key in ['title', 'projectCode', 'stage', 'description']:
            record[key] = text(entry.get(key), key)
        percentage = entry.get('percentage', 0)
        if isinstance(percentage, bool) or not isinstance(percentage, int) or not 0 <= percentage <= 100:
            raise ValueError('Progress must be an integer from 0 to 100')
        status = entry.get('status', 'production')
        if status not in ['production', 'shipping', 'delivered']:
            raise ValueError('Unknown order status')
        if status != 'production' and percentage != 100:
            raise ValueError('Finish production at 100% before shipping')
        record.update(percentage=percentage, status=status, photos=[])
        photos = entry.get('photos', [])
        if not isinstance(photos, list) or (photos and not 3 <= len(photos) <= 12):
            raise ValueError('Use 3 to 12 photos for an order slideshow')
        if 'percentage' in entry and len(photos) < 3:
            raise ValueError('New order cards require at least 3 photos')
        for photo in photos:
            record['photos'].append({'image': image_path(photo.get('image')), 'alt': text(photo.get('alt'), 'photo alt')})
        if entry.get('image'):
            record.update(image=image_path(entry['image']), alt=text(entry.get('alt'), 'alt'))
        record['timeline'] = []
        for item in entry.get('timeline', []):
            if item.get('approved') is True:
                record['timeline'].append({'date': iso_date(item.get('date')), 'stage': text(item.get('stage'), 'stage'), 'description': text(item.get('description'), 'description')})
        result['progress'].append(record)
    result['progress'].sort(key=lambda item: item['date'], reverse=True)
    return result


if __name__ == '__main__':
    source = json.loads((ROOT / 'content/site.json').read_text())
    compiled = compile_site(source)
    output = "/* Generated from approved content. Edit content/site.json, then run scripts/prepare-content.py. */\n'use strict';\nwindow.GDT_CONTENT = " + json.dumps(compiled, ensure_ascii=False, indent=2) + ';\n'
    destination = ROOT / 'dist/content.js'
    temporary = destination.with_suffix('.tmp')
    temporary.write_text(output)
    temporary.replace(destination)
    print(f'Published content: {len(compiled["projects"])} portfolio entries, {len(compiled["progress"])} progress records. Unapproved records and unlisted fields excluded.')
