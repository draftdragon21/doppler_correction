clear; close all; clc;

carrier_freq = 845e6;
tone_freq = 1e6;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

fs = 20e6; % sampling freq
sf = 40000; % samples per frame

tx_sig = dsp.SineWave;
tx_sig.Amplitude = 0.5;
tx_sig.Frequency = tone_freq;
tx_sig.ComplexOutput = true;
tx_sig.SampleRate = fs;
tx_sig.SamplesPerFrame = sf;
tx_sig_output = tx_sig();

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

tx.CenterFrequency = carrier_freq;
rx.CenterFrequency = carrier_freq;
tx.transmitRepeat(tx_sig_output);

while 1
    sa(rx());
end