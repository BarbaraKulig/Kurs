import os
import shutil
import threading


def sort_files_by_extension(src_folder, dest_folder):
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            src_path = os.path.join(root, file)

            _, extension = os.path.splitext(file)
            extension_folder = os.path.join(dest_folder, extension)

            if not os.path.exists(extension_folder):
                os.makedirs(extension_folder)

            shutil.move(src_path, os.path.join(extension_folder, file))


def process_folder(src_folder, dest_folder):
    threads = []

    for root, dirs, files in os.walk(src_folder):
        for directory in dirs:
            folder_path = os.path.join(root, directory)

            thread = threading.Thread(target=sort_files_by_extension, args=(folder_path, dest_folder))
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    source_folder = "Bałagan"
    destination_folder = "Sorted"

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    process_folder(source_folder, destination_folder)
