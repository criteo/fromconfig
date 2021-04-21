"""Monkey Patch to fake yarn environment.

Usage
-----
python monkeypatch_fromconfig.py config.yaml params.yaml launcher.yaml - model - train
"""

import cluster_pack
import skein
from collections import namedtuple
from cluster_pack.skein import skein_launcher


class _MonkeyClient:
    """Monkey patch skein Client."""

    # pylint: disable=unused-argument

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        return self

    def application_report(self, app_id):
        Report = namedtuple("Report", "tracking_uri")
        return Report("127.0.0.1")


def _monkey_submit_func(func, args, **kwargs):
    """Monkey patch submit function."""
    # pylint: disable=unused-argument
    print("Monkey Training on Yarn")
    func(*args)


setattr(cluster_pack, "upload_env", lambda *_, **__: None)
setattr(cluster_pack, "upload_zip", lambda *_, **__: None)
setattr(skein, "Client", _MonkeyClient)
setattr(skein_launcher, "submit_func", _monkey_submit_func)


if __name__ == "__main__":
    from fromconfig.cli.main import main

    main()
