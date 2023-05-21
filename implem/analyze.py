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

import os


from implem.calls_ana_simu import call_hibou_analysis
from implem.calls_ana_nfa import call_nfa_analysis
from implem.commons import FOLDER_MODEL
from implem.trace_kinds import GlobalTraceKind




def analysis_process(int_name,num_tries,polling_timeout):
    f = open("{}.csv".format(int_name), "w")
    f.truncate(0)  # empty file
    columns = ["name",
               "kind",
               "trace_length",
               "hibou_time_tries",
               "hibou_time_median",
               "hibou_verdict",
               "nfa_time_tries",
               "nfa_time_median",
               "nfa_weak_warnings_num",
               "nfa_strong_warnings_num"]
    f.write(";".join(columns) + "\n")
    f.flush()
    #
    kinds = [GlobalTraceKind.ACCEPTED,GlobalTraceKind.SLICE,GlobalTraceKind.CHUNKS,GlobalTraceKind.NOISE]
    #
    hsf_file = os.path.join(FOLDER_MODEL, "{}.hsf".format(int_name))
    hif_file = os.path.join(FOLDER_MODEL, "{}.hif".format(int_name))
    #
    for kind in kinds:
        print("analyzing {} traces for {}".format(kind.kind_repr(), int_name))
        folder = kind.get_tracegen_folder_name(int_name)
        for htf_file in os.listdir(folder):
            htf_file_name = htf_file[:-4]
            htf_file = os.path.join(folder, htf_file)
            #
            simu_dict = call_hibou_analysis(hsf_file, hif_file, htf_file, kind, num_tries, polling_timeout)
            nfa_dict = call_nfa_analysis(hsf_file,hif_file,htf_file,num_tries)
            f.write("{};{};{};{};{};{};{};{};{};{}\n".format(htf_file_name,
                                                        kind.kind_repr(),
                                                         nfa_dict['trace_length'],
                                                         simu_dict['hibou_time_tries'],
                                                         simu_dict['hibou_time_median'],
                                                         simu_dict['hibou_verdict'],
                                                         nfa_dict['nfa_time_tries'],
                                                         nfa_dict['nfa_time_median'],
                                                         nfa_dict['nfa_weak_warnings_num'],
                                                         nfa_dict['nfa_strong_warnings_num']))
            f.flush()



