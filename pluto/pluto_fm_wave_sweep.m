%% PLUTO FM SWEEP TEST
% Braydon Burkhardt

clear; close all; clc;
%configurePlutoRadio('AD9364');

% This program sweeps through a range of frequencies as a doppler shift sim
% A tone is transmitted with a shifting carrier frequency

startingFreq = 845e6;
endingFreq = 855e6;
freqIncrement = 100e3; 
sweepTime = 20;
toneFreq = 1e6;
rxFreqMatches = false; %true rx_freq=tx_freq, false rx_freq=mid freq

% ---------------------------------------------------- %


fs = 20e6; % sampling freq


% ----------------------------------------------------- %
% Create a TX signal by FM modulating a .wav file

% tx_sig = dsp.SineWave;
% tx_sig.Amplitude = 0.5;
% tx_sig.Frequency = toneFreq;
% tx_sig.ComplexOutput = true;
% tx_sig.SampleRate = fs;
% tx_sig.SamplesPerFrame = sf;
% tx_sig_output = tx_sig();
filename = "./txpulse.wav";
[audioin, audioFs] = audioread(filename);

% upsamples audioin to the required sample rate -- ab
upsampledAudioIn = upsample(audioin, round(fs / audioFs));

% Frequency modulate input w/ a 50 kHz carrier
fmCarrierFreq = 50e3; % Use 50 kHz low-IF
fmSampleRate = fs;
freqDev = 20e3; % 20 kHz 
tx_sig = fmmod(upsampledAudioIn, fmCarrierFreq, fmSampleRate, freqDev);

size(tx_sig)
length(tx_sig)
sf = length(tx_sig); % samples per frame
if mod(sf, 2)
    sf = sf - 1;
    tx_sig = tx_sig(1:length(tx_sig) - 1, 1);
end

%sf
%plot_dft_mag(tx_sig, fmSampleRate, 100);
%figure;
%spectrogram(tx_sig);

% FM signal is real -- obtain complex, 1-sided analytic representation
tx_sig_output = hilbert(tx_sig);
size(tx_sig_output)

% calc amount of increments
incAmount = (endingFreq-startingFreq)/freqIncrement;

% calc amount of received frames per freq increment
secPerInc = sweepTime/incAmount;
frameDuration = sf/fs;
framesPerInc = ceil(secPerInc/frameDuration);
secPerInc
frameDuration
framesPerInc

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

while (true)
    for j=startingFreq:freqIncrement:endingFreq

        tx.CenterFrequency = j;

        if rxFreqMatches
            rx.CenterFrequency = j;
        else
            rx.CenterFrequency = (startingFreq+endingFreq)/2;
        end

        tx.transmitRepeat(tx_sig_output);

        for k=1:1:framesPerInc
             sa(rx());
        end
    end
end

% release(tx);
% release(rx);
% release(sa);

