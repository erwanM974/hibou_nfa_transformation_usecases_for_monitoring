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


import statistics
import subprocess

from implem.trace_kinds import GlobalTraceKind

def parse_hibou_analysis_output(outwrap):
    #
    verdict = 'TIMEOUT'
    length = None
    node_count = None
    elapsed_time = None
    #
    for line in outwrap:
        if "verdict" in line:
            if "WeakPass" in line:
                verdict = "WeakPass"
            elif "Pass" in line:
                verdict = "Pass"
            elif "WeakFail" in line:
                verdict = "WeakFail"
            elif "Fail" in line:
                verdict = "Fail"
            elif "Inconc" in line:
                verdict = "Inconc"
            else:
                print(line)
                raise Exception("some other verdict ?")
        # ***
        if "of length" in line:
            length = int(line.split(" ")[-1].strip()[1:-1])
        # ***
        if "node count" in line:
            node_count = int(line.split(" ")[-1].strip())
        # ***
        if "elapsed" in line:
            elapsed_time = float(line.split(" ")[-1].strip())
        # ***
    #
    mydict = {
        'node_count': node_count,
        'trace_length': length,
        'hibou_verdict': verdict,
        'elapsed_time': elapsed_time
    }
    return mydict

def call_hibou_analysis(hsf_file,hif_file,htf_file,kind,num_tries,timeout):
    #
    hcf_simu_wtloc = "ana_simu_wtloc.hcf"
    hcf_simu_noloc = "ana_simu_noloc.hcf"
    hcf_prefix = "ana_prefix_noloc.hcf"
    #
    if kind == GlobalTraceKind.ACCEPTED:
        command = ["./hibou_label.exe", "analyze", hsf_file, hif_file, htf_file, hcf_prefix]
    elif kind == GlobalTraceKind.SLICE:
        command = ["./hibou_label.exe", "analyze", hsf_file, hif_file, htf_file, hcf_simu_noloc]
    else:
        command = ["./hibou_label.exe", "analyze", hsf_file, hif_file, htf_file, hcf_simu_wtloc]
    #
    final_dict = {}
    final_dict['hibou_time_tries'] = []
    for i in range(0,num_tries):
        try:
            output = subprocess.check_output(command, text=True,timeout=timeout).split("\n")
        except subprocess.TimeoutExpired:
            output = ""
        try_dict = parse_hibou_analysis_output(output)
        #
        keys = ['trace_length','hibou_verdict']
        for key in keys:
            if key in final_dict:
                pass
            else:
                final_dict[key] = try_dict[key]
        #
        final_dict['hibou_time_tries'].append(try_dict['elapsed_time'])
        #
    if None in final_dict['hibou_time_tries']:
        final_dict['hibou_time_median'] = None
    else:
        t_total = statistics.median(final_dict['hibou_time_tries'])
        final_dict['hibou_time_median'] = t_total
    #
    return final_dict



