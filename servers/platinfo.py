import json
import os.path
import platform
import warnings


if __name__ == '__main__':
    machine = platform.machine()
    processor = platform.processor()
    system = platform.system()

    cpuinfo_f = '/proc/cpuinfo'

    if (processor in {machine, 'unknown'} and os.path.exists(cpuinfo_f)):
        with open(cpuinfo_f, 'rt') as f:
            for line in f:
                if line.startswith('model name'):
                    _, _, p = line.partition(':')
                    processor = p.strip()
                    break

    if 'Linux' in system:

        with warnings.catch_warnings():
            # see issue #1322 for more information
            warnings.filterwarnings(
                'ignore',
                'dist\(\) and linux_distribution\(\) '
                'functions are deprecated .*',
                PendingDeprecationWarning,
            )
            distname, distversion, distid = platform.dist('')

        distribution = '{} {}'.format(distname, distversion).strip()

    else:
        distribution = None

    data = {
        'cpu': processor,
        'arch': machine,
        'system': '{} {}'.format(system, platform.release()),
        'distribution': distribution
    }

    print(json.dumps(data))
