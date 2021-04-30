"""Monkey Patch to fake yarn environment.

Usage
-----
python monkeypatch_fromconfig.py config.yaml params.yaml launcher.yaml - model - train
"""

import contextlib
import cluster_pack
import skein
from collections import namedtuple
from cluster_pack.skein import skein_launcher


@contextlib.contextmanager
def _MonkeyClient():  # pylint: disable=invalid-name
    """Monkey skein Client."""

    Client = namedtuple("Client", "application_report")
    Report = namedtuple("Report", "tracking_url")

    def application_report(app_id):
        return Report(app_id)

    yield Client(application_report)


def _monkey_submit_func(func, args, **kwargs):
    """Monkey patch submit function."""
    # pylint: disable=unused-argument
    print("Uploading PEX and running on YARN")
    func(*args)


setattr(cluster_pack, "upload_env", lambda *_, **__: None)
setattr(cluster_pack, "upload_zip", lambda *_, **__: None)
setattr(skein, "Client", _MonkeyClient)
setattr(skein_launcher, "submit_func", _monkey_submit_func)


if __name__ == "__main__":
    from fromconfig.cli.main import main

    main()
