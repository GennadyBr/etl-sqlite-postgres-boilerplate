""" Config """
import os

cur_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(cur_dir)
log_config_filename = f'{cur_dir}/log_conf.yaml'

if not os.path.exists(f'{parent_dir}/logs'):
    os.makedirs(f'{parent_dir}/logs')

log_rotation_filename = f'{parent_dir}/logs/logs.log'
