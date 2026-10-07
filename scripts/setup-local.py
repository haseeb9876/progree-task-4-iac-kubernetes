#!/usr/bin/env python3
"""Create local credentials without printing or overwriting existing values."""
import csv
import os
import subprocess
from pathlib import Path
import secrets
import shutil

root = Path(__file__).resolve().parents[1]
directory = root / '.secrets'
directory.mkdir(mode=0o700, exist_ok=True)
if os.name == 'nt':
    # chmod does not restrict Windows ACLs. Protect the parent before writing.
    identity = subprocess.check_output(
        ['whoami', '/user', '/fo', 'csv', '/nh'], text=True
    )
    sid = next(csv.reader(identity.strip().splitlines()))[1]
    subprocess.run(
        ['icacls', str(directory), '/inheritance:r', '/grant:r',
         f'*{sid}:(OI)(CI)F', '*S-1-5-18:(OI)(CI)F'],
        check=True, stdout=subprocess.DEVNULL,
    )
else:
    directory.chmod(0o700)
for name in ('mongo_root_password', 'mongo_app_password', 'redis_password', 'jwt_secret'):
    path = directory / name
    if not path.exists():
        # The private parent directory restricts host access. Read-only mounts
        # must be readable by different non-root container user IDs.
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as handle:
            handle.write(secrets.token_hex(32) + '\n')
        path.chmod(0o444)
        print(f'Created .secrets/{name} (value hidden)')
print('Local setup ready. Existing credentials were preserved.')
