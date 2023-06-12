
from secret import swd_folder_path, bds_output_path
import sis
import os
import glob

if __name__ == "__main__":
    s = sis.GisLink()

def remove_invalid_char(overlay_name: str) -> str:
    '''
    Parameters
    ----------
    overlay_name: str
        The name of an overlay in the swd.

    Returns
    -------
    str
        Returns overlay name after removing invalid file name characters.
    '''
    return ''.join(char for char in overlay_name if char not in invalid_chars_list)

def export_internal_datasets(swd_folder_path: str, bds_output_path: str):
    '''
    Parameters
    ----------
    swd_folder_path: str
        The file path to the folder contain all the swd files for a project.
    bds_output_path: str
        The file path to the folder within which all the bds files will be exported to.
    
    Notes
    -----
    This code does not return anything, but produces a bds file for every overlay in an swd. Exporting them to the bds_output_file.
    '''
    swd_filepath_list = glob.glob(os.path.join(swd_folder_path, "*.swd"))
    
    for swd_path in swd_filepath_list:
        s.LoadSwd(swd_path)
        s.ZoomView(1000.0)
        print(f"loading {swd_path}")
        while True:
            try:
                for i in range(1000):
                    s.SetProperty(5, i, "_status&", 0)
                    total_overlay = i
            except:
                print(f"First loop completed. There are {total_overlay} overlays in file; {swd_path}")
                break
    
        
        for x in range(total_overlay):
            try:
                s.SetProperty(5, x, "_status&", 1)
                overlay_name = s.GetProperty(5, x, "_name$")
                file_name = f"{remove_invalid_char(overlay_name)}.bds"
                bds_file_path = bds_output_path + f"//{file_name}"
                s.ExportBds(bds_file_path, 64)
                s.SetProperty(5, x, "_status&", 0)
            except:
                continue

def delete_backups(bds_output_path: str):
    '''
    Parameters
    ----------
    bds_output_path: str
        The file path to the folder within which all the bds files will be exported to.
    
    Notes
    -----
        This function removes all duplicate and backup bds files from the output folder.  
    '''
    bds_filepath_list = glob.glob(os.path.join(bds_output_path, '*.bds'))
    for bds_file_path in bds_filepath_list:
        bds_file_name = os.path.basename(bds_file_path)

        if bds_file_name.startswith("Backup") or bds_file_name.endswith("Copy"):
            os.remove(bds_file_path)
    print("Backups deleted. Code complete.")


#Specifies list of invalid file name characters
invalid_chars_list = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

export_internal_datasets(swd_folder_path, bds_output_path)
delete_backups(bds_output_path)
