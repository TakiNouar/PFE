@echo off
rem Runs a command with the toolchain the simplified model needs on this laptop:
rem MSVC 2022 Build Tools (C++ compiler for Brian2 and GeNN) and CUDA 12.9 (GPU).
rem Usage: with_gpu_env.cmd <command ...>
rem Example: with_gpu_env.cmd C:\Users\nouar\.venvs\brian2\Scripts\python.exe -m engine_benchmark.run_bench gpu
set "PATH=C:\Program Files (x86)\Microsoft Visual Studio\Installer;%PATH%"
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" >nul
set "CUDA_PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.9"
set "CUDA_PATH_V12_9=%CUDA_PATH%"
set "PATH=%CUDA_PATH%\bin;%PATH%"
set "PYTHONWARNINGS=ignore::UserWarning"
%*
