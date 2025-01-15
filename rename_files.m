clear;clc


folder_path = './'; %Current directory
files = dir(fullfile(folder_path, 'Pages*')); %desired files with specific keyword names

%sort file names
[~, idx] = sort({files.name});
sorted_files = files(idx);

destination_folder = './rename/'; % desination folder

% Start of desired page number (for renaming)
page_number = 569; 

% Pull out only specific pages
relevant_pages = [570, 571, 575, 579, 582, 585, 586, 590, 594, 597, 600, 603, 604, 608, 612, 615, 618, 619, 623, 627];


for i = 1:numel(sorted_files)
    
    if ismember(page_number, relevant_pages)
        source_file = fullfile(folder_path, sorted_files(i).name);
        [~, filename, ext] = fileparts(sorted_files(i).name);
        new_filename = ['pg', string(page_number) , '_QTR56006100EMI_', ext];
        new_filename_as_char= char(strcat(new_filename(1),new_filename(2), new_filename(3), new_filename(4)));
        destination_file = fullfile(destination_folder, new_filename_as_char);
        copyfile(source_file, destination_file);
    end 
    page_number = page_number + 1;
end

    