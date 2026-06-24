import json
import re
import subprocess
import os.path
import os
import time
from .cpg_client_wrapper import CPGClientWrapper
#from ..data import datamanager as data
def funcs_to_graphs(funcs_path):
    client = CPGClientWrapper()
    # query the cpg for the dataset
    print(f"Creating CPG.")
    graphs_string = client(funcs_path)
    # removes unnecessary namespace for object references
    graphs_string = re.sub(r"io\.shiftleft\.codepropertygraph\.generated\.", '', graphs_string)
    graphs_json = json.loads(graphs_string)
    return graphs_json["functions"]
def graph_indexing(graph):
    idx = int(graph["file"].split(".c")[0].split("/")[-1])
    del graph["file"]
    return idx, {"functions": [graph]}
def joern_parse(joern_path, input_path, output_path, file_name):
    out_file = file_name + ".bin"
    joern_parse_call = subprocess.run(["./" + joern_path + "joern-parse", input_path, "--out", output_path + out_file],
                                      stdout=subprocess.PIPE, text=True, check=True)
    print(str(joern_parse_call))
    return out_file
def joern_create(joern_path, in_path, out_path, cpg_files):
    json_files = []
    for cpg_file in cpg_files:
        json_file_name = f"{cpg_file.split('.')[0]}.json"
        json_files.append(json_file_name)
        print(in_path + cpg_file)
        if os.path.exists(in_path + cpg_file):
            json_out = f"{os.path.abspath(out_path)}/{json_file_name}"
            abs_cpg = f"{os.path.abspath(in_path)}/{cpg_file}"
            script_path = f"{os.path.dirname(os.path.abspath(joern_path))}/graph-for-funcs.sc"
            commands = (
                f'importCpg("{abs_cpg}")\n'
                f'cpg.runScript("{script_path}").toString() |> "{json_out}"\n'
                f'delete\n'
                f'exit\n'
            )
            env = os.environ.copy()
            env["TERM"] = "dumb"
            env["JAVA_OPTS"] = "-Djline.terminal=jline.UnsupportedTerminal"
            try:
                result = subprocess.run(
                    ["./" + joern_path + "joern", "--nocolors"],
                    input=commands.encode(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env=env,
                    timeout=600
                )
                print(f"Done: {json_file_name}")
                if result.stdout:
                    print(result.stdout.decode(errors="ignore")[:200])
            except subprocess.TimeoutExpired:
                print(f"Timeout: {cpg_file}")
    return json_files
def json_process(in_path, json_file):
    if os.path.exists(in_path+json_file):
        with open(in_path+json_file) as jf:
            cpg_string = jf.read()
            cpg_string = re.sub(r"io\.shiftleft\.codepropertygraph\.generated\.", '', cpg_string)
            cpg_json = json.loads(cpg_string)
            container = [graph_indexing(graph) for graph in cpg_json["functions"] if graph["file"] != "N/A"]
            return container
    return None
'''
def generate(dataset, funcs_path):
    dataset_size = len(dataset)
    print("Size: ", dataset_size)
    graphs = funcs_to_graphs(funcs_path[2:])
    print(f"Processing CPG.")
    container = [graph_indexing(graph) for graph in graphs["functions"] if graph["file"] != "N/A"]
    graph_dataset = data.create_with_index(container, ["Index", "cpg"])
    print(f"Dataset processed.")
    return data.inner_join_by_index(dataset, graph_dataset)
'''
# client = CPGClientWrapper()
# client.create_cpg("../../data/joern/")
# joern_parse("../../joern/joern-cli/", "../../data/joern/", "../../joern/joern-cli/", "gen_test")
# print(funcs_to_graphs("/data/joern/"))
"""
while True:
    raw = input("query: ")
    response = client.query(raw)
    print(response)
"""