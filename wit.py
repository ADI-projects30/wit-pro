import filecmp
import logging
import os
import random
import shutil
import string
import sys
import zipfile
from datetime import datetime
from distutils.dir_util import copy_tree
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import pytz


def init():
    current_directory = os.getcwd()
    first_directory = os.path.join(current_directory, r'.wit')
    second_directory = os.path.join(first_directory, r'images')
    third_directory = os.path.join(first_directory, r'staging_area')
    create_active = os.path.join(first_directory, r'activated.txt')
    creating = [first_directory, second_directory, third_directory]
    if not os.path.exists(first_directory):
        for crt_dir in creating:
            os.mkdir(crt_dir)
        with open(create_active, 'w') as create:
            create.write('master')
        logging.info('Wit folders created successfully!')
    else:
        logging.info('Wit folders already exists!')

def add(file_or_directory):
    current_directory = os.getcwd()
    check_if_path_exists = os.path.join(current_directory, file_or_directory)
    if os.path.exists(check_if_path_exists):
        path = Path(check_if_path_exists)
        file_or_directory = check_if_path_exists
        print(file_or_directory)
    else:
        path = Path(file_or_directory)
    d = path.parts
    c = str(path.parent)
    pathh= os.path.split(file_or_directory)
    found = False
    for i in range(1, len(d)):
        comb = d[:-i]
        s = os.path.join(*comb)
        head_base_name = os.path.split(path)
        if '.wit' in str(os.listdir(s)) and not found:
            first_directory = os.path.join(s, r'.wit')
            final_directory = os.path.join(first_directory, r'staging_area')
            if (os.path.isfile(file_or_directory) or zipfile.is_zipfile(file_or_directory)) and head_base_name[0] == s:
                shutil.copy(file_or_directory, final_directory)
                found = True
            if (os.path.isfile(file_or_directory) or zipfile.is_zipfile(file_or_directory)) and head_base_name[0] != s:
                while pathh[0] != s:
                    pathh= os.path.split(pathh[0])
                part_of_path = file_or_directory.split(pathh[1])
                combination_of_path = pathh[1] + part_of_path[1]
                split_builting_dirs = os.path.split(combination_of_path)
                builting_path = os.path.join(final_directory, split_builting_dirs[0])
                if os.path.exists(builting_path):
                    shutil.copy(file_or_directory, builting_path)
                else:
                    os.makedirs(builting_path)
                    shutil.copy(file_or_directory, builting_path)
                found = True
            if os.path.isdir(file_or_directory):
                while pathh[0] != s:
                    pathh= os.path.split(pathh[0])
                part_of_path = file_or_directory.split(pathh[1])
                combination_of_path = pathh[1] + part_of_path[1]
                create_directory = os.path.join(final_directory, combination_of_path)
                copy_tree(file_or_directory, create_directory)
                found = True
    if '.wit' not in str(os.listdir(s)) and not found:
        raise Exception('No parent directory named .wit was found')

