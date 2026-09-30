#!/usr/bin/env python3
"""Store/check a portal-scoped HubSpot private-app token without exposing it."""
import argparse
import getpass
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import urllib.error
import urllib.request
import warnings

API = 'https://api.hubapi.com'


class SafeError(Exception):
    pass


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise SafeError('Unexpected API redirect; credential was not forwarded.')


def request(token, path, method='GET', body=None):
    if not path.startswith('/') or path.startswith('//'):
        raise SafeError('Expected an API path, not a URL.')
    req = urllib.request.Request(API + path,
        data=None if body is None else json.dumps(body).encode(), method=method,
        headers={'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'})
    try:
        with urllib.request.build_opener(NoRedirect()).open(req, timeout=30) as response:
            raw = response.read()
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as exc:
        # Response bodies may echo input. Never print them for authentication errors.
        raise SafeError(f'HubSpot returned HTTP {exc.code}; no credential details logged.') from None
    except (urllib.error.URLError, TimeoutError, ValueError):
        raise SafeError('HubSpot request failed; no credential details logged.') from None


def verify(token, portal_id):
    data = request(token, '/oauth/v2/private-apps/get/access-token-info',
                   'POST', {'tokenKey': token})
    if not isinstance(data, dict) or str(data.get('hubId')) != str(portal_id):
        raise SafeError('Token belongs to a different portal or portal could not be verified. Nothing saved.')
    if 'content' not in data.get('scopes', []):
        raise SafeError('Token lacks the required content scope. Add it in the private app and retry. Nothing saved.')
    return data


def credential_path(portal_id):
    if not str(portal_id).isdigit() or int(portal_id) <= 0:
        raise SafeError('Portal ID must be a positive number.')
    return Path.home() / '.config' / 'man-digital' / 'hubspot' / f'{portal_id}.json'


def private_directory(path):
    if path.is_symlink():
        raise SafeError('Credential directory must not be a symlink.')
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    info = path.stat()
    if info.st_uid != os.getuid():
        raise SafeError('Credential directory is not owned by the current user.')
    path.chmod(0o700)


def save_token(token, portal_id):
    target = credential_path(portal_id)
    private_directory(target.parent.parent)
    private_directory(target.parent)
    if target.is_symlink():
        raise SafeError('Credential file must not be a symlink.')
    fd, temporary = tempfile.mkstemp(prefix='.credential-', dir=target.parent)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, 'w') as handle:
            json.dump({'portalId': int(portal_id), 'accessToken': token}, handle)
            handle.write('\n')
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return target


def load_token(portal_id):
    target = credential_path(portal_id)
    for parent in [target.parent.parent, target.parent]:
        if parent.is_symlink() or not parent.is_dir():
            raise SafeError('Missing or unsafe credential directory; run setup.')
        info = parent.stat()
        if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) & 0o077:
            raise SafeError('Credential directory must be owned by you with mode 700.')
    try:
        fd = os.open(target, os.O_RDONLY | os.O_NOFOLLOW)
        with os.fdopen(fd) as handle:
            info = os.fstat(handle.fileno())
            if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) & 0o077:
                raise SafeError('Credential file must be a private regular file owned by you (mode 600).')
            data = json.load(handle)
        if str(data.get('portalId')) != str(portal_id):
            raise SafeError('Stored portal ID does not match the selected portal.')
        token = data.get('accessToken')
        if not isinstance(token, str) or not token.strip():
            raise SafeError('Credential file has no usable token; run setup.')
        return token
    except (OSError, ValueError, AttributeError):
        raise SafeError('Credential file is missing or invalid; run setup.') from None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['setup', 'check'])
    parser.add_argument('--portal-id', required=True, type=int)
    args = parser.parse_args()
    credential_path(args.portal_id)
    if args.action == 'setup':
        if not sys.stdin.isatty():
            raise SafeError('Run setup directly in an interactive terminal; do not pipe a token.')
        with warnings.catch_warnings():
            warnings.simplefilter('error', getpass.GetPassWarning)
            try:
                token = getpass.getpass(f'HubSpot private-app token for portal {args.portal_id} (hidden): ').strip()
            except getpass.GetPassWarning:
                raise SafeError('Hidden input is unavailable; nothing saved.') from None
        if not token or any(ch.isspace() for ch in token):
            raise SafeError('Token is empty or contains whitespace; nothing saved.')
        verify(token, args.portal_id)
        target = save_token(token, args.portal_id)
        print(f'Verified portal {args.portal_id} and content scope. Saved privately to {target} (mode 600).')
    else:
        verify(load_token(args.portal_id), args.portal_id)
        print(f'Verified portal {args.portal_id} and content scope. Ready for CMS API draft edits.')


if __name__ == '__main__':
    try:
        main()
    except (SafeError, OSError):
        # OSError can contain arbitrary filenames; avoid accidental credential disclosure.
        exc = sys.exc_info()[1]
        print(str(exc) if isinstance(exc, SafeError) else 'Local credential operation failed; nothing logged.', file=sys.stderr)
        sys.exit(1)
    except (KeyboardInterrupt, EOFError):
        print('\nCancelled; nothing saved.', file=sys.stderr)
        sys.exit(1)
