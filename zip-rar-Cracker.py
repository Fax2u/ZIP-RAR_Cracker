import zipfile
import patoolib
from rarfile import RarFile
import multiprocessing
from multiprocessing.queues import Empty
import time
import os
RarFile.UNRAR_TOOL = "UnRAR.exe"


def printing_function(mode, archive="", dictionary="", password="", line_length=100):
    if max(len(archive), len(dictionary)) > line_length:
        line_length = max(len(archive), len(dictionary))

    if mode == "begin":
        title_string = "Zip / RAR Cracker"
        author_string = "by Guy Levavi"
        print(f"{'-' * line_length}")
        print(f"{' ' * ((line_length - len(title_string)) // 2)}{title_string}")
        print(f"{' ' * ((line_length - len(author_string)) // 2)}{author_string}")
        print(f"{'-' * line_length}\n")

    if mode == "start":
        print(f"\n{'-' * ((line_length - 14) // 2)} Archive Name {'-' * ((line_length - 14) // 2)}")
        print(f"{' ' * ((line_length - len(archive)) // 2)}{archive}")
        print(f"\n{'-' * ((line_length - 30) // 2)} Password Dictionary Filename {'-' * ((line_length - 30) // 2)}")
        print(f"{' ' * ((line_length - len(dictionary)) // 2)}{dictionary}\n")
        print(f"{' ' * ((line_length - 49) // 2)}Launching multi-core matrix crunching sequence...")
        return line_length

    if mode == "end":
        print(f"\n{'-' * ((line_length - 20) // 2)} Archive Extracted! {'-' * ((line_length - 20) // 2)}")
        print(f"{' ' * ((line_length - 18) // 2)} Result password: ")
        print(f"{' ' * ((line_length - len(password)) // 2)}{password}")
        print('-' * line_length)

    if mode == "failed":
        print(f"\n{'-' * ((line_length - 19) // 2)} Process Finished! {'-' * ((line_length - 19) // 2)}")
        print(f"{' ' * ((line_length - 27) // 2)} Failed to Extract Archive ")
        print('-' * line_length)

    if mode == 'cleanup':
        print(f"{' ' * ((line_length - 42) // 2)} Cleaning up Excess passwords from RAM... ")