def commit(message):
    found = False
    the_parent = 'None'
    length = 40
    ist = pytz.timezone('Israel')
    dt_kl = datetime.now(ist)
    ist_kl = dt_kl.astimezone(ist)
    time = ist_kl.strftime('%a %b %d %H:%M:%S %Y %z')
    current_directory = os.getcwd()
    path = Path(current_directory)
    d = path.parts
    for i in range(1, len(d) + 1):
        comb = d[:i]
        s = os.path.join(*comb)
        if '.wit' in str(os.listdir(s)) and not found:
            first_directory = os.path.join(s, r'.wit')
            final_directory = os.path.join(first_directory, r'images')
            reference = os.path.join(first_directory, 'references.txt')
            the_active_file = os.path.join(first_directory, 'activated.txt')
            parents_branch = os.path.join(first_directory, 'branch_parent.txt')
            letters_and_digits = 'abcdef' + string.digits
            commit_id = ''.join(random.choice(letters_and_digits) for i in range(length))
            built_folder = os.path.join(final_directory, commit_id)
            os.mkdir(built_folder)
            if os.path.exists(reference):
                with open(reference, "r") as file_3:
                    lines = file_3.readlines()
                    the_parent = lines[0].split('=')[1].strip('\n')
            else:
                with open(reference, "w") as file_ref:
                    need_write = f'HEAD={the_parent}\n' + f'master={commit_id}\n'
                    file_ref.write(need_write)
            if not os.path.exists(parents_branch):
                with open(parents_branch, 'w') as opening_file:
                    found_parent = ''
            else:
                with open(parents_branch, 'r') as get_parents:
                    lines_parents = get_parents.readlines()
                    if len(lines_parents) > 0:
                        found_parent = lines_parents[0]
                    else:
                        found_parent = ''
            with open(parents_branch, 'w') as to_delete:
                to_delete.write('')
            with open(os.path.join(final_directory, commit_id + '.txt'), "w") as file_1:
                if found_parent == '':
                    to_write = f"parent={the_parent}\n" + f"{time}\n" + f"message={message}"
                else:
                    if the_parent == found_parent:
                        to_write = f"parent={the_parent}\n" + f"{time}\n" + f"message={message}"
                    else:
                        to_write = f"parent={the_parent}, {found_parent}\n" + f"{time}\n" + f"message={message}"
                file_1.write(to_write)
            to_copy = os.path.join(first_directory, r'staging_area')
            src_files = os.listdir(to_copy)
            copy_tree(to_copy, built_folder)
            with open(the_active_file, 'r') as branch_head:
                check_branch_head = branch_head.readlines()
                the_same_branch = check_branch_head[0]
            with open(reference, "r") as file_2:
                lines = file_2.readlines()
                check_head = lines[0].split('=')[1].strip('\n')
                check_master = lines[1].split('=')[1].strip('\n')
            with open(reference, "r") as file_2:
                lines_branch = file_2.readlines()
                for num, line_branch in enumerate(file_2, 1):
                    spliting_line = line_branch.split('=')
                    if spliting_line[0] == the_same_branch:
                        if spliting_line[1] == check_head:
                            lines_branch[num-1] = f'{the_same_branch}={commit_id}'
                            file_2.writelines(lines_branch)
            with open(reference, "w") as file_2:
                if check_head == check_master and the_same_branch == 'master':
                    lines_branch[0] = f'HEAD={commit_id}\n'
                    lines_branch[1] = f'master={commit_id}\n'
                    file_2.writelines(lines_branch)
                else:
                    lines_branch[0] = f'HEAD={commit_id}\n'
                    file_2.writelines(lines_branch)
            found = True

def status():
    head_commit_id = ''
    changes_to_be_committed = ''
    changes_not_staged_for_commit = ''
    untracked_files = ''
    compare_right_only=[]
    message_for_user = f'commit id: {head_commit_id}\n' + f'Changes to be committed: {changes_to_be_committed}\n' + f'Changes not staged for commit: {changes_not_staged_for_commit}\n' + f'Untracked files: {untracked_files}'
    found = False
    current_directory = os.getcwd()
    path = Path(current_directory)
    d = path.parts
    for i in range(1, len(d) + 1):
        comb = d[:i]
        s = os.path.join(*comb)
        if '.wit' in str(os.listdir(s)) and not found:
            first_directory = os.path.join(s, r'.wit')
            second_directory = os.path.join(first_directory, r'staging_area')
            third_directory = os.path.join(first_directory, r'images')
            reference = os.path.join(first_directory, 'references.txt')
            if os.path.exists(reference):
                with open(reference, "r") as file_1:
                    lines = file_1.readlines()
                    head_commit_id = lines[0].split('=')[1].strip('\n')
            changes_not_staged_for_commit = changes_not_staged_for_commit + check_file_dir_content(second_directory, s)
            commit_directory = os.path.join(third_directory, head_commit_id)
            changes_to_be_committed = changes_to_be_committed + (', '.join(check_if_same_directories_content(commit_directory, second_directory))) + check_file_dir_content(second_directory, commit_directory)
            untracked_files = untracked_files + (', '.join(check_for_untracked_files(s, second_directory)))
            message_for_user = f'commit id: {head_commit_id}\n' + f'Changes to be committed: {changes_to_be_committed}\n' + f'Changes not staged for commit: {changes_not_staged_for_commit}\n' + f'Untracked files: {untracked_files}'
            found = True
            print(message_for_user)
    return message_for_user

