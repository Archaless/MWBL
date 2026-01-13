% MKIII_csv2mat.m:
% Marine Wave Boundary Layer Analysis
% Script for converting Rainwise MKIII data files from .csv to .mat
%
% Input: 
%   inputFile	- string variable, Ambilabs .csv file name
%   inputDir	- string variable, absolute or relative path to .txt input_file
%   outputDir	- string variable, absolute or relative path to write .mat file
%
% Output: A .mat file containing the following variables:
%   date_time	- Matlab formatted date and time (UTC)
%   WindSpd - (m/s)
%   WindDir - (Deg.), 0 is Northerly
%   Baro - Barometric Pressure (mBar)
%   

% Created by Tyler Knapp, 09/09/2025

function MKIII_csv2mat(fileName,inputDir,outputDir)
arguments
  % Test a file as default
  fileName = 'Rainwise_MK_W3425_20250930_SMAST.csv';
  inputDir = '/usr2/MWBL/Data/RainwisePortLog/raw/';
  outputDir = '/usr2/MWBL/Data/RainwisePortLog/processed/';
end
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  Version = 'KMIII_csv2mat, Version 09/09/2025';
  disp([Version, ' is running']);
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
  samplePeriod = 300; % seconds
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % specify the variables and units
  
  MKvar={'date_time';'T_Air';'RelHumid';'Baro';'WindSpd';'WindDir';'Precip';'SRad'};%'T_Encl'};
  additionalVar = {'Dew'; 'WS_Max'; 'SR_sum'; 'Volts';};

  variables = {'date_time';                           'T_Air'; 'RelHumid'; 'Dew';  'Baro';'WindDir';                             'WindSpd';'WS_Max';'SRad';    'SR_sum';'Precip';'Volts';'u'; 'v'};
  units =     {'Matlab formatted date and time (UTC)';'Deg C'; '%';        'Deg C';'mbar';'Compass Degrees (e.g. 360 => from N)';'m/s';    'm/s';   'Watts/m2';'J/m2';  'mm/hr'; 'Volts';'m/s';'m/s'};
  
  numvars = length(MKvar);
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  disp([' Reading ',fileName]);

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % Read data file as table
  fileData = readtable([inputDir,fileName],'PreserveVariableNames',true,'Delimiter',',');
  dataRaw = table;
  % fileData = movevars(fileData, "date_time", 'before',"time (Sec. from Epoch)");
  % fileData.("time (Sec. from Epoch)") = [];

  key = ["°";"%";'"';" mph";"°";'"';'W/m²';];
  for i = 1:numvars
    try
      dataRaw.(MKvar{i}) = str2double(strrep(fileData{:,i},key(i-1),""));
    catch % If data is already a number above will throw error
      dataRaw.(MKvar{i}) = fileData{:,i};
    end
  end
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % Data Processing
  dataOut = table;
  % Average Data
  for i = 2:length(MKvar)
    [dataOut.(MKvar{1}),dataOut.(MKvar{i}),~] = ensembleAverage(dataRaw.(MKvar{1}),dataRaw.(MKvar{i}),samplePeriod);
  end
  % Convert units
  dataOut.('T_Air') = (dataOut.('T_Air')-32)*5/9; % F => C
  dataOut.('Baro') = dataOut.('Baro')*33.86389; % InHg => mBar
  dataOut.('WindSpd') = dataOut.('WindSpd')*0.44704; % mph => m/s
  dataOut.('Precip') = dataOut.('Precip')*25.4; % in => mm
  % Filter out spikes
  % Note: Limits are over the course of 5 minutes
  dataOut.('T_Air') = remove_spikes(dataOut.('T_Air'),10); % Sample (Air) Temp
  dataOut.('RelHumid') = remove_spikes(dataOut.('RelHumid'),10); % Relative Humidity
  dataOut.('Baro') = remove_spikes(dataOut.('Baro'),10); % Barometric Pressure
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % Parse all variables from table format to array format
  date_time = datetime(dataOut.date_time,'convertFrom','epochTime');
  date_time = datetime(date_time, "InputFormat","dd-MMM-yyyy HH:mm:ss");
  for n=2:numvars
    eval([MKvar{n},' = dataOut{:,n};']);
  end

  [u_corr,v_corr,WindDir_corr,WindSpd_corr] = compass_correction_function(date_time(1),date_time(end),'SMAST_PortLog',[],[],dataOut.WindDir,dataOut.WindSpd);
  
  u = u_corr;
  v = v_corr;
  WindDir = WindDir_corr;
  WindSpd = WindSpd_corr;

  % Add additional vars
  for i = 1:length(additionalVar)
    eval([additionalVar{i},' = NaN(length(dataOut.date_time),1);']);
  end

  outputFile = strrep(fileName,'.csv','');
  
  disp([' Saving output to ',outputDir,outputFile]);
  disp(' ');

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % Save variable names and units
  save([outputDir,outputFile],'Version','variables','units');
  for n = 1:length(variables)  
    save([outputDir,outputFile],variables{n},'-append');
  end
end