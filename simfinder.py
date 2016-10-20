import os.path, time, platform, subprocess, sys, argparse, plistlib

CORE_SIMULATOR = 'com.apple.CoreSimulator.SimDeviceType'
RUN_TIME = 'com.apple.CoreSimulator.SimRuntime.iOS'

class SimulatorFinder(object):

    def __init__(self, args):
        super(SimulatorFinder, self).__init__()
        self.device = args.device
        self.file_name = args.name
        self.print_list = args.print_list
        self.simulator_path = '{}/Library/Developer/CoreSimulator'.format(os.path.expanduser('~'))
        self.runtime = '{0}-{1}'.format(RUN_TIME, args.runtime)
        self.simulators = {
            'pro' : 'iPad-Pro',
            'pro9,7' : 'iPad-Pro--9-7-inch-',
            'air2' : 'iPad-Air-2',
            'air' : 'iPad-Air',
            'retina' : 'iPad-Retina',
            '7+' : 'iPhone-7-Plus',
            '7' : 'iPhone-7',
            '6s+' : 'iPhone-6s-Plus',
            '6s' : 'iPhone-6s',
            '6+' : 'iPhone-6-Plus',
            '6' : 'iPhone-6',
            'se' : 'iPhone-SE',
            '5s' : 'iPhone-5s',
            '5' : 'iPhone-5',
            '4s' : 'iPhone-4s',
            '4' : 'iPhone-4'
        }
        self.simulator = None

    def get_directory(self):
        for dirpath, dirnames, files in os.walk(self.simulator_path):
            for name in files:
                if name.lower() == self.file_name.lower():
                    the_path = self.get_file(os.path.join(dirpath, name))
                    if the_path is not None:
                        return the_path

    def get_file(self, path):
        names = path.split('/')
        if names[7] == self.simulator:
            return path

    def parse_plist(self):
        device = '{0}.{1}'.format(CORE_SIMULATOR, self.selected_device())
        p_list = '{}/Devices/device_set.plist'.format(self.simulator_path)
        data = plistlib.readPlist(p_list)
        runtime = data['DefaultDevices'][self.runtime]
        if self.print_list:
            print('\n')
            for key, value in runtime.items():
                print('{0}  {1}'.format( key.rsplit('.', 1)[1], value))
            print('\n')
        return runtime[device]

    def selected_device(self):
        return self.simulators[self.device]

    def find(self):
        self.simulator = self.parse_plist()
        path = self.get_directory()

        if path:
            print ('Path\n{}\n'.format(path))
            subprocess.call(['open', '-R', path])
        else:
            print('File not found!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--device', help='Default iOS device', required=True)
    parser.add_argument('-n','--name', help='Name of file to search', required=True)
    parser.add_argument('-r','--runtime', help='Device runtime, Default: 10-0')
    parser.add_argument('-p', '--print', dest='print_list', help='Print list of device name and uuid', action='store_true')
    parser.set_defaults(runtime='10-0', print_list=False)
    args = parser.parse_args()

    sim = SimulatorFinder(args)
    sim.find()
