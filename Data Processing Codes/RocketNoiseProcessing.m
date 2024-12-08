%% Intro
% Code to import .csv files of rocket noise data, extract certain
% information, create graphs, and generate curve fits

clc, clear, close all

%% Extract data from broken .txt files

% Specify the folder path
folder = "C:\Users\joeyu\Documents\MatlabDrive\RocketNoise_BrokenTxts\FALCONHEAVY_ARABSAT6A-LAUNCHNOISE";

% Get a list of all .txt files in the folder 
% (should be all of them), but just in case
files = dir(fullfile(folder, '*.txt'));
numfiles = length(files);

dataarray = cell(numfiles,1);
rawmetadata = cell(numfiles,1);
rawsounddata = cell(numfiles,1);

% Iterate through each file
for i = 1:numfiles
    % Get the filename
    filename = fullfile(folder, files(i).name);
    
    % Import the data from the .txt file
    data = readtable(filename,"Delimiter",',');
    
    % Put each file's data into an array for easy access
    dataarray{i,1} = data;

    % Sort the data tables into metadata vs. sound data
    % if the iteration is odd (1,3,5,7...)
    if (mod(i,2)) == 1
        % assign the table as metadata
        rawmetadata{i,1} = data;
    % otherwise, it must be an even iteration
    else
        % assign the table as sounddata
        rawsounddata{i,1} = data;
    end
end

% Remove empty tables from our data arrays
sounddata = rawsounddata(~(cellfun(@isempty, rawsounddata)));
metadata = rawmetadata(~(cellfun(@isempty, rawmetadata)));

% Each set of files has some with 2 extra lines, for pre/post cal. sens.,
% We don't care about the extra 2 headings in those files,
% So, we need to remove them to get a consistent format:

% loop through the metadata cell array of tables
for i = 1:length(metadata)
    % find the size of the given table
    [Rows, Cols] = size(metadata{i});

    % if the table has 37 rows...
    if Rows == 37
        % ... then delete rows 21 and 22 (the rows we don't care about)
        metadata{i}([21, 22],:) = [];
    end
    
    % REMOVE LINE 26 for FALCON9 ONLY
    %metadata{i}(26,:) = [];
end

%% Setting up the master-file: Size and Headings

% Find the largest table size (row/col) in each of our arrays
% This is important to make the master-file a large enough size
maxRows = 0;
maxCols = 0;
for i = 1:numel(sounddata)
    % Get the size of the current table
    [numRows, numCols] = size(sounddata{i});
    
    % Update the maximum size if necessary
    maxSoundRows = max(maxRows, numRows);
    maxSoundCols = max(maxCols, numCols);

    if numRows > maxRows
        maxRows = numRows;
        maxSoundRowsIndex = i;
    end
end

maxRows = 0;
maxCols = 0;

for i = 1:numel(metadata)
    % Get the size of the current table
    [numRows, numCols] = size(metadata{i});
    
    % Update the maximum size if necessary
    maxMetaRows = max(maxRows, numRows);
    maxMetaCols = max(maxCols, numCols);

    if numRows > maxRows
        maxRows = numRows;
        maxMetaRowsIndex = i;
    end
end

% Create the master-file with our max size
masterfile = cell((maxMetaRows+maxSoundRows),(numfiles/2));
numsets = numfiles/2;

% Setup headings in our master-file:
masterfile(1:size(metadata{maxMetaRowsIndex,1},1),1) = table2array(metadata{maxMetaRowsIndex,1}(1:size(metadata{maxMetaRowsIndex,1},1),1));
%masterfile(:,2) = metadata{1,1}(:,1);

% Now, finally insert the meta-data into their correspondings columns
for i=(1:numsets)
    masterfile(1:maxMetaRows,(i+1)) = table2cell(metadata{i}(:,2));
end

%% Setting up the master-file: Sound Data Headings

% Since our files start at different times, we need to normalize them

% We'll start by finding the start time of each file:
starttimes = zeros(length(sounddata),1);
for i = 1:numsets
    starttimes(i,1) = seconds(table2array(sounddata{i}(2,1)));
end

% Now, we need to determine what is the "earliest" start time,
% so we can set that to be our global start time
GlobalStart = round(min(starttimes));
% also the last time will be handy...
GlobalEnd = round(max(starttimes));

% Find the time of launch in seconds; this will be our t=0
% MUST BE MANUALLY FOUND FOR EACH LAUNCH (not that bad dw)
LaunchTime = 81300;

% % Set the master-file sound data to start at our global start...
% masterfile{(maxRows + 1),1} = (GlobalStart);
% % ...and go up in 1s intervals from there, to the maxsoundrows #
% for i=(1:maxSoundRows)
%     masterfile{(maxRows + 1 + i),1} = (GlobalStart + i);
% end

% Set the master-file sound data to start at our global start...
masterfile{(maxRows + 1),1} = (GlobalStart - LaunchTime);
% ...and go up in 1s intervals from there, to the maxsoundrows #
numtimestamps = (maxSoundRows + abs(GlobalStart - LaunchTime) + abs(GlobalEnd - LaunchTime)-2);
for i = (1:numtimestamps)
    masterfile{(maxRows + 1 + i),1} = ((GlobalStart - LaunchTime) + i);
end

%% Normalizing the sound data time

% Now the hard part... we need to assign each file of sound data to its
% respective place in time. Unfortunately, our times are not all on 
% even 1 sec intervals. So, for those that are not, we need to round them
% to the nearest full second.

% Loop through each sound data file
for i = (1:numsets)

    % open a sound data file and get its timestamps
    timestamps = seconds(table2array(sounddata{i}(:,1)));

    % remove the first value in the list cuz it's "NaN"
    timestamps(1,:) = [];

    % round the rest of the timestamps
    timestamps = round(timestamps - LaunchTime);

    % find its starting time
    start = min(timestamps);

    % do the same thing as above, but with the dB data (column 2)
    dBdata = (table2array(sounddata{i}(:,2)));
    dBdata(1,:) = [];

    % concat the timestamps and dBdata into one
    both = [timestamps dBdata];

    % .. and insert that set of dBdata into the position in the
    % masterfile where its starting time lines up
    for b = 1:length(both)
        masterfile{maxMetaRows + start + b + abs(GlobalStart - LaunchTime),1 + i} = both(b,2);
    end
end

%% Saving the master-file

% Now the master file is complete and we just need to save it...
% (easier said than done???)

% first convert it to a table:
mastertable = cell2table(masterfile);
% and transpose it:
mastertable = rows2vars(mastertable);

% Now we need to move the header row to be the variable names of the table
% First, set up our variable names:
timenames = cell(1,numtimestamps+1);
for i=1:(numtimestamps+1)
    timenames{i} = ['T=' num2str(i-13)];
end
varsnames = [mastertable{1,1:(maxMetaRows+1)} timenames];
mastertable.Properties.VariableNames = varsnames;
mastertable(1,:) = [];

% specify file location:
filelocation = 'C:\Users\joeyu\Documents\MatlabDrive\ArcGIS_Masterfiles\MasterFile_FALCONHEAVY.csv';

% save it !
writetable(mastertable, filelocation);
