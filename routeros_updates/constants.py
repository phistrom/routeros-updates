from __future__ import unicode_literals


ARCHITECTURES = (
    "mipsbe",
    "smips",
    "tile",
    "ppc",
    "arm",
    "x86",
    "mmips",
)

DEFAULT_ENCODING = "utf-8"

LATEST_CHANNEL_URL = {
    "lts": "{scheme}://upgrade.mikrotik.com/routeros/LATEST.6fix",
    "stable": "{scheme}://upgrade.mikrotik.com/routeros/LATEST.6",
    "dev": "{scheme}://upgrade.mikrotik.com/routeros/LATEST.7",
    "testing": "{scheme}://upgrade.mikrotik.com/routeros/LATEST.6rc",
}

DOWNLOAD_URL = {
    "main": "{scheme}://upgrade.mikrotik.com/routeros/{version}/routeros-{arch}-{version}.npk",
    "all": "{scheme}://upgrade.mikrotik.com/routeros/{version}/all_packages-{arch}-{version}.zip",
}

CHANGELOG_URL = "{scheme}://upgrade.mikrotik.com/routeros/{version}/CHANGELOG"

CLI_DESCRIPTION = """
    Check for and/or download Mikrotik RouterOS updates. 
""".strip()

CLI_EXAMPLES = """
====================
    Examples:

    Download the latest mipsbe package from the 'stable' channel:
        >>{name} download mipsbe<<

    Download the latest, x86 package from the 'long term' channel:
        >>{name} --channel lts download x86<<

    Echo the latest patch notes for the 'testing' channel:
        >>{name} --channel testing notes<<

    Echo the URL to download the latest, 'stable' optional packages zip file for the arm architecture:
        >>{name} url arm --package all<<

    Download the optional packages for the ppc architecture from the 'long term' channel to /tmp:
        >>{name} --channel lts download ppc --package all --file /tmp<<

""".rstrip("\r\n").format(name="ros-updates").replace(">>", "\x1b[1;33m").replace("<<", "\x1b[0m")
