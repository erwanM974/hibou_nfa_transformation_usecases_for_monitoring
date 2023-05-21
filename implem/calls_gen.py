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

import subprocess
import os

from implem.commons import FOLDER_MODEL
from implem.trace_kinds import GlobalTraceKind

def generate_accepted(int_name):
    hsf_file = os.path.join(FOLDER_MODEL, "{}.hsf".format(int_name))
    hif_file = os.path.join(FOLDER_MODEL, "{}.hif".format(int_name))
    hcf_file = os.path.join(FOLDER_MODEL, "{}_explo.hcf".format(int_name))
    #
    command = ["./hibou_label.exe", "explore", hsf_file, hif_file, hcf_file]
    #print( " ".join(command) )
    #
    output = subprocess.check_output(command, text=True)
    #print(output)
    #

def generate_slices(int_name,accepted_htf_name,num_slices,is_slice_wide):
    #
    hsf_file = os.path.join(FOLDER_MODEL, "{}.hsf".format(int_name))
    tracegen_path = GlobalTraceKind.ACCEPTED.get_tracegen_folder_name(int_name)
    acc_htf_file = os.path.join(tracegen_path, "{}.htf".format(accepted_htf_name))
    #
    parent_folder = GlobalTraceKind.SLICE.get_tracegen_folder_name(int_name)
    #
    command = ["./hibou_label.exe", "slice", hsf_file, acc_htf_file, "-p", parent_folder, "-k", "slice", "-n", accepted_htf_name]
    #
    if num_slices != None:
        command += ["-r", str(num_slices)]
        if is_slice_wide:
            command += ["-w"]
    #
    output = subprocess.check_output(command, text=True)
    #print(output)
    #

def generate_noise_mutant(int_name,orig_htf_name,mut_id,max_insert_noise):
    #
    hsf_file = os.path.join(FOLDER_MODEL, "{}.hsf".format(int_name))
    tracegen_path = GlobalTraceKind.ACCEPTED.get_tracegen_folder_name(int_name)
    htf_file = os.path.join(tracegen_path, "{}.htf".format(orig_htf_name))
    #
    parent_folder = GlobalTraceKind.NOISE.get_tracegen_folder_name(int_name)
    #
    name = "{}_noise_{}".format(orig_htf_name,mut_id)
    command = ["./hibou_label.exe", "mutate_insert_noise", hsf_file, htf_file, "-p", parent_folder, "-n", name, "-m", str(max_insert_noise)]
    #
    output = subprocess.check_output(command, text=True)
    #print(output)
    #

def generate_chunks_mutant(int_name,orig_htf_name,mut_id,max_remove_actions):
    #
    hsf_file = os.path.join(FOLDER_MODEL, "{}.hsf".format(int_name))
    tracegen_path = GlobalTraceKind.ACCEPTED.get_tracegen_folder_name(int_name)
    htf_file = os.path.join(tracegen_path, "{}.htf".format(orig_htf_name))
    #
    parent_folder = GlobalTraceKind.CHUNKS.get_tracegen_folder_name(int_name)
    #
    name = "{}_chunk_{}".format(orig_htf_name,mut_id)
    command = ["./hibou_label.exe", "mutate_remove_actions", hsf_file, htf_file, "-p", parent_folder, "-n", name, "-m", str(max_remove_actions)]
    #
    output = subprocess.check_output(command, text=True)
    #print(output)
    #
