%% PLUTO FM SWEEP TEST
% Braydon Burkhardt, Chris Tinker

clear; close all; clc;

% This program sweeps through a range of frequencies as a doppler shift sim

startingFreq = 849.95e6;
endingFreq = 850.05e6;
freqIncrement = 10e3; 
sweepTime = 20;
rxFreqMatches = false; %true rx_freq=tx_freq, false rx_freq=mid freq

% ---------------------------------------------------- %;


fs = 600e3; % sampling freq


% ----------------------------------------------------- %
% Create a TX signal by FM modulating a .wav file

filename = "./50k_pulse.wav";
[audioin, audioFs] = audioread(filename);

% upsamples audioin to the required sample rate -- ab
upsampledAudioIn = upsample(audioin, round(fs / audioFs));

% Frequency modulate input w/ a 50 kHz carrier
fmCarrierFreq = 50e3; % Use 50 kHz low-IF
fmSampleRate = fs;
freqDev = 20e3; % 20 kHz 
tx_sig = fmmod(upsampledAudioIn, fmCarrierFreq, fmSampleRate, freqDev);

sf = length(tx_sig); % samples per frame

if mod(sf, 2) % Pluto requires even # of samples / frame
    sf = sf - 1;
    tx_sig = tx_sig(1:length(tx_sig) - 1, 1);
end


% FM signal is real -- obtain complex, 1-sided analytic representation
tx_sig = dsp.SineWave;
tx_sig.Amplitude = 0.5;
tx_sig.Frequency = 50e3;
tx_sig.ComplexOutput = true;
tx_sig.SampleRate = fs;
tx_sig.SamplesPerFrame = sf;
tx_sig_output = tx_sig();
% tx_sig_output = hilbert(tx_sig);

% calc amount of increments
incAmount = (endingFreq-startingFreq)/freqIncrement;

% calc amount of received frames per freq increment
secPerInc = sweepTime/incAmount;
frameDuration = sf/fs;
framesPerInc = ceil(secPerInc/frameDuration);

pause(5);
tx = sdrtx('Pluto'); 
tx.BasebandSampleRate = fs;
tx.Gain = 0;

rx = sdrrx('Pluto');
rx.SamplesPerFrame = sf;
rx.BasebandSampleRate = fs;

sa = dsp.SpectrumAnalyzer;
sa.SampleRate = rx.BasebandSampleRate;
sa.PlotAsTwoSidedSpectrum = true;

% connect to GnuRadio UDP socket
try gnu_radio = tcpclient("127.0.0.1",4532);
catch 
end

while (true)
    for j=startingFreq:freqIncrement:endingFreq
        
        tx.CenterFrequency = j;

        % try to send an updated frequency to gnu-radio
        try writeline(gnu_radio,strcat('F ', num2str(j)));
        catch
            try gnu_radio = tcpclient("127.0.0.1",4532);
            catch 
            end
        end

        if rxFreqMatches
            rx.CenterFrequency = j;
        else
            rx.CenterFrequency = (startingFreq+endingFreq)/2;
        end

        tx.transmitRepeat(tx_sig_output);

        for k=1:1:framesPerInc
             rx_sig_input = rx();
             sa(rx_sig_input);
        end
    end
end

% release(tx);
% release(rx);
% release(sa);