def checkout(commit_id):
    activeted = 'None'
    found = False
    current_directory = os.getcwd()
    path = Path(current_directory)
    d = path.parts
    not_replace = status()
    not_replace = not_replace.split('\n')
    if not_replace[1].split(': ')[1] != '' or not_replace[2].split(': ')[1] != '':
        raise Exception('Cant checkout')
    else:
        for i in range(1, len(d) + 1):
            comb = d[:i]
            src = os.path.join(*comb)
            if '.wit' in os.listdir(src) and not found:
                first_directory = os.path.join(src, r'.wit')
                second_directory = os.path.join(first_directory, r'staging_area')
                third_directory = os.path.join(first_directory, r'images')
                reference_file = os.path.join(first_directory, 'references.txt')
                active_file = os.path.join(first_directory, 'activated.txt')
                with open(reference_file, "r") as commit_branch:
                    find_line = commit_branch.readlines()
                    for line_branch in find_line:
                        spliting_line = line_branch.split('=')
                        if spliting_line[0] == commit_id:
                            commit_id = spliting_line[1].strip('\n')
                            activeted = spliting_line[0]  
                if sys.argv[2] == 'master':
                    with open(reference_file, "r") as file_master:
                        lines = file_master.readlines()
                        commit_id = lines[1].split('=')[1].strip('\n')
                need_copy = os.path.join(third_directory, commit_id)
                if os.path.exists(need_copy):
                    with open(active_file, 'w') as active:
                        active.write(activeted) 
                    copy_tree(need_copy, src)
                    with open(reference_file, "r") as file_2:
                        lines = file_2.readlines()
                        lines[0] = f'HEAD={commit_id}\n'
                    with open(reference_file, "w") as file_2:
                        file_2.writelines(lines)
                    for filedir in os.listdir(second_directory):
                        built_path = os.path.join(second_directory, filedir)
                        if os.path.isdir(built_path):
                            shutil.rmtree(built_path)
                        if os.path.isfile(built_path) or zipfile.is_zipfile(built_path):
                            os.remove(built_path)
                    copy_tree(need_copy, second_directory)
                found = True

