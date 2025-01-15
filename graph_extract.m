% ========================== README ==============================%
% RUN ON MATLAB 2016b OR HIGHER


%--- OVERVIEW ---%
% graph_extract.m is a MATLAB script that takes an image of a graph (.png;.jpeg;etc)
% and provides the x-/y-pixel values and corresponding x-/y-axis values.

%--- HOW TO RUN ---%
% Fill out "START OF USER INPUT" to "END OF USER INPUT" section in the
% code then run the script. 
% NOTE: First run will not display valid results, it should be used as
%       reference to pull data for a proper run's values (more info below)


%--- USER INPUT ---%
% The section "START OF USER INPUT" to "END OF USER INPUT" needs to be
% modified by the user. 

    %- input descriptions -%
    % File to be loaded:                    Name of image file being checked 
    % Logrithmic x-axis?:                   If the x-axis is in log, enter 1, if it is not, enter 0
    % Graph x,y min and max from image:     Enter the graph's x and y min/max values
        % Units do not matter, provide both xmin and xmax in the same units:
        % (i.e. both xmin and xmax are in HZ or MHz or GHz)
    % Pixel value for y-min and y-max:      Enter pixel value from matlab figure (can google how to grab this value)
        % x-pixel values are calculated automatically
    % RGB min and max values:               Enter desired color range for
    % the data line you want to pull data from. It should be the darkest to lightest in the line you are analyzing
    
clear;clc

%%
% ===================== START OF USER INPUT =====================%
%--- File to be loaded ---%
inputImage = './<folder name>/<name of image file>';

%--- Logrithmic x-axis? ---%
userInput.isLogrithmic_Xaxis = 1;

%--- Graph x,y min and max values from image---%
userInput.ymax_Value    = 100;
userInput.ymin_Value    = -10;
userInput.xmin_Value    = 30;        
userInput.xmax_Value    = 18000;     

%--- Pixel value for y-min and y-max ---% 
userInput.ymin_YPixelValue = 9539;
userInput.ymax_YPixelValue = 4398;

%--- RGB min and max values ---%
userInput.RGBmax = [126,121,255];
userInput.RGBmin = [72 ,72 ,254];



% ===================== END OF USER INPUT =====================%

%%
userInput.img = imread(inputImage)
[output, plot_data] = extract_image(userInput);
unique_data = max_data_per_unique_value(plot_data); 
export_data(unique_data, inputImage);


%%
% Export data
function export_data(unique_data, inputImage)
    % generate file name
    filename = erase(inputImage, [string('.png'),string('.jpeg'),string('.TIFF')]);
    
    %write to a table
    writetable(unique_data, strcat(filename, '.csv'))  
end

% Grabbing max Y_Value for each unique X_Value
function unique_data = max_data_per_unique_value(plot_data)

    %sort rows by 'X_Value'
    data = sortrows(plot_data, 'X_Value');
    
    % Grab unique values
    unique_x = unique(plot_data.X_Value);
    
    % Generate a matrix of zeros with size of unique_x. Used to fill later
    max_values = zeros(length(unique_x),2) ;

    % Find the max values per unique_x and put them into the max_values
    % matrix
    for i=1:length(unique_x)
        x_val = unique_x(i);
        max_y = max(data.Y_Value(data.X_Value == x_val));
        max_values(i, :) = [x_val, max_y];
    end
    
    unique_data = array2table(max_values, 'VariableNames', {'X_Values','Y_Values'});
    
end

% Pull data from image
function [output, plot_data] = extract_image(userInput)
    
    % Set image dimensions
    [graph.size.h,graph.size.w,graph.size.d] = size(userInput.img);

    % Set min and max values of x and y 
    graph.value.ymax = userInput.ymax_Value;
    graph.value.y0 = userInput.ymin_Value;
    graph.value.x0 = userInput.xmin_Value;
    graph.value.xmax = userInput.xmax_Value;

    % Set y-axis position
    graph.pixel.y0 = userInput.ymin_YPixelValue;
    graph.pixel.ymax = userInput.ymax_YPixelValue;

    % Set RGB max values
    graph.colorMatch.max(1) = uint8(userInput.RGBmax(1));  %Red Max
    graph.colorMatch.max(2) = uint8(userInput.RGBmax(2));  %Green Max
    graph.colorMatch.max(3) = uint8(userInput.RGBmax(3));  %Blue Max

    % Set RGB min values
    graph.colorMatch.min(1) = uint8(userInput.RGBmin(1));  %Red Min
    graph.colorMatch.min(2) = uint8(userInput.RGBmin(2));  %Green Min
    graph.colorMatch.min(3) = uint8(userInput.RGBmin(3)); %Blue Min

    %find pixels that meet ColorMatch criteria
    redMatch     = uint8((userInput.img(:,:,1) <= graph.colorMatch.max(1)).*(userInput.img(:,:,1) >= graph.colorMatch.min(1)));
    greenMatch   = uint8((userInput.img(:,:,2) <= graph.colorMatch.max(2)).*(userInput.img(:,:,2) >= graph.colorMatch.min(2)));
    blueMatch    = uint8((userInput.img(:,:,3) <= graph.colorMatch.max(3)).*(userInput.img(:,:,3) >= graph.colorMatch.min(3)));

    %return pixels that ONLY meet all three ColorMatch Critera
    output.match = redMatch.*greenMatch.*blueMatch;
    clear var redMatch greenMatch blueMatch
    
    %extract pixels from imported image that meet all ColorMatchCritera; convert into binary
    output.mask = logical(rgb2gray(userInput.img.*output.match));
    
    %find ColorMatching x,y pixels
    [output.data(:,1) , output.data(:,2)] = find(output.mask);

    %Calculate pixel for x0 and xmax from extracted data
    graph.pixel.x0      = min(output.data(:,2));
    graph.pixel.xmax    = max(output.data(:,2));
    
    
    %generate fit functions for converting pixel values into graph values
    if (userInput.isLogrithmic_Xaxis)
        %if xaxis is in a logrithmic scale
        graph.value.logX0   = 10*log10(graph.value.x0);
        graph.value.logXmax = 10*log10(graph.value.xmax);

        graph.yfit = fit([graph.pixel.ymax;graph.pixel.y0],[graph.value.ymax;graph.value.y0],'linearinterp');
        graph.xfit = fit([graph.pixel.xmax;graph.pixel.x0],[graph.value.logXmax;graph.value.logX0],'linearinterp');
    else
        %if xaxis is in a linear scale
        graph.yfit = fit([graph.pixel.ymax;graph.pixel.y0],[graph.value.ymax;graph.value.y0],'linearinterp');
        graph.xfit = fit([graph.pixel.xmax;graph.pixel.x0],[graph.value.xmax;graph.value.x0],'linearinterp');
    end

    %find yaxis value for each yaxis pixel
    output.data(:,3) = graph.yfit(output.data(:,1));
    
    %find xaxis value for each xaxis pixel
    output.data(:,4) = graph.xfit(output.data(:,2));

    %delinearize xvalues
    if(userInput.isLogrithmic_Xaxis)
        output.data(:,4) = 10.^(output.data(:,4)/10);
    end
    
    plot_data = array2table([output.data(:,3), output.data(:,4)], 'VariableNames', {'Y_Value','X_Value'});
    output.data = array2table([output.data],'VariableNames',{'Y_Pixel','X_Pixel','Y_Value','X_Value'});
    

    image(userInput.img);
    hold on;
    scatter(output.data.X_Pixel,output.data.Y_Pixel,...
            20,'filled'...
            );
end
