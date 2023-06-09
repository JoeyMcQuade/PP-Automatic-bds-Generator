
from secret import swd_folder_path, bds_output_file
import sis
import os
import glob

if __name__ == "__main__":
    s = sis.GisLink()

def remove_invalid_char(overlay_name):
    return ''.join(char for char in overlay_name if char not in invalid_chars_list)

def export_internal_datasets(swd_path, output_folder):
    s.LoadSwd(swd_path)
    while True:
        try:
            for i in range(100):
                s.SetProperty(5, i, "_status&", 0)
                total_overlay = i
        except:
            break
    
    s.ZoomView(1000.0)

    for x in range(total_overlay):
        s.SetProperty(5, x, "_status&", 1)
        overlay_name = s.GetProperty(5, x, "_name$")
        file_name = f"{remove_invalid_char(overlay_name)}.bds"
        bds_file_path = output_folder + file_name
        s.ExportBds(bds_file_path, 64)
        s.SetProperty(5, x, "_status&", 0)

# def find_all_swd(swd_folder):
#     all_swd_files = glob.glob(os.path.join(swd_folder, ".bds"))
#     for swd_file_path in all_swd_files:
#         print(swd_file_path)
#         export_internal_datasets(swd_file_path, bds_output_file)

def delete_backups(bds_folder):
    bds_filepath_list = glob.glob(os.path.join(bds_folder, '*.bds'))
    for bds_file_path in bds_filepath_list:
        bds_file_name = os.path.basename(bds_file_path)

        if bds_file_name.startswith("Backup") or bds_file_name.endswith("Copy"):
            os.remove(bds_file_path)


#Spcifies list of invalid characters
invalid_chars_list = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

export_internal_datasets(swd_folder_path, bds_output_file)
delete_backups(bds_output_file)