def graph():
    built_graph = []
    the_end = False
    found = False
    current_directory = os.getcwd()
    path = Path(current_directory)
    d = path.parts
    for i in range(1, len(d) + 1):
        comb = d[:i]
        src = os.path.join(*comb)
        if '.wit' in os.listdir(src) and not found:
            first_directory = os.path.join(src, r'.wit')
            second_directory = os.path.join(first_directory, r'staging_area')
            third_directory = os.path.join(first_directory, r'images')
            reference_file = os.path.join(first_directory, 'references.txt')
            if os.path.exists(reference_file):
                G = nx.DiGraph()
                with open(reference_file, "r") as file_head:
                    lines = file_head.readlines()
                    head = lines[0].split('=')[1].strip('\n')
                    head_check_if_branch_in = os.path.join(third_directory, head + '.txt')
                    with open(head_check_if_branch_in, 'r') as check_if_branch:
                        ln = check_if_branch.readlines()
                        the_head_branch = ln[0].split('=')[1]
                    if ', ' not in the_head_branch:
                        built_graph.append(head)
                        print(built_graph)
                        while not the_end:
                            commit_file = os.path.join(third_directory, head + '.txt')
                            with open(commit_file, 'r') as com_file:
                                lines = com_file.readlines()
                                parent = lines[0].split('=')[1].strip('\n')
                                if parent != 'None':
                                    built_graph.append(parent)
                                    head = parent
                                else:
                                    the_end = True
                        if len(built_graph) > 1:
                            for i in range(len(built_graph) - 1):
                                G.add_edge(built_graph[i][0:6], built_graph[i + 1][0:6])
                        else:
                            built_graph.append(head)
                            for i in range(len(built_graph) - 1):
                                G.add_edge(built_graph[i][0:6], built_graph[i + 1][0:6])
                        nx.draw(G, node_color='b', node_size=2500, edgecolors='k', width=2.0, with_labels=True)
                        plt.show()
                    else:
                        connect = []
                        built_graph_2 = []
                        two_branch = the_head_branch.split(', ')
                        built_graph = [head, two_branch[0]]
                        built_graph_2 = [head, two_branch[1].strip('\n')]
                        add_parent = find_parent(built_graph[1])
                        for i in add_parent:
                            built_graph.append(i)
                        add_parent_2 = find_parent(built_graph_2[1])
                        for i in add_parent_2:
                            built_graph_2.append(i)
                        connect = [built_graph, built_graph_2]
                        for pr_lst in connect:
                            for i in range(len(pr_lst) - 1):
                                G.add_edge(pr_lst[i][0:6], pr_lst[i + 1][0:6])
                        nx.draw(G, node_color='b', node_size=2500, edgecolors='k', width=2.0, with_labels=True)
                        plt.show()

def graph2():
    built_graph = []
    current_directory = os.getcwd()
    path = Path(current_directory)
    d = path.parts
    print(d)
    for i in range(1, len(d)+1):
        comb = d[:i]
        src = os.path.join(*comb)
        if '.wit' in os.listdir(src):
            print('aaaaa')
            first_directory = os.path.join(src, r'.wit')
            second_directory = os.path.join(first_directory, r'staging_area')
            third_directory = os.path.join(first_directory, r'images')
            reference_file = os.path.join(first_directory, 'references.txt')
            if os.path.exists(reference_file):
                G = nx.DiGraph()
            tree = []
            with open(reference_file, "r") as file_head:
                lines = file_head.readlines()
                head = lines[0].split('=')[1].strip('\n')
                head_check_if_branch_in = os.path.join(third_directory, head + '.txt')
            print(head_check_if_branch_in)
            with open(head_check_if_branch_in, 'r') as check_if_branch:
                ln = check_if_branch.readlines()
                the_head_branch = ln[0].split('=')[1]
            splits = the_head_branch.split(', ')
            tree.append((head, splits[0]))
            if len(splits) > 1:
                tree.append((head, splits[1]))
            while the_head_branch != 'None':
                for i in splits:
                    if i != 'None':
                        head_check_if_branch_in = os.path.join(third_directory, i + '.txt')
                        with open(head_check_if_branch_in, 'r') as check_if_branch:
                            ln = check_if_branch.readlines()
                            the_head_branch = ln[0].split('=')[1]
                            splits = the_head_branch.split(', ')
                        if ', ' in the_head_branch:
                            tree.append((i, splits[0]))
                            tree.append((i, splits[1]))
                        else:
                            tree.append((i, the_head_branch))
            for i in tree:
                if 'None' not in i:
                    built_graph.append(i)
            G.add_edges_from(built_graph)
            nx.draw(G, node_color='b', node_size=2500, edgecolors='k', width=2.0, with_labels=True)
            plt.show()

