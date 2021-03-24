import os.path
import pkgutil
import shutil
import sys
import struct
import tempfile

# Useful for very coarse version differentiation.
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:
    iterbytes = iter
else:
    def iterbytes(buf):
        return (ord(byte) for byte in buf)

try:
    from base64 import b85decode
except ImportError:
    _b85alphabet = (b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    b"abcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~"

    def b85decode(b):
        _b85dec=[None] * 256
        for i, c in enumerate(iterbytes(_b85alphabet)):
            _b85dec[c]=i

        padding=(-len(b)) % 5
        b=b + b'~' * padding
        out=[]
        packI=struct.Struct('!I').pack

        for i in range(0, len(b), 5):
            chunk=b[i:i + 5]
            acc=0
            try:
                for c in iterbytes(chunk):
                    acc=acc * 85 + _b85dec[c]
            except TypeError:
                for j, c in enumerate(iterbytes(chunk)):
                    if _b85dec[c] is None:
                        raise ValueError(
                            'bad base85 character at position %d' % (i + j)
                        )
                raise
            try:
                out.append(packI(acc))
            except struct.error:
                raise ValueError('base85 overflow in hunk starting at byte %d'
                                 % i)

        result=b''.join(out)
        if padding:
            result=result[:-padding]
        return result


def bootstrap(tmpdir=None):
    # Import pip so we can use it to install pip and maybe setuptools too
    import pip._internal
    from pip._internal.commands.install import InstallCommand
    from pip._internal.req.constructors import install_req_from_line

    # Wrapper to provide default certificate with the lowest priority
    class CertInstallCommand(InstallCommand):
        def parse_args(self, args):
            # If cert isn't specified in config or environment, we provide our
            # own certificate through defaults.
            # This allows user to specify custom cert anywhere one likes:
            # config, environment variable or argv.
            if not self.parser.get_default_values().cert:
                self.parser.defaults["cert"]=cert_path  # calculated below
            return super(CertInstallCommand, self).parse_args(args)

    pip._internal.commands_dict["install"]=CertInstallCommand

    implicit_pip=True
    implicit_setuptools=True
    implicit_wheel=True

    # Check if the user has requested us not to install setuptools
    if "--no-setuptools" in sys.argv or os.environ.get("PIP_NO_SETUPTOOLS"):
        args=[x for x in sys.argv[1:] if x != "--no-setuptools"]
        implicit_setuptools=False
    else:
        args=sys.argv[1:]

    # Check if the user has requested us not to install wheel
    if "--no-wheel" in args or os.environ.get("PIP_NO_WHEEL"):
        args=[x for x in args if x != "--no-wheel"]
        implicit_wheel=False

    # We only want to implicitly install setuptools and wheel if they don't
    # already exist on the target platform.
    if implicit_setuptools:
        try:
            import setuptools  # noqa
            implicit_setuptools=False
        except ImportError:
            pass
    if implicit_wheel:
        try:
            import wheel  # noqa
            implicit_wheel=False
        except ImportError:
            pass

    # We want to support people passing things like 'pip<8' to get-pip.py which
    # will let them install a specific version. However because of the dreaded
    # DoubleRequirement error if any of the args look like they might be a
    # specific for one of our packages, then we'll turn off the implicit
    # install of them.
    for arg in args:
        try:
            req=install_req_from_line(arg)
        except Exception:
            continue

        if implicit_pip and req.name == "pip":
            implicit_pip=False
        elif implicit_setuptools and req.name == "setuptools":
            implicit_setuptools=False
        elif implicit_wheel and req.name == "wheel":
            implicit_wheel=False

    # Add any implicit installations to the end of our args
    if implicit_pip:
        args += ["pip"]
    if implicit_setuptools:
        args += ["setuptools"]
    if implicit_wheel:
        args += ["wheel"]

    # Add our default arguments
    args=["install", "--upgrade", "--force-reinstall"] + args

    delete_tmpdir=False
    try:
        # Create a temporary directory to act as a working directory if we were
        # not given one.
        if tmpdir is None:
            tmpdir=tempfile.mkdtemp()
            delete_tmpdir=True

        # We need to extract the SSL certificates from requests so that they
        # can be passed to --cert
        cert_path=os.path.join(tmpdir, "cacert.pem")
        with open(cert_path, "wb") as cert:
            cert.write(pkgutil.get_data("pip._vendor.certifi", "cacert.pem"))

        # Execute the included pip and use it to install the latest pip and
        # setuptools from PyPI
        sys.exit(pip._internal.main(args))
