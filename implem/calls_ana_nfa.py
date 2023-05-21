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
import statistics


def parse_nfa_analysis_output(outwrap):
    #
    nfa_weak_warnings_num = None
    nfa_strong_warnings_num = None
    length = None
    time_to_transform = None
    time_for_analysis = None
    #
    for line in outwrap:
        if "verdict" in line:
            if "no warnings" in line:
                nfa_weak_warnings_num = 0
                nfa_strong_warnings_num = 0
            else:
                splitted = line.split(" ")
                nfa_strong_warnings_num = int(splitted[-2].strip())
                nfa_weak_warnings_num = int(splitted[-5].strip())
        # ***
        if "of length" in line:
            length = int(line.split(" ")[-1].strip()[1:-1])
        # ***
        if "time to transform" in line:
            time_to_transform = float(line.split(" ")[-1].strip()[1:-1])
        # ***
        if "time of analysis" in line:
            time_for_analysis = float(line.split(" ")[-1].strip()[1:-1])
        # ***
    #
    mydict = {
        'nfa_weak_warnings_num': nfa_weak_warnings_num,
        'nfa_strong_warnings_num': nfa_strong_warnings_num,
        'trace_length': length,
        'time_to_transform': time_to_transform,
        'time_for_analysis': time_for_analysis
    }
    return mydict

def call_nfa_analysis(hsf_file,hif_file,htf_file,num_tries):
    #
    command_nfa = ["./hibou_label.exe", "nfa_analyze", hsf_file, hif_file, htf_file]
    #
    final_dict = {}
    final_dict['nfa_time_tries'] = []
    for i in range(0,num_tries):
        output = subprocess.check_output(command_nfa,text=True).split("\n")
        try_dict = parse_nfa_analysis_output(output)
        #
        keys = ['trace_length','nfa_weak_warnings_num','nfa_strong_warnings_num']
        for key in keys:
            if key in final_dict:
                pass
            else:
                final_dict[key] = try_dict[key]
        #
        final_dict['nfa_time_tries'].append(try_dict['time_for_analysis'])
        #
    t_total = statistics.median(final_dict['nfa_time_tries'])
    final_dict['nfa_time_median'] = t_total
    #
    return final_dict