def branch(name):
    check_if_branch_name_exists = False
    found = False
    current_directory = os.getcwd()
    path = Path(current_directory)
    d = path.parts
    for i in range(1, len(d) + 1):
        comb = d[:i]
        src = os.path.join(*comb)
        if '.wit' in os.listdir(src) and not found:
            first_directory = os.path.join(src, r'.wit')
            second_directory = os.path.join(first_directory, r'staging_area')
            third_directory = os.path.join(first_directory, r'images')
            reference_change = os.path.join(first_directory, 'references.txt')
            with open(reference_change, "r") as search_branch:
                search_line = search_branch.readlines()
                for line_branch in search_line:
                    spliting_line_branch = line_branch.split('=')
                    if spliting_line_branch[0] == name:
                        check_if_branch_name_exists = True
            if not check_if_branch_name_exists:
                if os.path.exists(reference_change):
                    with open(reference_change, 'r') as file_name:
                        lines = file_name.readlines()
                        head = lines[0].split('=')[1].strip('\n')
                    with open(reference_change, 'a') as ref_write:
                        need_write = f'{name}={head}\n'
                        ref_write.write(need_write)
            else:
                print('Branch already exists')

def merge(branch_name):
    check_if_branch_name_exists = False
    found = False
    current_directory = os.getcwd()
    path = Path(current_directory)
    d = path.parts
    for i in range(1, len(d) + 1):
        comb = d[:i]
        src = os.path.join(*comb)
        print(src)
        if '.wit' in os.listdir(src) and not found:
            first_directory = os.path.join(src, r'.wit')
            second_directory = os.path.join(first_directory, r'staging_area')
            third_directory = os.path.join(first_directory, r'images')
            reference_head = os.path.join(first_directory, 'references.txt')
            with open(reference_head, "r") as search_for_branch:
                search_for_line = search_for_branch.readlines()
                for line_branch in search_for_line:
                    spliting_line_branch = line_branch.split('=')
                    if spliting_line_branch[0] == branch_name and branch_name != 'HEAD':
                        check_if_branch_name_exists = True
            if check_if_branch_name_exists:
                with open(reference_head, 'r') as head_image:
                        lines_head = head_image.readlines()
                        head = lines_head[0].split('=')[1].strip('\n')
                path_head_image = os.path.join(third_directory, head)
                its_the_same = check_if_same_directories_content(second_directory, path_head_image)
                if its_the_same == []:
                    with open(reference_head, 'r') as file_reference:
                        find_branch = file_reference.readlines()
                        for line_branch in find_branch:
                            spliting_line = line_branch.split('=')
                            if spliting_line[0] == branch_name:
                                copy_branch = spliting_line[1].strip('\n')
                                print(copy_branch)
                    parent_of_branch = os.path.join(first_directory, 'branch_parent.txt')
                    with open(parent_of_branch, 'w') as write_parent:
                        write_parent.write(copy_branch)
                    branch_folder = os.path.join(third_directory, copy_branch)
                    copy_tree(branch_folder, second_directory)
                    commit('successful commit')
                else:
                    print('Create branch first with branch command')



def check_if_same_directories_content(first_dir, second_dir, take=None):
    if take is None:
        take = []
    check_two_directories = filecmp.dircmp(first_dir, second_dir)
    (_, mismatch, errors) =  filecmp.cmpfiles(first_dir, second_dir, check_two_directories.common_files, shallow=False)
    for i in mismatch:
        take.append(os.path.join(first_dir, i))
    if len(check_two_directories.left_only) > len(check_two_directories.right_only):
        for only_here in check_two_directories.left_only:
            path_build = os.path.join(first_dir, only_here)
            if os.path.isfile(path_build) or zipfile.is_zipfile(path_build):
                take.append(os.path.join(first_dir, only_here))
            if os.path.isdir(path_build):
                   for root, dirs, files in os.walk(path_build):
                        take.append(root)
                        if files != []:
                            for fl in files:
                                take.append(os.path.join(root, fl))
                        if dirs != [] and files == []:
                            for dr in dirs:
                                take.append(os.path.join(root, dr))        
    else:
        for only_here in check_two_directories.left_only:
            take.append(os.path.join(first_dir, only_here))
    for the_same in check_two_directories.common_dirs:
        new_dir1 = os.path.join(first_dir, the_same)
        new_dir2 = os.path.join(second_dir, the_same)
        if not check_if_same_directories_content(new_dir1, new_dir2, take):
            for i in mismatch:
                take.append(os.path.join(first_dir, i))
    return take
                
                
