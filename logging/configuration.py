import configparser

config_file = 'setting.ini'     #configureation 파일 경로

config = configparser.ConfigParser()
config.read(config_file)

input_dir = config['input']['input_dir']
ratio = float(config['input']['test_ratio'])
