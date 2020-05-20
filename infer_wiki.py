#!/usr/bin/env python3

import sys
import os
import datetime
import string
import hdhp
import notebook_helpers
import seaborn as sns
import json
import pickle

def usage(status=0):
    ''' Display usage information and exit with specified status '''
    progname = os.path.basename(sys.argv[0])
    print(f'''Usage: {progname} [DATA_FILE] [options] [FILE_NAME]

    [DATA_FILE]         Pickle file of sorted list of tuples to run inference on
    -g [FILE_NAME]      Specifies which file to save the graphs into
    -p [FILE_NAME]      Specifies which file to save the particle into
    -n [FILE_NAME]      Specifies which file to save the norms object into
    ''')
    sys.exit(status)

def save_object(object, file_name):
    with open(file_name, 'wb') as object_file:
        pickle.dump(object, object_file)
        object_file.close()

def load_object(file_name):
    with open(file_name, 'rb') as obj_file:
        obj = pickle.load(obj_file)
        obj_file.close()
    return obj

def infer_and_save(tuples_list, particle_file, norms_file):

    '''Set Parameters '''
    '''Parameters used are from examples in notebook on hdhp github'''
    doc_min_length = 5
    doc_length = 10
    words_per_pattern = 50
    alpha_0 = (2.5, 0.75)
    mu_0 = (2, 0.5)
    omega = 3.5
    num_patterns = 10

    '''Run inference'''
    particle, norms = hdhp.infer(tuples_list, alpha_0=alpha_0, mu_0=mu_0, omega=omega, num_particles=4, 
                                    seed=512, resample_every=10, progress_file='progress.log')

    print('Saving particle and norm object to files...')
    save_object(particle, particle_file)
    save_object(norms, norms_file)

def make_process_plot(inf_process, file_name):

    start_date = datetime.datetime(2005, 1, 1)
    # user limit is number of users to plot, users is which specific users, while fig_height_per_user is the graph height
    # users is based on highest users
    inf_process.plot(task_detail=True, save_to_file=True, num_samples=1000, seed=170, fig_height_per_user=10,users=[26, 34, 35, 37, 42, 43],
                    user_limit=5, time_unit='months', fig_width=80, filename=file_name,
                    T_min=0, start_date=start_date, paper=True, label_every=6)

def main():
    '''Declare variables'''
    arguments = sys.argv[1:]
    if len(arguments) == 0:
        usage(1)
    data_file = arguments.pop(0)
    particle_file = 'pickle_files/particle.obj'
    norms_file = 'pickle_files/norms.obj'
    graph_file = 'user_timelines'

    ''' Parse command line arguments'''
    while len(arguments) > 0:
        arg = arguments.pop(0)
        if arg == '-p':
            particle_file = arguments.pop(0)
        elif arg == '-n':
            norms_file = arguments.pop(0)
        elif arg == '-g':
            graph_file = arguments.pop(0)
        else:
            usage(1)

    '''Get tuples list'''
    print('Loading object from file')
    tuples_list = load_object(data_file)

    '''Run inference and save'''
    print('Running inference...')
    infer_and_save(tuples_list, particle_file, norms_file)

    '''Load particle and convert'''
    # particle = load_object(particle_file)

    # Export the inferred process
    print('Converting particle to process')
    # inf_process = particle.to_process()
    
    print('Making plot')
    # make_process_plot(inf_process, graph_file)

# Main Execution
if __name__ == '__main__':
    main()