def check_file_dir_content(main_dir, compare_dir):
    changes = ''
    for obj in os.listdir(main_dir):
        src = os.path.join(compare_dir, obj)
        before_wit = os.path.join(main_dir, obj)
        if os.path.isdir(before_wit):
            if os.path.exists(src): 
                to_add = check_if_same_directories_content(before_wit, src)
                for i in to_add:
                    changes = changes + i + ', '
            else:
                changes = changes + before_wit + ', '
        if os.path.isfile(before_wit) or zipfile.is_zipfile(before_wit):
            if os.path.exists(src): 
                comparison = filecmp.cmp(src, before_wit, shallow = False)
                if not comparison:
                    changes = changes + before_wit + ', '
            else:
                changes = changes + before_wit + ', '
    return changes

def check_for_untracked_files(first_dir, second_dir, take=None):
    if take is None:
        take = []
    check_two_directories = filecmp.dircmp(first_dir, second_dir)
    (_, mismatch, errors) =  filecmp.cmpfiles(first_dir, second_dir, check_two_directories.common_files, shallow=False)
    if len(check_two_directories.left_only) > len(check_two_directories.right_only):
        for only_here in check_two_directories.left_only:
            path_build = os.path.join(first_dir, only_here)
            if os.path.isfile(path_build) or zipfile.is_zipfile(path_build):
                take.append(os.path.join(first_dir, only_here))
            if os.path.isdir(path_build) and '.wit' not in path_build:
                   for root, dirs, files in os.walk(path_build):
                        take.append(root)
                        if dirs == []:
                            for fl in files:
                                take.append(os.path.join(root, fl))
                        if dirs != [] and files != []:
                            comb = os.path.join(root, dirs[0])
                            for fi in files:
                                take.append(os.path.join(comb, fi))
                        if dirs != [] and files == []:
                            for dr in dirs:
                                take.append(os.path.join(root, dr))
    for the_same in check_two_directories.common_dirs:
        new_dir1 = os.path.join(first_dir, the_same)
        new_dir2 = os.path.join(second_dir, the_same)
        check_for_untracked_files(new_dir1, new_dir2, take)
    return take

def find_parent(head, built_graph=None, the_end=False):
    if built_graph is None:
        built_graph = []
    found = False
    current_directory = os.getcwd()
    path = Path(current_directory)
    d = path.parts
    for i in range(1, len(d) + 1):
        comb = d[:i]
        src = os.path.join(*comb)
        print(src)
        if '.wit' in os.listdir(src) and not found:
            first_directory = os.path.join(src, r'.wit')
            second_directory = os.path.join(first_directory, r'staging_area')
            third_directory = os.path.join(first_directory, r'images')
            while not the_end:
                commit_file = os.path.join(third_directory, head + '.txt')
                with open(commit_file, 'r') as com_file:
                    lines = com_file.readlines()
                    parent = lines[0].split('=')[1].strip('\n')
                    if parent != 'None':
                        built_graph.append(parent)
                        head = parent
                    else:
                        the_end = True
    return built_graph       


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'init':
            init()
        if sys.argv[1] == 'status':
            status()
        if sys.argv[1] == 'graph':
            graph()
        if sys.argv[1] == 'graph2':
            graph2()
        if sys.argv[1] == 'add' or sys.argv[1] == 'commit' or sys.argv[1] == 'checkout' or sys.argv[1] == 'branch' or sys.argv[1] == 'merge':
            globals()[sys.argv[1]](sys.argv[2])
