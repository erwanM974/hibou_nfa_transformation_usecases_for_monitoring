#
# Copyright 2023 Erwan Mahe (github.com/erwanM974)
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from implem.commons import try_mkdir,empty_directory
from implem.calls_gen import *
from implem.trace_kinds import GlobalTraceKind

def reset_directories(int_name):
    folders = [GlobalTraceKind.ACCEPTED.get_tracegen_folder_name(int_name),
               GlobalTraceKind.SLICE.get_tracegen_folder_name(int_name),
               GlobalTraceKind.CHUNKS.get_tracegen_folder_name(int_name),
               GlobalTraceKind.NOISE.get_tracegen_folder_name(int_name)]
    #
    for parent_folder in folders:
        try_mkdir(parent_folder)
        empty_directory(parent_folder)


def generation_process(int_name,num_slices_per_mu,is_slice_wide,num_mut_per_mu):
    #
    reset_directories(int_name)
    #
    print("exploring semantics for " + int_name)
    generate_accepted(int_name)
    #
    print("generating slices for " + int_name)
    tracegen_path = GlobalTraceKind.ACCEPTED.get_tracegen_folder_name(int_name)
    for acc_htf_file_name in os.listdir(tracegen_path):
        acc_htf_file_name = acc_htf_file_name[:-4]
        generate_slices(int_name,acc_htf_file_name,num_slices_per_mu,is_slice_wide)
    #
    print("generating noise mutants and chunk mutants for " + int_name)
    all_orig_traces_names = [trace_htf_file_name[:-4] for trace_htf_file_name in os.listdir(tracegen_path)]
    for i in range(0,len(all_orig_traces_names)):
        trace_htf_file_name = all_orig_traces_names[i]
        #
        for j in range(1,num_mut_per_mu+1):
            generate_noise_mutant(int_name,trace_htf_file_name,j,10)
            generate_chunks_mutant(int_name,trace_htf_file_name,j,10)
        #
    #

