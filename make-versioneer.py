
def unquote(s):
    return s.replace("%", "%%")

def create_script():
    vcs = "git"
    if vcs not in ("git",):
        raise ValueError("Unhandled revision-control system '%s'" % vcs)
    f = open("versioneer.py", "w")
    def get(fn): return open(fn, "r").read()
    f.write(get("src/header.py"))
    f.write('VCS = "%s"\n' % vcs)
    for line in open("src/%s/long-version.py" % vcs, "r").readlines():
        if line.startswith("#### START"):
            f.write("LONG_VERSION_PY = '''\n")
        elif line.startswith("#### SUBPROCESS_HELPER"):
            f.write(unquote(get("src/subprocess-helper.py")))
        elif line.startswith("#### MIDDLE"):
            f.write(unquote(get("src/%s/middle.py" % vcs)))
        elif line.startswith("#### END"):
            f.write("'''\n")
        else:
            f.write(line)
    f.write(get("src/subprocess-helper.py"))
    f.write(get("src/%s/middle.py" % vcs))
    f.write(get("src/%s/install.py" % vcs))
    f.write(get("src/trailer.py"))
    f.close()

if __name__ == '__main__':
    create_script()