def print_progress_bar(iteration, total, suffix='', line_length=100):
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int((line_length - 28) * iteration // total)
    bar = '█' * filled_length + '-' * (line_length - 28 - filled_length)

    if not hasattr(print_progress_bar, 'rolling_index'):
        print_progress_bar.rolling_index = 0
    signs = ['|', '/', '-', '\\']
    rolling_indicator = signs[print_progress_bar.rolling_index % len(signs)]

    if iteration == total:
        print(f'\rProgress: |{bar}| {percent}% {suffix}', end='', flush=True)
    else:
        print(f'\rProgress: |{bar}| {percent}% {rolling_indicator} {suffix}', end='', flush=True)
        print_progress_bar.rolling_index += 1


def progress_bar_process(parts_complete, total_parts, stop_flag, line_length):
    while parts_complete.value < total_parts:
        if stop_flag.value:
            print_progress_bar(total_parts, total_parts, suffix='Complete', line_length=line_length)
            break
        else:
            print_progress_bar(parts_complete.value, total_parts, suffix='Working!', line_length=line_length)
        time.sleep(1)


def zip_or_rar(filepath):
    zip_signature = b'PK\03'
    rar_signature = b'Rar!\x1a\x07\x01\x00'
    try:
        file = open(filepath, 'rb')
        header = file.read()
        file.close()
        if zip_signature == header[:len(zip_signature)]:
            return 'ZIP'
        if rar_signature == header[:len(rar_signature)]:
            return 'RAR'
        else:
            return None
    except Exception as e:
        raise e


def open_pass_file(filepath, queue, max_lines_per_list=100):
    try:
        with open(filepath, encoding='utf-8', errors='ignore') as file:
            data = file.readlines()

        current_list = []
        for line in data:
            current_list.append(line.strip('\n'))

            if len(current_list) == max_lines_per_list:
                queue.put(current_list)
                current_list = []

        if current_list:
            queue.put(current_list)
        return len(data)
    except Exception as e:
        raise e


def crack_archive(archive_name, archive_type, queue, result_password, stop_flag, parts_complete, tool, extract_path):
    while not stop_flag.value:
        try:
            password_list = queue.get(timeout=5)
        except Empty:
            break

        if archive_type == 'ZIP':
            zf = zipfile.ZipFile(archive_name)
            for password in password_list:
                try:
                    if stop_flag.value:
                        break

                    file_info = zf.infolist()[0]
                    file_info.filename = os.path.basename(file_info.filename)
                    zf.extract(file_info, path='.', pwd=bytes(password, 'utf8'))
                    result_password.value = password
                    stop_flag.value = True
                    time.sleep(1)
                    extracted_file_path = os.path.join(os.getcwd(), file_info.filename)
                    try:
                        os.remove(extracted_file_path)
                    except:
                        pass
                    zf.extractall(path=extract_path, pwd=bytes(password, 'utf8'))
                    zf.close()
                    break
                except:
                    pass

        if archive_type == 'RAR':
            for password in password_list:
                try:
                    if stop_flag.value:
                        break

                    if tool == "Patool":
                        patoolib.extract_archive(archive=archive_name,
                                                 outdir=extract_path,
                                                 password=password,
                                                 verbosity=-1,
                                                 interactive=False)
                        result_password.value = password
                        stop_flag.value = True
                        time.sleep(1)

                    if tool == "unrar":
                        rf = RarFile(archive_name)
                        rf.setpassword(pwd=password)
                        file_info = rf.infolist()[0]
                        file_info.filename = os.path.basename(file_info.filename)
                        rf.extract(file_info, path='.')
                        result_password.value = password
                        stop_flag.value = True
                        time.sleep(1)
                        extracted_file_path = os.path.join(os.getcwd(), file_info.filename)
                        try:
                            os.remove(extracted_file_path)
                        except:
                            pass
                        rf.extractall(path=extract_path)
                        rf.close()
                    break
                except:
                    pass
        parts_complete.value += len(password_list)


def user_selections():
    archive_file_name = input("Enter Archive Filename or Path: ").strip('"')
    passwords_file_name = input("Enter Password Dictionary Filename or Path: ").strip('"')
    extract_path = input("Enter Extract Path (Leave Blank for Current Folder): ").strip('"')

    new_folder_name = archive_file_name.rsplit('\\', 1)[-1]
    if not extract_path:
        extract_path = new_folder_name.replace('.', '-')
    else:
        extract_path += '\\'
        extract_path += new_folder_name.replace('.', '-')

    archive_type = zip_or_rar(archive_file_name)
    rar_tool = ''
    if archive_type == 'RAR':
        while True:
            rar_tool = input("Enter 0 to use Patool, Enter 1 to use unrar.exe: ")
            if rar_tool == '0':
                rar_tool = "Patool"
                break
            elif rar_tool == '1':
                rar_tool = 'unrar'
                break
            else:
                print("Invalid input!")
                continue

    return archive_file_name, passwords_file_name, archive_type, extract_path, rar_tool


def main():
    printing_function("begin")
    queue = multiprocessing.Queue()
    archive_file_name, passwords_file_name, archive_type, extract_path, rar_tool = user_selections()
    password_lists_length = open_pass_file(passwords_file_name, queue)
    line_length = printing_function("start", archive=archive_file_name, dictionary=passwords_file_name)

    manager = multiprocessing.Manager()
    result_password = manager.Value('s', "")
    stop_flag = manager.Value('b', False)
    parts_complete = manager.Value('i', 0)

    processes = [multiprocessing.Process(target=crack_archive,
                                         args=(archive_file_name,
                                               archive_type,
                                               queue,
                                               result_password,
                                               stop_flag,
                                               parts_complete,
                                               rar_tool,
                                               extract_path)) for _ in range(multiprocessing.cpu_count())]

    progress_process = multiprocessing.Process(target=progress_bar_process,
                                               args=(parts_complete,
                                                     password_lists_length,
                                                     stop_flag,
                                                     line_length))
    progress_process.start()

    for process in processes:
        if not stop_flag.value:
            process.start()

    if stop_flag.value:
        for process in processes:
            if process.is_alive():
                process.join()

    for process in processes:
        process.join()

    progress_process.terminate()
    progress_process.join()

    if result_password.value != '':
        printing_function("end", password=result_password.value, line_length=line_length)
    else:
        printing_function("failed", line_length=line_length)

    if not queue.empty():
        printing_function('cleanup', line_length=line_length)
        while True:
            try:
                queue.get(timeout=0.1)
            except Empty:
                break
            except:
                if queue.empty():
                    break
                else:
                    continue

    queue.close()
    queue.join_thread()


if __name__ == '__main__':
    main()
